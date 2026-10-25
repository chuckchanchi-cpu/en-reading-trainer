#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📖 English Reading Comprehension Trainer — 英文閱讀理解訓練（P.6 考試程度）

題型完全照 P.6 評估卷：
  5 條 MCQ（細節 / NOT mentioned 逆向 / 推論 / 詞義 / 主旨）+ 1 條 ONE-word 填詞
每題附：
  💡 提示（定位技巧：點搵答案）
  ⚠️ 陷阱（干擾項分析：點解會中伏）
兩種模式：
  📖 題庫練習 — 內置 passage 題庫（100% 預定題目，即時）
  ✨ AI 生成新篇 — qwen3.8-flash 生成同程度全新 passage + 題目
"""

import os
import json
import re
import random
import requests
import streamlit as st

from passages import PASSAGES

st.set_page_config(page_title="📖 英文閱讀理解訓練", page_icon="📖", layout="wide")

# 將 Streamlit Secrets 注入環境變數（每個 page 獨立執行，要自己注入！）
if hasattr(st, "secrets") and len(st.secrets) > 0:
    for k in st.secrets.keys():
        os.environ[k] = str(st.secrets[k])

# ===== API 配置（env-first，兼容 OPENAI_* / SILRA_*）=====
def get_api_config():
    base = os.environ.get("OPENAI_API_BASE", "").rstrip("/")
    key = os.environ.get("OPENAI_API_KEY", "") or os.environ.get("SILRA_API_KEY", "")
    model = os.environ.get("OPENAI_MODEL_NAME", "") or os.environ.get("MODEL_NAME", "qwen3.8-flash")
    if not base:
        silra_url = os.environ.get("SILRA_API_URL", "")
        if silra_url:
            base = silra_url.replace("/chat/completions", "").rstrip("/")
    if not base:
        base = "https://api.silra.cn/v1"
    return base, key, model

SKILL_LABEL = {
    "detail": "🔎 細節理解",
    "not-mentioned": "🚫 逆向題（NOT mentioned）",
    "inference": "🧠 推論",
    "vocabulary": "📚 詞義",
    "main-idea": "🎯 主旨",
    "cloze": "✏️ ONE-word 填詞",
}

def norm_answer(s):
    """寬鬆比對：去首尾空格、小寫、去標點"""
    if s is None:
        return ""
    s = s.strip().lower()
    s = re.sub(r"[.,!?;:'\"()]", "", s)
    return s.strip()

def grade_cloze(user, answer):
    alts = [a.strip() for a in re.split(r"\s*/\s*", answer)]
    return norm_answer(user) in [norm_answer(a) for a in alts] and norm_answer(user) != ""

def _match_option(ans, opts):
    """模糊比對答案同選項：正規化後完全一致優先，再退包含式比對（容忍標點/大小寫/首尾差異）"""
    na = norm_answer(ans)
    if not na:
        return None
    for o in opts:
        if norm_answer(o) == na:
            return o
    for o in opts:
        no = norm_answer(o)
        if no and (na in no or no in na):
            return o
    return None

def validate_questions(questions):
    """過濾唔合格題目；回傳 (valid, rejected_count)"""
    valid = []
    for q in questions:
        t = q.get("type")
        if t == "mcq":
            opts = [str(o).strip() for o in q.get("options", []) if str(o).strip()]
            ans = str(q.get("answer", "")).strip()
            matched = _match_option(ans, opts)
            if len(opts) == 4 and matched and q.get("q"):
                q["options"], q["answer"] = opts, matched
                valid.append(q)
        elif t == "cloze":
            ans = str(q.get("answer", "")).strip()
            if ans and len(ans.split()) <= 3 and q.get("q"):
                valid.append(q)
    return valid

def ai_generate(topic):
    api_base, api_key, model = get_api_config()
    if not api_key:
        st.error("⚠️ 未偵測到 API key — 請設定 OPENAI_API_KEY（app Settings → Secrets）")
        return None
    prompt = (
        "你是小六英文閱讀理解出題老師，出一份香港小六考試程度（P.6）嘅閱讀理解練習。\n"
        f"主題：{topic}（如果主題空白，就自選一個小六常見題材：環保、動物、健康、科技、校園生活）\n"
        "要求：\n"
        "1. 文章 250-350 英文詞，正式考試風格，段落清晰，適合小六學生。\n"
        "2. 出 6 題：5 條四選一 MCQ + 1 條 ONE-word 填詞。\n"
        "3. MCQ 題型必須包括：detail（細節）、not-mentioned（逆向：NOT mentioned）、inference（推論）、"
        "vocabulary（詞義）、main-idea（主旨）各一題。\n"
        "4. 干擾項要接近同似是而非（同範疇、常見混淆），唔可以太易排除。\n"
        "5. 每題要有 hint（中文書面語，講定位技巧）同 trap（中文書面語，講干擾項點解錯、常見陷阱）。\n"
        "6. 填詞題答案必須係文章中出現過嘅一個英文字。\n"
        "只回 JSON，格式：\n"
        '{"title":"...","article":"...","questions":['
        '{"type":"mcq","skill":"detail","q":"...","options":["...","...","...","..."],"answer":"...","hint":"...","trap":"..."},'
        '{"type":"cloze","skill":"cloze","q":"...","answer":"...","hint":"...","trap":"..."}]}'
    )
    try:
        resp = requests.post(
            f"{api_base}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 3000,
            },
            timeout=90,
        )
    except Exception as e:
        st.error(f"❌ 網絡/API 連接出錯：{e}")
        return None
    # 先檢查 HTTP 狀態同回應格式 — 非 JSON 回應多數係 key 無效/endpoint 唔啱
    try:
        content = resp.json()["choices"][0]["message"]["content"]
    except Exception:
        body = (resp.text or "").strip()[:200]
        st.error(f"❌ API 回應格式錯誤（HTTP {resp.status_code}）：{body or '（空回應）'}")
        st.caption("💡 常見原因：①API key 無效或已過期（檢查 Settings → Secrets 嘅 OPENAI_API_KEY）②API 地址或模型名稱唔啱 ③服務暫時過載")
        return None
    # 清理 ```json fences
    m = re.search(r"\{.*\}", content, re.S)
    if not m:
        st.error("❌ AI 回覆搵唔到 JSON — 再試一次？")
        return None
    try:
        data = json.loads(m.group(0))
    except Exception:
        st.error("❌ AI JSON 解析失敗 — 再試一次？")
        return None
    qs = validate_questions(data.get("questions", []))
    if len(qs) < 4:
        st.error("❌ AI 生成嘅題目唔夠合格數量 — 再試一次？")
        return None
    return {"title": data.get("title", "AI Generated Passage"), "source": "✨ AI 生成（qwen3.8-flash）",
            "article": data.get("article", ""), "questions": qs}

def ai_generate_from_article(article):
    """📥 仿寫：輸入原文 → 分析程度 → 生成同程度全新文章 + 題目"""
    api_base, api_key, model = get_api_config()
    if not api_key:
        st.error("⚠️ 未偵測到 API key — 請設定 OPENAI_API_KEY（app Settings → Secrets）")
        return None
    prompt = f"""你是小六英文閱讀理解出題老師。以下是學生用過嘅一篇閱讀理解原文。
