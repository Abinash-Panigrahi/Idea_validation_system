# 🚀 ThynxAI Idea Lab — Startup Idea Validator

An AI-powered system that analyzes startup ideas and generates detailed evaluation reports using Google Gemini AI.

---

## 📌 What it Does

1. Takes a startup idea as input
2. Collects detailed founder information through a conversational chat interface
3. Generates intelligent adaptive follow-up questions based on the idea and founder profile
4. Analyzes the idea across 8 structured dimensions
5. Shows detailed problem statement with pain points, real world examples and market size
6. Shows detailed proposed solution with step by step breakdown and key features
7. Generates AI powered MVP and Investment readiness roadmap if not ready
8. Generates a detailed evaluation report (JSON + Markdown)
9. Fetches real-time market data, competitors and industry trends via web search

---

## 🧩 Project Structure

```
Idea_validation_system/
├── prompts.py          # All AI prompt functions
├── analyzer.py         # Gemini API integration
├── report.py           # JSON + Markdown report generation
├── main.py             # CLI interface
├── app.py              # Streamlit web interface
├── database.py         # MongoDB Atlas integration
├── websearch.py        # Tavily real-time web search integration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── samples/            # Sample input and output files
│   ├── sample_input.md
│   └── sample_output/
│       ├── analysis.json
│       └── report.md
└── outputs/            # Generated reports (auto-created)
    ├── analysis.json
    └── report.md
```

---

## 📥 Prerequisites

Before starting, make sure you have these installed:

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.8 or above | https://www.python.org/downloads/ |
| Git | Latest | https://git-scm.com/downloads |
| VS Code (recommended) | Latest | https://code.visualstudio.com/ |

After installing Python, verify in terminal:

```bash
python --version
pip --version
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Idea_validation_system.git
cd Idea_validation_system
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

```bash
# Windows (PowerShell):
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies

All required libraries are in `requirements.txt`:

| Library | Purpose |
|---------|---------|
| `google-generativeai` | Gemini AI API |
| `python-dotenv` | Environment variables |
| `streamlit` | Web UI |
| `pymongo[srv]` | MongoDB Atlas connection |
| `tavily-python` | Real-time web search |

```bash
pip install -r requirements.txt
```

---


### 5. Set Up Environment Variables

```bash
# Copy the example file:
cp .env.example .env
```

### 6. Get Gemini API Key
1. Go to: https://aistudio.google.com
2. Click "Get API Key"
3. Copy and paste into `.env` file:

```
GEMINI_API_KEY=your-actual-gemini-key-here
```

### 7. Set Up MongoDB Atlas
1. Create free account at https://www.mongodb.com/cloud/atlas/register
2. Create a free cluster (M0) — select FREE tier only!
3. Create a database user — ⚠️ save username and password immediately!
4. Allow network access from anywhere (0.0.0.0/0)
5. Copy connection string — ⚠️ password will not be shown again after this screen!
6. Add to `.env`:

```
MONGO_URI=your-mongodb-connection-string-here
```

### 8. Get Tavily API Key
1. Go to: https://app.tavily.com
2. Sign up and copy your API key
3. Add to `.env`:
```
TAVILY_API_KEY=your-actual-tavily-key-here
```

---

## 🚀 How to Run

### Option 1 — CLI (Terminal)

```bash
python main.py
```

### Option 2 — Web UI (Streamlit)

```bash
streamlit run app.py
```

### Option 3 — Live Demo

🌐 [Try it here](https://ideavalidationsystem-eyvfi388xtmk5shgmggxt7.streamlit.app/)

---

## 📊 Analysis Output

After running, the system generates:

- `outputs/analysis.json` → Structured JSON data
- `outputs/report.md` → Human-readable Markdown report

### 8 Analysis Sections:
1. Problem Statement (description, pain points, real world example, market size, current workarounds)
2. Proposed Solution (one line pitch, simple explanation, step by step, key features, unfair advantage)
3. Core Innovation
4. Market Landscape
5. Scores (1-10) with reasoning
6. Support Required
7. Tech Stack Suggestion
8. Overall Verdict (MVP/Investment/Incubator ready + AI roadmap if not ready)

---

## 🛠️ Tech Stack

- **Language:** Python
- **AI:** Google Gemini API (gemini-2.5-flash)
- **UI:** Streamlit
- **Database:** MongoDB Atlas
- **Web Search:** Tavily API (real-time market data)
- **Output:** JSON + Markdown

---

## 🤖 API Usage

- Normal flow: 8 Gemini API calls + 1 Tavily search
- Worst case (retries + help pages): 14 Gemini API calls
- MVP and Investment tips are cached — no extra calls if revisited
- Tavily search runs once after Step 2 and is reused across all steps

---

## 🗂️ Sample Input/Output

See the `samples/` folder for:
- Example startup idea input → `samples/sample_input.md`
- Example JSON output → `samples/sample_output/analysis.json`
- Example Markdown report → `samples/sample_output/report.md`

---

## ❌ Environment Variables

Never commit your `.env` file!
Use `.env.example` as template only.

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key |
| `MONGO_URI` | Your MongoDB Atlas connection string |
| `TAVILY_API_KEY` | Your Tavily web search API key |

---

*Built with Python + Google Gemini AI + MongoDB Atlas + Tavily Web Search*