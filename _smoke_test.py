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

# 2. 題庫驗證（內置已清空，改用每日篇）
from passages import PASSAGES


# 每日一篇檢查
from reading_loader import load_reading_passages
lang = "中文" if "zh" in __file__ else "英文"
d = load_reading_passages(only_lang=lang)
assert d, "每日一篇讀唔到"
for p_ in d:
    assert len(p_["questions"]) == 8, p_["title"]
print(f"✅ 每日一篇 {len(d)} 篇 × 8 題 OK")

print("done" if fail == 0 else f"FAILED ({fail})")
sys.exit(1 if fail else 0)