請先分析原文嘅程度（詞彙難度、句式、文章長度、主題），然後生成一篇「同程度」嘅全新文章（內容唔同、唔可以抄原文，但題材相近、難度一致），再出 6 題。

【原文】
{article}

要求：
1. 新文章 250-350 英文詞，程度同原文一致，題材相近但內容全新。
2. 出 6 題：5 條四選一 MCQ + 1 條 ONE-word 填詞。
3. MCQ 題型必須包括：detail（細節）、not-mentioned（逆向：NOT mentioned）、inference（推論）、vocabulary（詞義）、main-idea（主旨）各一題。
4. 干擾項要接近同似是而非（同範疇、常見混淆），唔可以太易排除。
5. 每題要有 hint（中文書面語，講定位技巧）同 trap（中文書面語，講干擾項點解錯、常見陷阱）。
6. 填詞題答案必須係文章中出現過嘅一個英文字。
只回 JSON，格式：
{{"title":"...","article":"...","questions":[{{"type":"mcq","skill":"detail","q":"...","options":["...","...","...","..."],"answer":"...","hint":"...","trap":"..."}},{{"type":"cloze","skill":"cloze","q":"...","answer":"...","hint":"...","trap":"..."}}]}}"""
    try:
        resp = requests.post(
            f"{api_base}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.7, "max_tokens": 3000},
            timeout=90,
        )
        content = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"❌ API 出錯：{e}")
        return None
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end <= start:
        st.error("❌ AI 回覆搵唔到 JSON — 再試一次？")
        return None
    try:
        data = json.loads(content[start:end + 1])
    except Exception:
        st.error("❌ AI JSON 解析失敗 — 再試一次？")
        return None
    qs = validate_questions(data.get("questions", []))
    if len(qs) < 4:
        st.error("❌ AI 生成嘅題目唔夠合格數量 — 再試一次？")
        return None
    return {"title": data.get("title", "AI Generated Passage"), "source": "📥 AI 仿寫（同程度新篇）",
            "article": data.get("article", ""), "questions": qs}


def build_quiz(passage):
    qs = []
    for q in passage["questions"]:
        item = dict(q)
        if item["type"] == "mcq":
            item["options"] = random.sample(item["options"], len(item["options"]))
        qs.append(item)
    return {"title": passage["title"], "source": passage.get("source", ""), "article": passage["article"], "questions": qs}

# ===== Session state =====
if "rd_quiz" not in st.session_state:
    st.session_state.rd_quiz = None
if "rd_checked" not in st.session_state:
    st.session_state.rd_checked = False

# ===== Sidebar =====
with st.sidebar:
    st.header("⚙️ 設定")
    mode = st.radio("生成模式", ["📖 題庫練習（即時）", "✨ AI 生成新篇（自訂主題）", "📥 AI 仿寫（輸入原文）"], key="rd_mode")
    if mode.startswith("📖"):
        pmap = {f"{p['title']}（{p['source']}）": p for p in PASSAGES}
        choice = st.selectbox("揀篇章", list(pmap.keys()), key="rd_pick")
        if st.button("🎲 開始練習", type="primary", use_container_width=True):
            st.session_state.rd_quiz = build_quiz(pmap[choice])
            st.session_state.rd_checked = False
            st.rerun()
    elif mode.startswith("✨"):
        topic = st.text_input("主題（可留空自動揀）", placeholder="例如：海洋保育、太空旅行…", key="rd_topic")
        if st.button("✨ 生成新篇章", type="primary", use_container_width=True):
            with st.spinner("✨ AI 生成緊篇章同題目…（約 10–30 秒）"):
                p = ai_generate(topic.strip() or "")
            if p:
                st.session_state.rd_quiz = build_quiz(p)
                st.session_state.rd_checked = False
                st.rerun()
    else:
        article = st.text_area("貼上原文（AI 分析程度 → 生成同程度新篇）", placeholder="貼上考試卷嘅閱讀理解原文…", height=200, key="rd_article")
        if st.button("📥 生成同程度新篇", type="primary", use_container_width=True):
            if not article.strip():
                st.warning("⚠️ 請先貼上原文")
            else:
                with st.spinner("📥 AI 分析程度 + 生成同程度新篇…（約 20–40 秒）"):
                    p = ai_generate_from_article(article.strip())
                if p:
                    st.session_state.rd_quiz = build_quiz(p)
                    st.session_state.rd_checked = False
                    st.rerun()
    st.divider()
    st.caption("題型：細節 / 逆向 / 推論 / 詞義 / 主旨 / ONE-word 填詞\n每題附 💡提示 + ⚠️陷阱")

# ===== 主頁 =====
st.title("📖 英文閱讀理解訓練")
st.caption("小六考試程度（P.6）— 篇章 + MCQ + ONE-word 填詞，每題附定位提示同陷阱分析。")

quiz = st.session_state.rd_quiz
if not quiz:
    st.info("👈 左邊 sidebar：揀篇章或者用 AI 生成新篇開始！")
    st.markdown("**📚 內置題庫：**")
    for p in PASSAGES:
        n_mc = sum(1 for q in p["questions"] if q["type"] == "mcq")
        n_cl = sum(1 for q in p["questions"] if q["type"] == "cloze")
        st.markdown(f"- **{p['title']}**（{p['source']}）— {n_mc} MCQ + {n_cl} 填詞")
    st.stop()

st.subheader(f"📄 {quiz['title']}")
if quiz.get("source"):
    st.caption(quiz["source"])
with st.container(border=True):
    for para in quiz["article"].split("\n\n"):
        st.markdown(para)

st.divider()
st.subheader(f"📝 題目（{len(quiz['questions'])} 題）")

for i, q in enumerate(quiz["questions"]):
    skill = SKILL_LABEL.get(q.get("skill", ""), "")
    st.markdown(f"**{i + 1}.** {q['q']}　`{skill}`")
    if q["type"] == "mcq":
        st.radio(" ", q["options"], key=f"rd_a{i}", index=None, label_visibility="collapsed")
    else:
        st.text_input(" ", key=f"rd_a{i}", placeholder="輸入 ONE word（一個英文字）", label_visibility="collapsed")

c1, c2, _ = st.columns([1, 1, 3])
if not st.session_state.rd_checked:
    if c1.button("✅ 檢查答案", type="primary"):
        st.session_state.rd_checked = True
        st.rerun()
else:
    correct = 0
    skill_stat = {}
    for i, q in enumerate(quiz["questions"]):
        user = st.session_state.get(f"rd_a{i}")
        if q["type"] == "mcq":
            ok = (user == q["answer"])
        else:
            ok = grade_cloze(user, q["answer"])
        skill = q.get("skill", "other")
        d = skill_stat.setdefault(skill, [0, 0])
        d[1] += 1
        if ok:
            d[0] += 1
            correct += 1
        st.markdown(f"**{i + 1}.** {q['q']}")
        if ok:
            st.success(f"✅ 正確！你答：「{user}」")
        else:
            shown = user if user else "（未作答）"
            st.error(f"❌ 你答：「{shown}」　正確答案：**{q['answer']}**")
        st.markdown(f"💡 {q['hint']}")
        st.markdown(f"⚠️ {q['trap']}")
        st.markdown("---")

    st.metric("🏆 得分", f"{correct} / {len(quiz['questions'])}")
    st.subheader("📊 題型弱點分析")
    for skill, (c, t) in skill_stat.items():
        emoji = "✅" if c == t else ("⚠️" if c * 2 >= t else "❌")
        st.markdown(f"{emoji} {SKILL_LABEL.get(skill, skill)}：{c}/{t}")

if c2.button("🔄 再嚟一篇", use_container_width=True):
    if st.session_state.rd_mode.startswith("📖"):
        pmap = {f"{p['title']}（{p['source']}）": p for p in PASSAGES}
        choice = st.session_state.get("rd_pick")
        if choice in pmap:
            st.session_state.rd_quiz = build_quiz(pmap[choice])
            st.session_state.rd_checked = False
            st.rerun()
    elif st.session_state.rd_mode.startswith("✨"):
        with st.spinner("✨ AI 生成緊…"):
            p = ai_generate(st.session_state.get("rd_topic", "") or "")
        if p:
            st.session_state.rd_quiz = build_quiz(p)
            st.session_state.rd_checked = False
            st.rerun()
    else:
        article = st.session_state.get("rd_article", "") or ""
        if not article.strip():
            st.error("⚠️ 未有原文可仿寫")
        else:
            with st.spinner("📥 AI 仿寫緊…"):
                p = ai_generate_from_article(article.strip())
            if p:
                st.session_state.rd_quiz = build_quiz(p)
                st.session_state.rd_checked = False
                st.rerun()
