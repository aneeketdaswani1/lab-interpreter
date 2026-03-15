# 🔬 LabLens AI – AI-Powered Biomarker Analysis Platform

An intelligent, user-friendly platform that transforms your blood test results into personalized health insights powered by AI research and data science.

**Status**: ✅ Fully functional | **Last Updated**: November 2024

---

## 🎯 Overview

LabLens AI is an educational tool that helps you understand your blood test results better. Upload a PDF lab report, and the platform will:

1. **Extract** biomarker values from your PDF automatically
2. **Analyze** your results against clinical reference ranges and your personal profile
3. **Research** peer-reviewed PubMed studies relevant to your findings
4. **Explain** your results in plain, friendly language (not medical jargon)
5. **Generate** a personalized 30-day action plan based on research
6. **Report** everything in a professional downloadable PDF

## 📊 How It Works

```
┌──────────────────────────────────────────────────────────────┐
│                    USER INPUTS (Sidebar)                     │
│  • Name, Age, Sex (for gender-specific ranges)              │
│  • Activity Level (sedentary → active)                      │
│  • Dietary Preference (omnivore, vegetarian, vegan, keto)   │
│  • Health Goals (energy, weight loss, athletic performance) │
│  • Lab PDF Upload                                           │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│              AGENT 1: PDF EXTRACTION & PARSING               │
│  • Extract text from PDF using pdfplumber                   │
│  • Parse biomarker values with regex + fuzzy matching       │
│  • Classify status: normal/high/low/borderline              │
│  • Fall back to Gemini AI if regex fails                    │
│  Output: Structured biomarker list with units, ranges, status
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│            AGENT 2: RESEARCH (NCBI PubMed API)              │
│  • For each abnormal biomarker:                             │
│    - Search PubMed with biomarker name + status             │
│    - Fetch top 5 studies with abstracts                     │
│    - Cache results (avoid duplicate requests)               │
│  Output: Research context for AI agents                     │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│         AGENT 3: EXPLANATION (Google Gemini 2.5 Flash)      │
│  • For each abnormal biomarker:                             │
│    - Use Gemini to explain what it measures                 │
│    - Why it might be abnormal (lifestyle causes)            │
│    - Context from PubMed research                           │
│    - Practical implications                                 │
│  Output: Friendly, research-backed explanations             │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│      AGENT 4: PLANNING (Google Gemini 2.5 Flash)            │
│  Inputs:                                                     │
│    • User profile (age, sex, activity, diet, goals)         │
│    • All abnormal biomarkers                                │
│    • PubMed research for each                               │
│  Output:                                                     │
│    • Week-by-week 30-day action plan                        │
│    • Nutrition protocol (specific foods, portions)          │
│    • Exercise prescription                                  │
│    • Supplement recommendations                            │
│    • When to see doctor urgently                            │
│    • Re-testing timeline                                    │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│        AGENT 5: REPORTING (fpdf2 PDF Generation)            │
│  Outputs: Professional PDF containing:                       │
│    • Cover page (patient info, health score, disclaimer)    │
│    • Summary table (all biomarkers, color-coded status)     │
│    • Detailed analysis (flagged results + research)         │
│    • Full action plan                                       │
│    • Footer on every page                                   │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│              RESULTS DASHBOARD (5 Tabs)                      │
│  1. Overview: Health score, KPI metrics, charts             │
│  2. Biomarker Details: Full results with explanations       │
│  3. Research: PubMed studies, abstracts, links              │
│  4. Action Plan: Week-by-week protocol, copy/download       │
│  5. Report: Download professional PDF                       │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit 1.40.0 | Interactive web UI with dark theme |
| **PDF Input** | pdfplumber 0.11.0 | Extract text from lab PDFs |
| **PDF Output** | fpdf2 2.8.1 | Generate professional reports |
| **AI/LLM** | Google Generative AI (Gemini 2.5 Flash) | Explanations & planning |
| **Research** | NCBI E-utilities API (free, no key) | PubMed study fetching |
| **Data Processing** | pandas 2.2.2, plotly 5.24.1 | Analysis & visualization |
| **HTTP** | requests 2.32.3 | API calls & rate limiting |
| **Environment** | python-dotenv 1.0.1 | Secret management |
| **Python** | 3.11+ | Core runtime |

---

## 📋 Core Assets

### Biomarker Database
- **60 common blood tests** in `data/reference_ranges.json`
- Gender-specific reference ranges (male/female) for all values
- Organized by category: metabolic, thyroid, lipids, liver, kidney, blood, hormones, vitamins, inflammation
- Examples: HbA1c, Glucose, Cholesterol, TSH, Vitamin D, CRP, Testosterone, Iron, etc.

### Sample Lab Report
- **File**: `data/sample_results.pdf`
- **Format**: Realistic "MedLab Diagnostics" report
- **Biomarkers** (8 intentionally mixed):
  - ✅ Normal: Glucose (98), HDL (62), Triglycerides (128), CRP (0.4)
  - ⚠️ Abnormal: HbA1c (6.1, borderline high), Vitamin D (21, low), TSH (4.8, high), LDL (142, high)
- Perfect for testing the full analysis pipeline

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- macOS, Linux, or Windows
- Google API key (free tier available at [Google AI Studio](https://ai.google.dev))

### Installation

1. **Clone or download** this repository:
   ```bash
   cd lab-interpreter
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # OR
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key:
   # GOOGLE_API_KEY=your_key_here
   ```

5. **Get your Google API key** (free):
   - Visit [Google AI Studio](https://ai.google.dev)
   - Click "Get API Key"
   - Create a new project or select existing
   - Copy the key into your `.env` file

### Running the App

```bash
streamlit run app.py
```

The app will launch at `http://localhost:8502` (or print the correct URL in terminal).

