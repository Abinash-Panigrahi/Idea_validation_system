# 🚀 ThynxAI Idea Lab — Startup Idea Validator

An AI-powered system that analyzes startup ideas and generates detailed evaluation reports using Google Gemini AI.

---

## 📌 What it Does

1. Takes a startup idea as input
2. Collects founder information (name + background)
3. Generates intelligent follow-up questions based on the idea
4. Analyzes the idea across 8 structured dimensions
5. Generates a detailed evaluation report (JSON + Markdown)

---

## 🧩 Project Structure
```
Idea_validation_system/
├── prompts.py          # All AI prompt functions
├── analyzer.py         # Gemini API integration
├── report.py           # JSON + Markdown report generation
├── main.py             # CLI interface
├── app.py              # Streamlit web interface
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
```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
```bash
# Copy the example file:
cp .env.example .env

# Add your Gemini API key to .env:
GEMINI_API_KEY=your-actual-gemini-key-here
```

### 6. Get Gemini API Key
1. Go to: https://aistudio.google.com
2. Click "Get API Key"
3. Copy and paste into `.env` file

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

---

## 📊 Analysis Output

After running, the system generates:

- `outputs/analysis.json` → Structured JSON data
- `outputs/report.md` → Human-readable Markdown report

### 8 Analysis Sections:
1. Problem Statement
2. Proposed Solution
3. Core Innovation
4. Market Landscape
5. Scores (1-10) with reasoning
6. Support Required
7. Tech Stack Suggestion
8. Overall Verdict (MVP/Investment/Incubator ready)

---

## 🛠️ Tech Stack

- **Language:** Python
- **AI:** Google Gemini API (gemini-2.5-flash)
- **UI:** Streamlit
- **Output:** JSON + Markdown

---

## 📦 Sample Input/Output

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

---

*Built with Python + Google Gemini AI*

