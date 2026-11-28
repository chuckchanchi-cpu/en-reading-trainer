# -*- coding: utf-8 -*-
"""vocab_loader — 讀 vocab/*.md 生字庫 → 溫習卡／訓練題

格式（每詞一塊）：
    ### 詞
    - 解釋：...
    - 例句：...

設計：
  * 唯讀 .md，唔改內容（內容由隊友維護）
  * 填充題由例句自動挖空（答案位置替換成 ____）
  * MC 干擾項從同庫其他詞抽，保證同語言、同範疇
"""
import os
import random
import re

_H = re.compile(r"^###\s+(.+?)\s*$")
_EXP = re.compile(r"^[-*]\s*解釋\s*[：:]\s*(.+)$")
_EX = re.compile(r"^[-*]\s*例句\s*[：:]\s*(.+)$")
_GRP = re.compile(r"^##\s+(.+?)\s*$")


def _dirs():
    base = os.path.dirname(os.path.abspath(__file__))
    return [os.path.join(base, "vocab"), os.path.join(base, "Vocab")]


def parse_md(text, lang="zh"):
    """→ [{'word','explain','example','group','lang'}]"""
    out = []
    group = ""
    cur = None
    for ln in text.splitlines():
        g = _GRP.match(ln)
        if g:
            group = g.group(1).strip()
            continue
        h = _H.match(ln)
        if h:
            if cur and cur.get("word"):
                out.append(cur)
            cur = {"word": h.group(1).strip(), "explain": "", "example": "",
                   "group": group, "lang": lang}
            continue
        if cur is None:
            continue
        m = _EXP.match(ln.strip())
        if m:
            cur["explain"] = m.group(1).strip()
            continue
        m = _EX.match(ln.strip())
        if m:
            cur["example"] = m.group(1).strip()
    if cur and cur.get("word"):
        out.append(cur)
    return [w for w in out if w["word"] and w["explain"]]


def load_vocab(lang="zh"):
    """讀本地 vocab/ 資料夾"""
    out = []
    for d in _dirs():
        if not os.path.isdir(d):
            continue
        want = ("zh", "en")
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md") or fn.startswith(("_", "README")):
                continue
            prefix = fn[:2].lower()
            if prefix not in want:
                continue
            if prefix != lang:
                continue
            try:
                txt = open(os.path.join(d, fn), encoding="utf-8").read()
            except Exception:
                continue
            out.extend(parse_md(txt, lang=prefix))
    # 同一個詞可能出現多次（唔同詞義）→ 合併，唔好丟棄
    order, merged = [], {}
    for w in out:
        k = w["word"]
        if k not in merged:
            merged[k] = dict(w)
            order.append(k)
            continue
        prev = merged[k]
        # 合併解釋（去重）
        parts = [x.strip() for x in prev["explain"].split("；") if x.strip()]
        for alt in w["explain"].split("；"):
            alt = alt.strip()
            if alt and alt not in parts:
                parts.append(alt)
        prev["explain"] = "；".join(parts)
        # 例句合併（示範唔同用法）
        if w["example"] and w["example"] not in prev["example"]:
            prev["example"] = (prev["example"] + " ／ " + w["example"]).strip(" ／")
    return [merged[k] for k in order]


# ─────────────────── 出題 ───────────────────
def _mask(word, example, lang):
    """由例句挖空該詞，返回 (題目字串, 是否成功)"""
    if not example:
        return "", False
    # 英文：大小寫不敏感 + 詞形變化（+s/es/ed/ing）
    if lang == "en":
        stem = re.escape(word)
        pat = re.compile(rf"\b{stem}(s|es|ed|ing|d)?\b", re.I)
        if pat.search(example):
            return pat.sub("________", example, count=1), True
        return "", False
    # 中文：直接取代
    if word in example:
        return example.replace(word, "________", 1), True
    return "", False


def build_fill(items, n=10, rng=None):
    """填充題：例句挖空＋解釋提示"""
    rng = rng or random.Random()
    pool = []
    for w in items:
        q, ok = _mask(w["word"], w["example"], w["lang"])
        if ok:
            pool.append({
                "type": "fill",
                "q": q,
                "answer": w["word"],
                "hint": w["explain"],
                "word": w["word"],
                "group": w["group"],
            })
    rng.shuffle(pool)
    return pool[:n]


def build_mc(items, n=10, rng=None):
    """MC：問詞義，干擾項由同庫抽（同長度優先）"""
    rng = rng or random.Random()
    if len(items) < 4:
        return []
    pool = []
    for w in items:
        others = [o for o in items if o["word"] != w["word"]]
        if len(others) < 3:
            continue
        # 干擾項：解釋長度接近優先，避免一眼看出
        others.sort(key=lambda o: abs(len(o["explain"]) - len(w["explain"])))
        cand = others[:6]
        picks = rng.sample(cand, 3)
        opts = [w["explain"]] + [p["explain"] for p in picks]
        rng.shuffle(opts)
        pool.append({
            "type": "mc",
            "q": f"「{w['word']}」的意思是：",
            "options": opts,
            "answer": w["explain"],
            "word": w["word"],
            "group": w["group"],
        })
    rng.shuffle(pool)
    return pool[:n]


def build_word_mc(items, n=10, rng=None):
    """MC：給解釋，選正確的詞（反向）"""
    rng = rng or random.Random()
    if len(items) < 4:
        return []
    pool = []
    for w in items:
        others = [o for o in items if o["word"] != w["word"]]
        picks = rng.sample(others, 3)
        opts = [w["word"]] + [p["word"] for p in picks]
        rng.shuffle(opts)
        pool.append({
            "type": "mc",
            "q": f"以下哪一個詞的意思是「{w['explain']}」？",
            "options": opts,
            "answer": w["word"],
            "word": w["word"],
            "group": w["group"],
        })
    rng.shuffle(pool)
    return pool[:n]
