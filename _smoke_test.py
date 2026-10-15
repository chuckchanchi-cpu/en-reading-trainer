#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_smoke_test.py — en-reading-trainer 冒煙測試"""
import ast
import sys

fail = 0

# 1. 語法檢查
for f in ("app.py", "passages.py"):
    try:
        ast.parse(open(f, encoding="utf-8").read())
        print(f"✅ {f} syntax OK")
    except SyntaxError as e:
        print(f"❌ {f} syntax error: {e}")
        fail += 1

# 2. 題庫驗證
from passages import PASSAGES

if len(PASSAGES) < 4:
    print(f"❌ passages 只有 {len(PASSAGES)} 篇（至少 4 篇）")
    fail += 1

for p in PASSAGES:
    qs = p["questions"]
    n_mc = sum(1 for q in qs if q["type"] == "mcq")
    n_cl = sum(1 for q in qs if q["type"] == "cloze")
    problems = []
    if n_mc != 5:
        problems.append(f"MCQ 數量 {n_mc} ≠ 5")
    if n_cl != 1:
        problems.append(f"cloze 數量 {n_cl} ≠ 1")
    for q in qs:
        if not q.get("hint"):
            problems.append(f"「{q['q'][:20]}…」缺 hint")
        if not q.get("trap"):
            problems.append(f"「{q['q'][:20]}…」缺 trap")
        if q["type"] == "mcq":
            if len(q["options"]) != 4:
                problems.append(f"「{q['q'][:20]}…」選項 {len(q['options'])} ≠ 4")
            if q["answer"] not in q["options"]:
                problems.append(f"「{q['q'][:20]}…」答案唔喺選項入面")
        elif q["type"] == "cloze":
            if len(q["answer"].split()) > 2:
                problems.append(f"「{q['q'][:20]}…」cloze 答案唔係一個字")
    mcq_skills = {q.get("skill") for q in qs if q["type"] == "mcq"}
    # 必須包括逆向題 + 推論題，且至少 3 種 MCQ 題型
    if "not-mentioned" not in mcq_skills:
        problems.append("缺逆向題（not-mentioned）")
    if "inference" not in mcq_skills:
        problems.append("缺推論題（inference）")
    if len(mcq_skills) < 3:
        problems.append(f"MCQ 題型只得 {len(mcq_skills)} 種（至少 3 種）")
    if problems:
        fail += 1
        print(f"❌ {p['id']}: " + "; ".join(problems))
    else:
        print(f"✅ {p['id']}（{p['title']}）: {n_mc} MCQ + {n_cl} cloze, 題型齊全, hint/trap 全備")

print("done" if fail == 0 else f"FAILED ({fail})")
sys.exit(1 if fail else 0)