### Testing with Sample Data

1. Start the app with `streamlit run app.py`
2. In the sidebar:
   - Name: "John Smith" (or any name)
   - Age: 48
   - Sex: Male
   - Activity Level: Moderate
   - Dietary Preference: Omnivore
   - Health Goals: Select any options
3. Click "Upload Lab PDF" and select `data/sample_results.pdf`
4. Click "Analyze Now" and watch the agentic pipeline process your results
5. Explore all 5 tabs and download the PDF report

---

## 📁 Project Structure

```
lab-interpreter/
├── app.py                          # Main Streamlit application
├── agent/                          # Modular AI agents
│   ├── extractor.py               # PDF → text extraction
│   ├── parser.py                  # Text → structured biomarkers
│   ├── researcher.py              # Biomarker → PubMed studies
│   ├── explainer.py               # Biomarker → AI explanation
│   ├── planner.py                 # Profile + biomarkers → action plan
│   └── reporter.py                # All data → professional PDF
├── data/
│   ├── reference_ranges.json      # 60-biomarker database (gender-specific ranges)
│   └── sample_results.pdf         # Realistic test report (8 mixed biomarkers)
├── .streamlit/
│   └── config.toml                # Dark theme configuration
├── requirements.txt               # Python dependencies
├── .env.example                   # Template for secrets
├── .gitignore                     # Git exclusions
└── README.md                      # This file
```

---

## 🎨 Features

### Dashboard Tabs

#### 1. **Overview** 📊
- Health Score (0-100%, % of normal biomarkers)
- Key Performance Indicators (KPI cards)
- Biomarker positioning chart
- Category radar chart (comparison across metabolic, thyroid, lipids, etc.)

#### 2. **Biomarker Details** 📋
- Full list of all biomarkers tested
- Expandable sections with AI-generated explanations
- Color-coded status badges
- Percentile from normal range

#### 3. **Research** 🔬
- PubMed studies relevant to your abnormal biomarkers
- Study titles, abstracts, and publication dates
- Direct links to PubMed
- Cached results for fast display

#### 4. **Action Plan** 📅
- 30-day personalized protocol
- Week-by-week milestones
- Nutrition protocol (specific foods and portions)
- Movement/exercise prescription
- Supplement recommendations
- Urgent warning signs
- Re-testing timeline
- Copy to clipboard & download as markdown

#### 5. **Report** 📄
- Professional PDF download containing:
  - Cover page
  - Summary table (all biomarkers)
  - Detailed analysis of flagged results
  - Full action plan
  - PubMed citations

---

## 🔐 Privacy & Security

- **Local Processing**: PDFs are processed in-memory; never stored on disk
- **API Keys**: Required env variables (.env file, not commited to git)
- **No Data Collection**: Platform doesn't save user data or lab results
- **Free APIs**: Uses free tiers of Google Gemini & NCBI PubMed (no credentials needed for PubMed)

