# -*- coding: utf-8 -*-
"""reading_loader — 讀 openhing-project/Reading/ 每日一篇 .md → 轉 PASSAGES 格式
優先讀本地 clone（~/Desktop/openhing/Reading），冇就經 GitHub raw 下載。
"""
import os, re, glob, json

REPO = "chuckchanchi-cpu/openhing-project"
BRANCH = "main"
LOCAL_DIR = os.path.expanduser("~/Desktop/openhing/Reading")

SKILL_MAP = {"主旨": "main", "細節": "detail", "推論": "inference", "詞義": "vocab",
             "逆向": "not", "因果": "cause", "目的": "cause", "作者態度": "attitude", "深層意思": "attitude"}

def _fetch_texts():
    texts = {}
    # 1) 本地
    if os.path.isdir(LOCAL_DIR):
        for f in glob.glob(os.path.join(LOCAL_DIR, "*.md")):
            name = os.path.basename(f)
            if name.startswith(("README", "_")):
                continue
            try:
                texts[name] = open(f, encoding="utf-8").read()
            except Exception:
                pass
        if texts:
            return texts
    # 2) raw + index.txt（免 API 限速）
    try:
        import requests
        raw = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/Reading"
        idx = requests.get(f"{raw}/index.txt", timeout=15)
        if idx.status_code == 200:
            for name in idx.text.splitlines():
                name = name.strip()
                if not name.endswith(".md") or name.startswith(("README", "_")):
                    continue
                r = requests.get(f"{raw}/{name}", timeout=15)
                if r.status_code == 200:
                    texts[name] = r.text
        if texts:
            return texts
    except Exception:
        pass
    # 3) GitHub API fallback
    try:
        import requests
        r = requests.get(f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1", timeout=15)
        r.raise_for_status()
        for t in r.json().get("tree", []):
            p = t.get("path", "")
            if p.startswith("Reading/") and p.endswith(".md") and not os.path.basename(p).startswith(("README", "_")):
                raw = requests.get(f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{p}", timeout=15)
                if raw.status_code == 200:
                    texts[os.path.basename(p)] = raw.text
    except Exception:
        pass
    return texts

def parse_md(name, text):
    """一篇 .md → PASSAGES item"""
    m = re.search(r"^#\s*(\d{4}-\d{2}-\d{2})\s*每日一篇・(中文|英文)：(.+)$", text, re.M)
    if not m:
        return None
    date, lang, title = m.group(1), m.group(2), m.group(3).strip()
    am = re.search(r"## 文章\s*\n(.*?)\n##\s*閱讀理解", text, re.S)
    if not am:
        return None
    article = re.sub(r"^>.*$", "", am.group(1), flags=re.M).strip()
    qs = []
    for qm in re.finditer(r"###\s*Q(\d+)（([^）]+)）\s*\n(.*?)(?=\n###|\n---|\Z)", text, re.S):
        skill_raw, body = qm.group(2), qm.group(3)
        lines = [l.rstrip() for l in body.splitlines()]
        q_text, options, answer_letter = [], [], ""
        mode = "q"
        for l in lines:
            s = l.strip()
            om = re.match(r"^-\s*([A-D])\.\s*(.+)$", s)
            if om:
                mode = "o"
                options.append(om.group(2).strip())
                continue
            am2 = re.match(r"^\*\*答案：\*\*\s*([A-D])", s)
            if am2:
                answer_letter = am2.group(1)
                continue
            if s.startswith(("**文中依據", "**💡", "**⚠️", "**答案")):
                mode = "x"
                continue
            if mode == "q" and s:
                q_text.append(s)
        if not q_text or len(options) < 2 or not answer_letter:
            continue
        ans_idx = "ABCD".find(answer_letter)
        if not (0 <= ans_idx < len(options)):
            continue
        ind = re.search(r"\*\*文中依據：\*\*\s*(.+)", body)
        tip = re.search(r"\*\*💡[^\*]*：\*\*\s*(.+)", body)
        trap = re.search(r"\*\*⚠️[^\*]*：\*\*\s*(.+)", body)
        qs.append({
            "type": "mcq",
            "skill": SKILL_MAP.get(skill_raw.strip(), "detail"),
            "q": " ".join(q_text),
            "options": options,
            "answer": options[ans_idx],
            "hint": (ind.group(1).strip() if ind else "") + ("｜" + tip.group(1).strip() if tip else ""),
            "trap": trap.group(1).strip() if trap else "",
        })
    if not qs:
        return None
    return {"title": f"《{title}》— 每日一篇", "source": f"{date} Reading/{lang}（chuck 分享）",
            "article": article, "questions": qs}

def load_reading_passages(only_lang=None):
    out = []
    for name, text in sorted(_fetch_texts().items()):
        try:
            item = parse_md(name, text)
            if item and only_lang and f"Reading/{only_lang}" not in item["source"]:
                item = None
            if item:
                out.append(item)
        except Exception:
            continue
    return out

if __name__ == "__main__":
    ps = load_reading_passages(only_lang="英文")
    print(f"✅ 讀到 {len(ps)} 篇每日一篇：")
    for p in ps:
        print(f"  - {p['title']}｜{len(p['questions'])} 題")
