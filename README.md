# ✦ CVanta AI

### One Resume. Every Career.

**CVanta AI** is a multi-domain AI-powered Resume Analyzer, Resume Builder, and Career Assistant built with **Python, Flask, and Google Gemini AI**.

It analyzes PDF resumes, identifies career domains and skills, recommends suitable job roles, provides career insights, and helps users create professional resumes.

---

## ✨ Features

- 📄 PDF Resume Analysis
- 🌐 Multi-Domain Career Detection
- 🎯 Best Matching Job Role
- 📊 Career Fit Score
- 🧠 Smart Skill Detection
- 🛠️ Tools & Technology Detection
- 💪 Resume Strength Analysis
- ⚡ Missing / Recommended Skills
- 📈 Resume Improvement Suggestions
- 🚀 AI Career Recommendations
- 📝 AI Resume Builder
- ✨ Professional Headline Generator
- ✨ Professional Summary Generator
- 💼 AI Experience Improvement
- 🧩 AI Project Description Improvement
- 🎤 Interview Question Generator
- 🛣️ Career Learning Roadmap
- 🔍 Resume Gap Detection
- ✅ Skill Evidence Checker
- 🔄 Resume Consistency Checker
- 📄 Resume PDF Generation

---

## 🌍 Multi-Domain Support

CVanta AI is designed to analyze resumes from many different career fields, including:

- Computer Science / IT
- Artificial Intelligence & Machine Learning
- Mechanical Engineering
- Civil Engineering
- Electrical Engineering
- Electronics & Communication
- Automobile Engineering
- Chemical Engineering
- Biotechnology
- Production & Manufacturing
- Aerospace
- Architecture
- Agriculture
- Finance
- Accounting
- Marketing
- Sales
- Human Resources
- Operations & Supply Chain
- UI/UX Design
- Healthcare
- Nursing
- Pharmacy
- Teaching & Education
- Law
- Hospitality
- Technical / ITI Trades
- Other domains through AI-based detection

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Flask | Web application framework |
| HTML | Website structure |
| CSS | User interface styling |
| JavaScript | Frontend interactions |
| Google Gemini AI | AI analysis and generation |
| PyMuPDF | PDF text extraction |
| python-dotenv | Environment variable management |
| Werkzeug | File handling and Flask utilities |
| Gunicorn | Production server |

---

## 📁 Project Structure

```text
CVanta-AI/
│
├── src/
│   ├── ai_analyzer.py
│   ├── matcher.py
│   ├── pdf_reader.py
│   └── skill_extractor.py
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── resume_builder.html
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/PRANS009/CVanta-AI.git
```

### 2. Open the project folder

```bash
cd CVanta-AI
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the virtual environment

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Gemini API Setup

Create a `.env` file inside the project root.

Add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> Never upload your real Gemini API key to GitHub.

An example configuration is available in `.env.example`.

---

## ▶️ Run CVanta AI

Start the Flask application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5001
```

---

## 📊 How It Works

```text
Upload Resume
      ↓
PDF Text Extraction
      ↓
Local Skill Detection
      ↓
Domain Detection
      ↓
Gemini AI Analysis
      ↓
Career Fit + Job Roles
      ↓
Strengths + Improvements
      ↓
Career Recommendations
```

---

## 🔐 Security

Sensitive and unnecessary files are excluded from Git using `.gitignore`.

Examples:

```text
.env
.venv/
__pycache__/
*.pyc
uploads/
*.bak
.DS_Store
```

This helps prevent API keys, uploaded resumes, cache files, and local environment files from being published.

---

## 🗺️ Roadmap

Future improvements planned for CVanta AI:

- 📊 Separate ATS Score Checker
- 🎯 Job Description Matching
- 📑 More Resume Templates
- 📥 Improved Resume Export
- 🌐 Cloud Deployment
- 💼 Target Job Role Analysis
- 🤖 Enhanced AI Career Guidance
- 📈 More detailed resume scoring

---

## ⚠️ Disclaimer

CVanta AI provides AI-generated resume and career guidance. Results should be treated as recommendations and may vary depending on resume content and AI model responses.

---

## 🔗 Repository

**GitHub:**  
https://github.com/PRANS009/CVanta-AI

---

## ✦ CVanta AI

### One Resume. Every Career.

Built with Python, Flask, and Gemini AI.