---

## ⚠️ Important Disclaimer

**This is an educational tool, NOT a medical device.**

- ❌ Do NOT use for diagnostic purposes
- ❌ Do NOT use as a substitute for professional medical advice
- ✅ DO consult with a qualified healthcare provider before making changes
- ✅ DO use this to better understand your lab results and ask informed questions
- ✅ DO share results with your doctor

All explanations and recommendations are for informational purposes only. Results are not medical advice.

---

## 🔧 Configuration

### Streamlit Theme
Edit `.streamlit/config.toml` to customize:
- Primary color: `#1D9E75` (teal)
- Background: Dark theme
- Port: 8502

### Biomarker Ranges
Edit `data/reference_ranges.json` to:
- Add new biomarkers
- Update reference ranges for your region
- Change unit conversions

### AI Model & Prompts
Edit `agent/explainer.py` and `agent/planner.py` to:
- Switch Gemini models (e.g., `gemini-1.5-pro`)
- Modify system prompts
- Change output structure

---

## 🚨 Troubleshooting

### "GOOGLE_API_KEY not found"
- Ensure `.env` file exists in project root
- Verify `GOOGLE_API_KEY=xxx` is set correctly
- Restart Streamlit after updating `.env`

### "ModuleNotFoundError: No module named 'xxx'"
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### PDF Upload Fails
- Try with `data/sample_results.pdf` first
- Ensure PDF is not corrupted or password-protected
- PDFs must be in English

### Streamlit Connection Timeout
- Check internet connection (needed for Gemini & PubMed APIs)
- Verify API key is valid at [Google AI Studio](https://ai.google.dev)
- Try reducing the number of studies fetched in `agent/researcher.py`

### Slow Analysis
- PubMed research fetching has 0.5s rate limiting (intentional)
- Gemini API calls may take 5-10 seconds per biomarker
- Analysis pipeline typically takes 30-60 seconds for 8 biomarkers

---

## 📊 Sample Output

### Input
- 48-year-old male
- Moderate activity, omnivore diet
- Lab report with 8 mixed biomarkers

### Output Example
```
BIOMARKER: HbA1c = 6.1% [ABNORMAL - Borderline High]

What this measures:
HbA1c is your 3-month average blood glucose. Think of it like 
checking your overall grades instead of just one test.

Why yours is high:
- Excess refined carbohydrates or sugar
- Insufficient physical activity
- Insulin resistance developing

Research says:
Studies show that HbA1c >6.0% increases risk of type 2 diabetes. 
Early lifestyle intervention can reduce this risk by 58%.

Action Plan Week 1:
✓ Reduce refined carbs to <50g/day
✓ Add 30 min brisk walking 5x/week
✓ Increase fiber to 25-30g/day
✓ Add cinnamon to meals (shown to improve insulin sensitivity)

Re-test in 3 months.
```

---

## 🤝 Contributing

This is an educational project. Contributions welcome!

**Ideas for improvement:**
- [ ] Support for more biomarkers
- [ ] Meal plans with recipes
- [ ] Exercise video library
- [ ] Historical tracking (compare reports over time)
- [ ] Supplement interaction checker
- [ ] Integration with wearable data (Apple Health, Withings, etc.)
- [ ] Multiple language support
- [ ] Mobile app version

---

## 📜 License

MIT License – Free to use and modify for educational purposes.

---

## 🙋 Support

- **Documentation**: See this README
- **Sample Data**: Use `data/sample_results.pdf` for testing
- **Google API Issues**: Contact [Google AI Support](https://support.google.com/ai)
- **PubMed API**: See [NCBI Documentation](https://www.ncbi.nlm.nih.gov/home/develop/api/)

---

## 🚀 Next Steps

1. **Get your free Google API key** (5 min): [Google AI Studio](https://ai.google.dev)
2. **Install dependencies** (2 min): `pip install -r requirements.txt`
3. **Test with sample data** (1 min): Upload `data/sample_results.pdf`
4. **Upload your lab PDF** and explore your results!

---

## 📞 Questions?

- Check the troubleshooting section above
- Review inline code comments in `agent/*.py` for technical details
- Test with `data/sample_results.pdf` first

---

**Built with ❤️ for health-conscious people who want to understand their labs better.**

*Last updated: November 2024*
