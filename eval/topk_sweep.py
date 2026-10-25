"""top_k 消融：检索命中率随 k 的变化，以及正确块的首次命中排名。

用法：python eval/topk_sweep.py
口径：
  - 契约内 18 条 = 20 条有预期章节的用例 - 2 条边界用例（E14/E30，复合输入，按设计不计分）
  - 命中 = 前 k 个候选里出现预期章节（走原始检索，不走界面出处）
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import model, open_collection  # noqa: E402

QA_SET = Path(__file__).resolve().parent / "qa_set.json"
BOUNDARY_IDS = {"E14", "E30"}
MAX_K = 15


def first_hit_rank(collection, question, expect_sections):
    emb = model.encode([question], normalize_embeddings=True).tolist()
    res = collection.query(query_embeddings=emb, n_results=MAX_K)
    metas = res["metadatas"][0]
    distances = res["distances"][0]
    for i, meta in enumerate(metas):
        if any(p in meta["heading"] for p in expect_sections):
            return i + 1, distances[0]
    return None, distances[0]


def main():
    cases = [c for c in json.loads(QA_SET.read_text(encoding="utf-8")) if "expect_sections" in c]
    collection = open_collection()

    rows = []
    for case in cases:
        rank, top1 = first_hit_rank(collection, case["q"], case["expect_sections"])
        rows.append({"id": case["id"], "q": case["q"], "rank": rank, "top1": top1,
                     "boundary": case["id"] in BOUNDARY_IDS})

    print("=== 首次命中排名 ===")
    for r in rows:
        mark = "（边界）" if r["boundary"] else ""
        print(f"{r['id']:4} 排名={r['rank'] if r['rank'] else '>' + str(MAX_K):>3}  top1距离={r['top1']:.4f}  {r['q']}{mark}")

    print("\n=== 命中率 vs k ===")
    print(f"{'k':>3} {'契约内18条':>12} {'全量20条':>10}")
    for k in (1, 3, 5, 8, 10, 15):
        inner = [r for r in rows if not r["boundary"]]
        hi = sum(1 for r in inner if r["rank"] and r["rank"] <= k)
        ha = sum(1 for r in rows if r["rank"] and r["rank"] <= k)
        print(f"{k:>3} {hi:>7}/{len(inner)} {hi/len(inner)*100:>4.0f}% {ha:>5}/{len(rows)} {ha/len(rows)*100:>4.0f}%")

    print("\n=== 排名分布 ===")
    for rank, n in sorted(Counter(r["rank"] or 99 for r in rows).items()):
        print(f"  排名 {'>'+str(MAX_K) if rank == 99 else rank}: {n} 条")

    print("\n=== 例外 ===")
    for r in rows:
        if r["rank"] is None or r["rank"] > 5:
            print(f"  {r['id']} 排名={r['rank']} top1距离={r['top1']:.4f} {r['q']}")


if __name__ == "__main__":
    main()
