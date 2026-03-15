# 🔬 LabLens AI – AI-Powered Biomarker Analysis Platform

**Transform your blood test results into actionable health insights with AI-powered analysis, peer-reviewed research, and personalized recommendations.**

An intelligent, user-friendly Streamlit application that helps you understand your biomarkers through AI explanations, scientific research, and evidence-based protocols.

- **Status**: ✅ Production-Ready | **Version**: 1.0 | **Last Updated**: March 2026
- **Demo Data**: Test with included `sample_results.pdf` (8 realistic biomarkers)
- **Free to Use**: Open-source, no medical license required

---

## 📖 Table of Contents

1. [What It Does](#-what-it-does)
2. [How It Works](#️-how-it-works)
3. [Technology Stack](#️-technology-stack)
4. [Quick Start](#-quick-start--5-minutes)
5. [Test with Sample Data](#-test-with-sample-data-30-seconds)
6. [Project Structure](#-project-structure)
7. [Features](#-features)
8. [Privacy & Security](#-privacy--security)
9. [Medical Disclaimer](#-important-medical-disclaimer)
10. [Troubleshooting](#-troubleshooting)
11. [Sample Analysis Output](#-sample-analysis-output)
12. [Roadmap](#️-future-roadmap)
13. [Contributing](#-contributing)
14. [FAQ](#-frequently-asked-questions)
15. [License](#-license)

---

## 🎯 What It Does

LabLens AI analyzes blood test PDFs in 6 intelligent steps:

1. **📄 Extract** – Automatically parse PDF lab reports to extract biomarker values
2. **🔍 Parse** – Align results with reference ranges (gender-specific) and classify status
3. **📚 Research** – Fetch peer-reviewed PubMed studies for abnormal findings
4. **💡 Explain** – AI-generated explanations in plain, friendly language (not medical jargon)
5. **📋 Plan** – Generate personalized 30-day protocols tailored to your profile
6. **📊 Report** – Download a professional, shareable PDF report with all findings

## 🏗️ How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                  STEP 1: USER INPUT (Sidebar)                   │
│  • Personal Profile: Name, Age, Sex (for gender-specific ranges)│
│  • Lifestyle: Activity level, dietary preference, health goals  │
│  • Lab Report: Upload PDF file from your healthcare provider    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         STEP 2: EXTRACTION (pdfplumber)                         │
│  Extract all text from PDF, clean OCR artifacts & formatting    │
│  Output: Raw biomarker text string                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         STEP 3: PARSING (Regex + Gemini AI)                     │
│  • Match biomarker names/values with 40+ regex patterns         │
│  • Fall back to Gemini if regex finds <3 results               │
│  • Classify: normal | high | low | borderline                  │
│  Output: Structured biomarker list {name, value, unit, status}  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         STEP 4: RESEARCH (NCBI PubMed API)                      │
│  For each abnormal biomarker:                                   │
│  • Search PubMed with biomarker name + status                  │
│  • Fetch top 5 studies with abstracts                          │
│  • Cache results to avoid duplicate API calls                  │
│  Output: [{title, abstract, PMID, link}]                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│      STEP 5: EXPLANATION (Google Gemini 2.5 Flash)             │
│  For each abnormal biomarker:                                   │
│  • What it measures (simple analogy)                            │
│  • Why it's abnormal (common lifestyle causes)                 │
│  • Research context (PubMed studies cited)                      │
│  • Practical implications                                       │
│  Output: Friendly, research-backed explanation text             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│      STEP 6: PLANNING (Google Gemini 2.5 Flash)                │
│  Inputs: User profile + abnormal biomarkers + research          │
│  Output: Personalized 30-day protocol:                          │
│  • Weekly milestones & nutrition changes                       │
│  • Exercise prescriptions (specific intensity & duration)      │
│  • Supplement recommendations (research-backed)                 │
│  • Urgent warning signs & retest timeline                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│      STEP 7: REPORTING (fpdf2 PDF Generation)                  │
│  Multi-page professional PDF:                                   │
│  • Cover: Patient info, health score %, disclaimer              │
│  • Summary Table: All biomarkers with color-coded status       │
│  • Details: Flagged results + research citations               │
│  • Protocol: Full 30-day action plan                            │
│  Output: Downloadable PDF file                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│      RESULTS DASHBOARD (5 Interactive Tabs)                      │
│  1. Overview: Health score, KPIs, visualizations               │
│  2. Details: All biomarkers with AI explanations               │
│  3. Research: PubMed studies with links                         │
│  4. Protocol: Week-by-week action plan                          │
│  5. Report: Download professional PDF                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Frontend** | Streamlit | 1.40.0 | Interactive web UI with dark theme |
| **PDF Input** | pdfplumber | 0.11.0 | Extract text from lab PDFs |
| **PDF Output** | fpdf2 | 2.8.1 | Generate professional PDF reports |
| **AI/LLM** | Google Generative AI | 0.8.6 | AI explanations & 30-day plans |
| **Research API** | NCBI E-utilities | — | PubMed study fetching (free) |
| **Data Lib** | pandas | 2.2.2 | Data processing & analysis |
| **Charts** | Plotly | 5.24.1 | Interactive visualizations |
| **HTTP** | requests | 2.32.3 | API calls with rate limiting |
| **Config** | python-dotenv | 1.0.1 | Environment variable management |
| **Runtime** | Python | 3.11+ | Core interpreter |
| **OS** | macOS / Linux / Windows | — | Cross-platform support |

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

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Your Free Google API Key *(1 min)*

1. Visit **[Google AI Studio](https://ai.google.dev)** 
2. Click **"Get API Key"** → **"Create new project"**
3. Copy your key (looks like: `AIza...`)
4. Safe to use - free tier includes 60 API calls/minute

### Step 2: Clone & Setup *(2 min)*

```bash
# Clone repository
git clone <your-repo-url>
cd lab-interpreter

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment *(1 min)*

```bash
# Copy template
cp .env.example .env

# Edit .env and paste your Google API key
# GOOGLE_API_KEY=AIza...
```

### Step 4: Launch App *(1 min)*

```bash
streamlit run app.py
```

The app opens at **`http://localhost:8502`**

---

## 📊 Test with Sample Data (30 seconds)

1. **Name**: John Smith
2. **Age**: 48
3. **Sex**: Male
4. **Activity Level**: Moderate
5. **Diet**: Omnivore
6. **Upload**: Select `data/sample_results.pdf` (included in repo)
7. **Click**: "Analyze Now"
8. **Wait**: 30-60 seconds for analysis to complete
9. **Explore**: All 5 tabs and download the PDF report

The sample data includes **8 intentionally mixed biomarkers** (4 normal, 4 abnormal) perfect for seeing the full analysis pipeline.

---

## 📁 Project Structure

```
lab-interpreter/
├── 📄 README.md                    ← You are here
├── 📋 requirements.txt              ← All Python dependencies
├── 🔑 .env.example                  ← Environment variable template (copy to .env)
├── 🚀 app.py                        ← Main Streamlit application (850+ lines)
│
├── 📂 agent/                        ← 6 specialized AI agent modules
│   ├── extractor.py                 ← PDF text extraction
│   ├── parser.py                    ← Biomarker parsing + Gemini fallback
│   ├── researcher.py                ← PubMed API integration
│   ├── explainer.py                 ← AI-powered explanations (Gemini)
│   ├── planner.py                   ← 30-day protocol generation (Gemini)
│   └── reporter.py                  ← Professional PDF report generation
│
├── 📂 data/                         ← Biomarker database & sample data
│   ├── reference_ranges.json        ← 60 biomarkers with gender-specific ranges
│   └── sample_results.pdf           ← Realistic test lab report (8 mixed results)
│
├── 📂 .streamlit/                   ← Streamlit configuration
│   └── config.toml                  ← Dark theme settings
│
└── 📂 __pycache__/                  ← Python bytecode (ignore)
```

---

## ✨ Features

### 📊 Dashboard & Visualization
- **Health Score Meter** – 0-100% based on biomarkers in normal range
- **Key Performance Indicators** – Color-coded status for each biomarker category
- **Biomarker Positioning Chart** – Visual placement within normal ranges
- **Category Radar Chart** – Compare across 6 health categories
- **Status Badges** – 🟢 Normal | 🔴 Abnormal | 🟡 Borderline

### 📋 Biomarker Analysis
- **60 Biomarkers** – Comprehensive blood test coverage
- **Gender-Specific Ranges** – Separate reference values for male/female
- **6 Categories** – Metabolic, Thyroid, Lipids, Liver, Kidney, Blood, Hormones, Vitamins, Inflammation
- **Multi-Status Classification** – normal | high | low | borderline_high | borderline_low

### 🔬 AI-Powered Insights
- **Automated Explanations** – Google Gemini generates easy-to-understand biomarker explanations
- **Research Integration** – Links every insight to peer-reviewed PubMed studies
- **Personalized Protocols** – AI-generated 30-day action plans based on your profile
- **Study Caching** – Efficient API usage with smart result caching

### 📥 PDF Support
- **Upload Lab PDFs** – Works with most US lab reports (LabCorp, Quest, MedLab, etc.)
- **OCR Cleanup** – Automatic removal of scanning artifacts
- **Fallback Parsing** – Uses Gemini AI if regex extraction fails

### 📑 Professional Reports
- **Multi-Page PDF Export** – Cover page, summary table, detailed analysis, full protocol
- **Color-Coded Results** – Visual status indicators in tabular format
- **Citation Management** – PubMed study links and PMIDs included
- **Professional Formatting** – Ready to download and share with healthcare providers

### 🔄 Smart Processing
- **Rate Limiting** – PubMed API: 0.5s between requests (respectful)
- **Caching** – No duplicate API calls for same biomarkers
- **Progress Tracking** – Visual step-by-step analysis progress
- **Error Handling** – Graceful fallback strategies for all modules

---

## 🔐 Privacy & Security

✅ **Your Data is Safe**
- **No Cloud Storage** – PDFs processed in-memory, never saved to disk
- **No Data Collection** – Platform doesn't track users or store results
- **Local Processing** – Everything runs on your machine
- **Open Source** – Full transparency, audit the code yourself
- **Free APIs** – Uses free tiers of Google Gemini & NCBI PubMed (no login tracking)

🔑 **API Keys**
- **Google Gemini**: Required (personal API key, not shared)
- **NCBI PubMed**: No key needed (free public service)
- `.env` file is gitignored (never committed to repository)

---

## ⚠️ Important Medical Disclaimer

**This is an EDUCATIONAL TOOL, NOT a medical device or diagnostic service.**

### ✅ DO:
- Use this to understand your lab results better
- Ask informed questions to your healthcare provider
- Share the PDF report with your doctor
- Track trends in your health over time
- Use protocols as general wellness guidance

### ❌ DO NOT:
- Use as a substitute for professional medical advice
- Make medical decisions without consulting a doctor
- Ignore results that require urgent medical attention
- Share results with anyone without your permission
- Rely solely on AI recommendations for health changes

**Always consult a qualified healthcare provider before making any health decisions.** 

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| `GOOGLE_API_KEY not found` | Copy .env.example to .env and add your key |
| `ModuleNotFoundError: 'X'` | Ensure venv is activated, run `pip install -r requirements.txt` |
| PDF upload fails | Test with `data/sample_results.pdf` first, check file isn't corrupted |
| Slow analysis (>2 min) | Normal – PubMed API is rate-limited. Fewer abnormal biomarkers = faster |
| Streamlit connection error | Check internet (needed for Gemini & PubMed), verify API key is valid |
| "Regex error" during parsing | Parser falls back to Gemini automatically, usually resolves on retry |

---

## 📊 Sample Analysis Output

### Input Example
```
Lab Report: data/sample_results.pdf
Patient: John Smith, 48M, Moderate activity, Omnivore diet
Biomarkers tested: 8 total (4 normal, 4 abnormal)
```

### Dashboard Output
```
🎯 HEALTH SCORE: 50%
   Biomarkers in normal range: 4/8

📈 KEY METRICS:
   • Metabolic: 2/3 abnormal (HbA1c↑, Glucose→Normal)
   • Lipids: 2/2 abnormal (LDL↑, HDL→Normal)
   • Thyroid: 1/1 abnormal (TSH↑)
   • Vitamins: 1/2 abnormal (Vitamin D↓)
```

### AI Explanation Example
```
📊 HbA1c = 6.1% [BORDERLINE HIGH]

📖 What This Measures:
   Your 3-month average blood sugar. Think of it like checking your 
   overall grade instead of just one test score.

⚠️ Why Yours is High:
   • Too many refined carbs (white bread, sugar, processed foods)
   • Not enough physical activity (recommend 150 min/week)
   • Insulin resistance developing (catch it now!)

🔬 Research Says:
   Studies show that early intervention at HbA1c 6.0-6.4% can reduce 
   Type 2 diabetes risk by 58%. (PubMed: 15234856)

✅ Good News:
   This is reversible! Diet + exercise changes typically lower HbA1c 
   by 0.5-1% in 3 months.
```

### Action Plan Example
```
🎯 YOUR 30-DAY PROTOCOL

WEEK 1-2: Foundation
  • Reduce refined carbs to <50g/day
  • Add 30 min brisk walking, 5x/week
  • Increase fiber to 25-30g/day
  • Add cinnamon to meals (insulin-sensitizing)

WEEK 3-4: Optimization
  • Add resistance training 2x/week
  • Explore low-glycemic index foods
  • Consider berberine supplement (0.5g 3x/day)
  • Track blood glucose at home (optional)

📅 Retest: 3 months (check HbA1c improvement)
⚠️ Urgent: If you develop blurred vision or extreme fatigue, see doctor immediately
```

---

## 🗺️ Future Roadmap

### Phase 2 (In Development)
- [ ] Historical tracking – Compare reports over time
- [ ] Meal plan generation – AI-created recipes matching your needs
- [ ] Supplement checker – Drug-supplement interaction warnings
- [ ] Wearable integration – Pull data from Apple Health, Fitbit, Withings

### Phase 3 (Planned)
- [ ] Multi-language support (Spanish, French, German, Mandarin)
- [ ] Mobile app (iOS/Android)
- [ ] Doctor collaboration mode (share reports securely)
- [ ] Biomarker trend analysis with predictive modeling
- [ ] Integration with existing health platforms (MyFitnessPal, Cronometer)

---

## 🤝 Contributing

This is an open-source educational project. Contributions welcome!

To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Ways to Contribute
- Report bugs or suggest features via Issues
- Improve documentation or add examples
- Add support for new biomarkers
- Enhance AI prompts and explanations
- Optimize performance or code quality
- Translate to other languages
- Write blog posts or tutorials

---

## 📜 License

**MIT License** – Free to use and modify for educational purposes.

You are free to:
- ✅ Use commercially (though this is educational)
- ✅ Modify and adapt
- ✅ Distribute
- ✅ Use privately

Just include the license notice.

---

## 📚 Learning Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Google Gemini API**: https://ai.google.dev/docs
- **NCBI PubMed API**: https://www.ncbi.nlm.nih.gov/home/develop/api/
- **Clinical Biomarkers**: https://en.wikipedia.org/wiki/Biomarker

---

## 🙋 Support & Questions

| Question | Answer |
|----------|--------|
| How do I get a Google API key? | Visit [Google AI Studio](https://ai.google.dev), click "Get API Key" |
| Can I use this for medical diagnosis? | No – this is educational only. Consult a healthcare provider |
| Works on Windows/Mac/Linux? | Yes to all! Python 3.11+ required |
| How long does analysis take? | 30-60 seconds depending on biomarker count |
| Can I modify the biomarker ranges? | Yes – edit `data/reference_ranges.json` |
| What if my PDF doesn't parse correctly? | Email PDF sample or file an issue on GitHub |

---

## 🎓 Frequently Asked Questions

**Q: Is this a medical device?**
A: No. This is an educational tool to help you understand your lab results. Always consult healthcare providers for medical decisions.

**Q: Do you store my data?**
A: No. Everything runs locally on your computer. We don't collect any information.

**Q: Which lab reports are supported?**
A: Most US lab reports (LabCorp, Quest, Cleveland Clinic, Mayo Clinic, etc.). Test with your PDF – fallback to Gemini parsing if regex fails.

**Q: Can I use this offline?**
A: No – requires internet for Google Gemini API and PubMed API calls. Local processing happens offline.

**Q: Can I modify the action plan protocols?**
A: Yes! Edit the system prompts in `agent/planner.py` to customize recommendations for your needs.

**Q: How accurate are the explanations?**
A: Gemini provides science-backed explanations, but they should supplement, not replace, professional medical advice.

---

## 📧 Contact & Community

- **GitHub Issues**: Report bugs or suggest features
- **Discussions**: Share ideas and best practices
- **Email**: Include the word "LabLens" in subject line

---

## 🙏 Acknowledgments

- **Google** – Generative AI API
- **NCBI** – PubMed research database
- **Streamlit** – Amazing web framework
- **Open Source Community** – All libraries that make this possible

---

**Built with ❤️ for people who want to understand their health better.**

**Last updated**: March 2026  
**Status**: ✅ Production Ready (v1.0)
