"""token 口径测量：验证"字符数 * 系数"能否替代真实 token 计数。

用法：python eval/measure_tokens.py
输出：语料构成、按中文占比分桶的 token/字符比率、token 最多的块、纯中文基准。
"""
import io
import contextlib
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import ingest  # noqa: E402
from transformers import AutoTokenizer  # noqa: E402

TOKENIZER = "BAAI/bge-small-zh"
DOC = Path(__file__).resolve().parent.parent / "docs" / "Dive-into-DL-Pytorch.md"


def cjk_ratio(text):
    if not text:
        return 0.0
    return sum(1 for c in text if "\u4e00" <= c <= "\u9fff") / len(text)


def n_tokens(tok, text):
    return len(tok(text, add_special_tokens=False)["input_ids"])


def main():
    tok = AutoTokenizer.from_pretrained(TOKENIZER)
    raw = DOC.read_text(encoding="utf-8")
    clean = ingest.clean_txt(raw)

    print(f"max_seq_length = {tok.model_max_length}\n")
    print("=== 语料构成 ===")
    for name, text in (("原文", raw), ("清洗后", clean)):
        n = n_tokens(tok, text)
        print(f"{name}: 字符 {len(text):,} / token {n:,} / 中文占比 {cjk_ratio(text)*100:.1f}% / {n/len(text):.3f} token 每字符")

    with contextlib.redirect_stdout(io.StringIO()):
        chunks = ingest.split_documents({"d2l": clean})
        kept = ingest.filter_chunks(chunks)
    texts = [c[3] for c in kept]
    ratios = [cjk_ratio(t) for t in texts]
    print(f"\n入库块 {len(texts)} 个：中文占比 中位 {statistics.median(ratios)*100:.1f}% / 最高 {max(ratios)*100:.1f}% / 最低 {min(ratios)*100:.1f}%")

    print("\n=== 按中文占比分桶 ===")
    buckets = [(0.00, 0.15), (0.15, 0.30), (0.30, 0.50), (0.50, 0.70), (0.70, 0.85), (0.85, 1.01)]
    for lo, hi in buckets:
        sel = [t for t in texts if lo <= cjk_ratio(t) < hi]
        label = f"中文 {lo*100:>3.0f}-{hi*100:>3.0f}%"
        if not sel:
            print(f"{label}: 0 块（被中文占比 <15% 的过滤规则丢弃）")
            continue
        rs = [n_tokens(tok, t) / len(t) for t in sel]
        worst = max(sel, key=lambda t: n_tokens(tok, t))
        print(f"{label}: {len(sel):>3} 块 / 比率 中位 {statistics.median(rs):.3f} / 区间 [{min(rs):.3f}, {max(rs):.3f}] / 最大块 {len(worst)} 字 = {n_tokens(tok, worst)} token")

    print("\n=== token 最多的 5 个块 ===")
    for t in sorted(texts, key=lambda x: -n_tokens(tok, x))[:5]:
        print(f"  {len(t)} 字 / {n_tokens(tok, t)} token / 中文 {cjk_ratio(t)*100:.0f}%: {t[:36]!r}")

    print("\n=== 纯中文基准 ===")
    pure = [t for t in texts if cjk_ratio(t) > 0.95]
    if pure:
        rs = [n_tokens(tok, t) / len(t) for t in pure]
        print(f"  书中中文占比 >95% 的块：{len(pure)} 块，比率 中位 {statistics.median(rs):.3f}")
    sample = "深度学习是机器学习的一个分支，它通过多层神经网络从数据中自动学习特征表示。"
    print(f"  纯中文样例句：{len(sample)} 字 = {n_tokens(tok, sample)} token → {n_tokens(tok, sample)/len(sample):.3f} token 每字符")
    print(f"\n结论：纯中文 1 字 ≈ 1 token；混合文本的平均比率低于 1 是被英文/代码/数字拉低的，不能反推中文字符的 token 数。")


if __name__ == "__main__":
    main()
