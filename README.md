# Resume Analyzer AI Backend

FastAPI backend for Resume Analyzer AI.

Features:
- Resume upload
- PDF/DOCX/TXT parsing
- Resume-job matching
- ATS score generation
- Skill extraction
- Missing skill detection
- Recommendations
- Interview question generation
- Groq AI integration
- Fallback local analysis

---

# Project Structure

```text
backend/
│
├── main.py
├── config.py
├── requirements.txt
│
├── services/
│   ├── resume_parser.py
│   ├── ai_analyzer.py
│   ├── scoring.py
│   └── interview_questions.py
│
├── models/
│   └── schemas.py
│
└── uploads/