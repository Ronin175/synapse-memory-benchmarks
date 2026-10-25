"""Recompute the README's tables from the published results files.

    python3 scripts/score.py results/2026-10-23_synapse-0.1.5_gpt-oss-20b.jsonl

Standard library only. Categories use LoCoMo's dataset codes.
"""
import json
import sys
from collections import defaultdict

NAMES = {4: "Single-hop", 2: "Temporal", 1: "Multi-hop", 3: "Open-domain / reasoning"}


def pct(xs):
    return f"{100 * sum(xs) / len(xs):5.1f}%" if xs else "  n/a"


def main(path):
    rows = [json.loads(line) for line in open(path, encoding="utf-8")]
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        for key in (int(r["category"]), "all"):
            b = by[key]
            b["strict"].append(r["judge_strict"] == "CORRECT")
            if "judge_lenient" in r:
                b["lenient"].append(r["judge_lenient"] == "CORRECT")
            if r.get("f1_official") is not None:
                b["f1"].append(float(r["f1_official"]))
            if r.get("evidence_recall") is not None:
                b["ev"].append(float(r["evidence_recall"]))
    print(f"{path}: {len(rows)} questions")
    print(f"{'Category':26s} {'n':>5s} {'J strict':>9s} {'J lenient':>10s} {'F1':>7s} {'Evidence':>9s}")
    for key, name in list(NAMES.items()) + [("all", "Overall")]:
        b = by[key]
        print(f"{name:26s} {len(b['strict']):5d} {pct(b['strict']):>9s} {pct(b['lenient']):>10s} "
              f"{pct(b['f1']):>7s} {pct(b['ev']):>9s}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
        print()
