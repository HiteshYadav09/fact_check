# 🔍 AI Fact Checker

> An AI-powered misinformation detection platform that verifies claims in real time using web search and large language model analysis.

---

## 🌟 Overview

AI Fact Checker is a professional-grade web application that helps users verify claims, detect misinformation, and analyze online news or statements. It combines real-time web search (Tavily) with advanced AI reasoning (OpenAI GPT-4o-mini) to deliver structured, evidence-based verdicts.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Real-time Search | Uses Tavily API to search the web for up-to-date evidence |
| 🤖 AI Analysis | GPT-4o-mini analyzes evidence against the claim |
| 🏷️ Verdict System | 6 verdict types: TRUE, FALSE, MISLEADING, PARTIALLY TRUE, UNVERIFIED, SATIRE |
| 📊 Confidence Score | 0–100% confidence rating with color coding |
| 🧠 Reasoning Chain | Step-by-step AI reasoning transparency |
| 🌐 Source Cards | Clickable source links with titles and snippets |
| 📜 History | Session-based check history in the sidebar |
| ⬇️ Download | Export full verification report as a .txt file |
| 🎨 Dark UI | Modern dark theme with animated verdict cards |

---

## 🏗️ Project Structure

```
fact-checker-app/
│
├── app.py            # Main Streamlit UI application
├── verifier.py       # Core orchestration: search → AI → result
├── search.py         # Tavily API integration
├── prompts.py        # OpenAI prompt engineering
├── requirements.txt  # Python dependencies
├── .env.example      # API key template
└── README.md         # This file
```

---

## ⚙️ Installation

### 1. Clone or download the project

```bash
git clone https://github.com/yourusername/ai-fact-checker.git
cd ai-fact-checker
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up API keys

```bash
cp .env.example .env
```

Then open `.env` and fill in your keys:

```env
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

---

## 🔑 API Setup

### OpenAI API Key
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new secret key
3. Paste it into `.env` as `OPENAI_API_KEY`
4. Ensure you have credits / a paid plan

### Tavily Search API Key
1. Go to [https://app.tavily.com/](https://app.tavily.com/)
2. Sign up for a free account (1,000 free searches/month)
3. Copy your API key
4. Paste it into `.env` as `TAVILY_API_KEY`

---

## 🚀 Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🎯 How It Works

```
User enters claim
       ↓
Tavily searches web (up to 8 sources)
       ↓
Evidence collected and formatted
       ↓
OpenAI GPT-4o-mini analyzes claim vs. evidence
       ↓
Structured JSON verdict returned
       ↓
Results displayed with verdict card, evidence, sources
```

---

## 🏷️ Verdict Types

| Verdict | Meaning | Color |
|---|---|---|
| ✅ TRUE | Accurately supported by evidence | Green |
| ❌ FALSE | Demonstrably incorrect | Red |
| ⚠️ MISLEADING | True but deceptively framed | Orange |
| 🔶 PARTIALLY TRUE | Some correct, some wrong | Yellow |
| ❓ UNVERIFIED | Insufficient evidence | Gray |
| 🎭 SATIRE | From a satirical source | Purple |

---

## ☁️ Deployment

### Streamlit Cloud (Recommended)
1. Push your code to GitHub (exclude `.env`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add secrets in **Settings → Secrets**:
   ```toml
   OPENAI_API_KEY = "sk-..."
   TAVILY_API_KEY = "tvly-..."
   ```

### Render / Railway
- Set environment variables in the dashboard
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

---

## 🔮 Future Improvements

- [ ] Multi-language claim support
- [ ] Image/screenshot fact-checking
- [ ] Shareable result links
- [ ] Browser extension
- [ ] Batch CSV upload for multiple claims
- [ ] Saved history with local database
- [ ] Claim source credibility scoring

---

## 📸 Screenshots

*Add screenshots of the app here after running it locally.*

---

## 📄 License

MIT License — free to use and modify.

---

*Built as a Product Management Trainee assessment project demonstrating AI integration, API orchestration, and professional UI/UX design.*
