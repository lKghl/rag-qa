import json
import re
import sys
from pathlib import Path

from core import ask, open_collection, search_info

DATA_PATH = Path(__file__).resolve().parent/"eval"/"qa_set.json"
RESULT_PATH = Path(__file__).resolve().parent/"eval"/"eval_results.md"

REFUSAL = "很抱歉，我没有相关内容的资料"
GREETING = "d2l知识库问答助手"
CITATION = "引用资料："

BOUNDARY_IDS = {"E14", "E30"}


def load_cases(only_ids):
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if only_ids:
        data = [c for c in data if c["id"] in only_ids]
    return data


def check_hit(retrieved, expect_sections):
    for prefix in expect_sections:
        for item in retrieved:
            if prefix in item:
                return True, prefix
    return False, ""


def check_behavior(answer, retrieved, behavior):
    if behavior == "answer":
        ok = CITATION in answer and len(retrieved) > 0
    elif behavior == "refuse":
        ok = REFUSAL in answer
    elif behavior == "greet":
        ok = GREETING in answer and len(retrieved) == 0
    elif behavior == "partial":
        ok = CITATION in answer and len(retrieved) > 0
    else:
        ok = False
    return ok


def extract_chunks(answer):
    return set(re.findall(r"资料(chunk_\d+)", answer))


def main():
    only_ids = set(sys.argv[1:])
    cases = load_cases(only_ids)
    if not cases:
        print("没有匹配的用例，检查传入的 ID")
        return

    print(f"共 {len(cases)} 条用例，将调用 {len(cases)} 次 DeepSeek API，开始...\n")

    results = {}
    rows = []
    boundary_rows = []
    hit_total = hit_pass = 0
    beh_total = beh_pass = 0
    collection = open_collection()

    for case in cases:
        cid = case["id"]
        print(f"运行 {cid} ...", flush=True)
        try:
            answer, retrieved = ask(case["q"])
        except Exception as e:
            print(f"  {cid} 运行出错：{e}")
            answer, retrieved = f"【运行出错】{e}", []
        results[cid] = {"answer": answer, "retrieved": retrieved}

        hit, hit_prefix = None, ""
        if "expect_sections" in case:
            _, raw_retrieved = search_info(collection, [case["q"]])
            hit, hit_prefix = check_hit(raw_retrieved, case["expect_sections"])

        beh = check_behavior(answer, retrieved, case["expect_behavior"])

        consist = ""
        if "match_citation_of" in case:
            other = results.get(case["match_citation_of"])
            if other:
                mine = extract_chunks(answer)
                theirs = extract_chunks(other["answer"])
                same = len(mine & theirs) > 0
                consist = f"引用一致性:{'✓' if same else '✗'} 本方{sorted(mine)} vs 对方{sorted(theirs)}"

        row = {"case": case, "answer": answer, "retrieved": retrieved,
               "hit": hit, "hit_prefix": hit_prefix, "beh": beh, "consist": consist}

        if cid in BOUNDARY_IDS:
            boundary_rows.append(row)
        else:
            rows.append(row)
            beh_total += 1
            beh_pass += int(beh)
            if "expect_sections" in case:
                hit_total += 1
                hit_pass += int(bool(hit))

        if hit is None:
            hit_str = "命中—"
        else:
            hit_str = f"命中{'✓' if hit else '✗'}({hit_prefix})"
        print(f"  {cid} [{case['type']}] 行为{'✓' if beh else '✗'} {hit_str} {consist}")

    print("\n========== 指标汇总 ==========")
    if only_ids:
        print(f"（注意：本次只跑了 {len(cases)} 条，下面是已跑部分的临时值，不是全量基线）")
    if beh_total:
        print(f"行为符合率：{beh_pass}/{beh_total}（契约内用例）")
    if hit_total:
        print(f"检索命中率：{hit_pass}/{hit_total}（有预期章节的契约内用例）")
    print("忠实度：人工指标——打开 eval/eval_results.md，逐条论断对引用块打勾")
    for row in boundary_rows:
        c = row["case"]
        if row["hit"] is None:
            hit_show = "—"
        else:
            hit_show = "✓" if row["hit"] else "✗"
        print(f"边界用例 {c['id']}（{c['q']}）：行为{'✓' if row['beh'] else '✗'} 命中{hit_show} —— 复合输入，只要求安全退化")

    lines = [
        "# 评测结果（供人工核查忠实度）",
        "",
        "核查方法：把每条答案的关键论断，逐条到它引用的块里找依据，打勾/打叉。",
        "",
    ]
    for row in rows + boundary_rows:
        c = row["case"]
        if row["hit"] is None:
            hit_show = "—"
        else:
            hit_show = "✓" if row["hit"] else "✗"
        lines.append(f"## {c['id']} [{c['type']}] {c['q']}")
        lines.append(f"判定：行为{'✓' if row['beh'] else '✗'} / 命中{hit_show} {row['consist']}")
        lines.append("")
        lines.append("**答案**：")
        lines.append(row["answer"])
        lines.append("")
        lines.append("**检索候选**：")
        for item in row["retrieved"]:
            lines.append(f"- {item}")
        lines.append("")
        lines.append("---")
        lines.append("")
    RESULT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n答案全文已写入 {RESULT_PATH}")


if __name__ == "__main__":
    main()
