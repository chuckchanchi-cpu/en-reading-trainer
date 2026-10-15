# 📖 en-reading-trainer — 英文閱讀理解訓練（P.6 考試程度）

小六英文閱讀理解獨立訓練 app，題型完全照 P.6 評估卷考試程度：
**篇章 + 5 條 MCQ + 1 條 ONE-word 填詞**，每題附 **💡定位提示** 同 **⚠️陷阱分析**。

## 題型
| 題型 | 說明 |
|------|------|
| 🔎 細節理解 | 答案喺原文直接搵到 |
| 🚫 逆向題 | NOT mentioned — 逐項對原文排除 |
| 🧠 推論 | 由原文線索 + 常識推斷 |
| 📚 詞義 | 片語／生字按上下文解 |
| 🎯 主旨 | 段旨／要旨，覆蓋全段全文 |
| ✏️ ONE-word 填詞 | 文中詞語，限定一個英文字 |

## 功能
- **📖 題庫練習**：內置篇章題庫（含 2026-10-16 評估卷模範篇 + 原創同程度篇章）
- **✨ AI 生成新篇**：qwen3.8-flash 自動生成同程度新 passage + 題目（含提示同陷阱）
- **📊 題型弱點分析**：即場計分 + 邊類題型弱一目了然

## 執行
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 測試
```bash
python3 _smoke_test.py
```

## 配置（AI 模式）
Streamlit Cloud → Settings → Secrets：
```toml
OPENAI_API_KEY = "..."
OPENAI_MODEL_NAME = "qwen3.8-flash"
OPENAI_API_BASE = "https://api.silra.cn/v1"
```
