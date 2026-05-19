# Resume Analyzer AI

**Resume Analyzer AI** is a comprehensive, AI-powered platform designed to help job seekers optimize their resumes, understand how well they match specific job descriptions, and practice for interviews. It provides deep insights into candidate strengths, missing skills, and missing fields while offering realistic, interactive AI interview practice.

---

## 🚀 Key Features

### 📄 Intelligent Resume Analysis
- **Format Support:** Upload resumes in PDF, DOCX, or TXT formats.
- **ATS Match Scoring:** Get a realistic match percentage against a provided job description.
- **Skill Extraction:** Automatically identifies technical and soft skills present in the resume.
- **Gap Analysis:** Highlights missing skills and critical missing resume fields (e.g., contact info, education, project links).
- **Actionable Recommendations:** Provides strengths, weaknesses, and concrete steps for improvement.
- **Audio Feedback:** Summarizes candidate profiles using integrated Text-to-Speech (TTS).

### ❓ Question Generation
- Automatically generates tailored interview questions based on the resume and job description.
- Categorizes questions into **Technical**, **HR**, and **Role-Based** subsets.

### 💬 Live AI Interview Practice
- **Role-Play Modes:** Practice with AI personas like *HR Interviewer*, *Senior Developer*, *Technical Recruiter*, or *Team Lead*.
- **Context-Aware:** Uses your resume and target job description to ask highly relevant, personalized questions.
- **Dynamic Follow-ups:** The AI challenges vague answers and digs deeper, simulating a real interview experience.

---

## 🛠️ Technology Stack

### Backend (FastAPI)
- **Framework:** FastAPI
- **Parsing:** `pypdf`, `python-docx`
- **AI Integration:** OpenAI API client (configured for Groq AI integration)
- **Validation:** Pydantic
- **Environment:** `python-dotenv`, `pydantic-settings`

### Frontend (Streamlit)
- **Framework:** Streamlit
- **Styling:** Custom CSS with a modern, dark "neon" aesthetic and dynamic gradients.
- **HTTP Client:** `requests` for backend communication.
- **Audio:** Custom `voice_component.py` for text-to-speech functionality.

---

## 📂 Project Structure

```text
resume-analyzer-ai/
│
├── backend/
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration and environment variables
│   ├── requirements.txt         # Backend dependencies
│   ├── services/                # Core business logic
│   │   ├── resume_parser.py     # PDF/DOCX/TXT parsing service
│   │   ├── ai_analyzer.py       # Core AI analysis and Groq integration
│   │   ├── scoring.py           # ATS scoring algorithms
│   │   └── interview_questions.py # Question generation service
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response schemas
│   └── uploads/                 # Temporary directory for uploaded files
│
├── frontend/
│   ├── app.py                   # Streamlit UI application
│   ├── voice_component.py       # Text-to-speech integration
│   └── requirements.txt         # Frontend dependencies
│
├── sample_data/                 # Sample resumes and job descriptions for testing
├── .env                         # Environment variables (API keys, URLs)
└── README.md                    # Project documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9+
- A Groq API Key (or OpenAI compatible endpoint)

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd resume-analyzer-ai
```

### 2. Environment Variables
Create a `.env` file in the root directory (or use the existing one) and configure the following variables:
```env
# Backend settings
GROQ_API_KEY=your_groq_api_key_here
# Frontend settings
BACKEND_URL=http://127.0.0.1:8000
```

### 3. Start the Backend Server
Open a new terminal and navigate to the project root:
```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Run the FastAPI server
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
The backend will be available at `http://127.0.0.1:8000`. You can view the API documentation at `http://127.0.0.1:8000/docs`.

### 4. Start the Frontend Application
Open a second terminal and navigate to the project root:
```bash
# Activate the same virtual environment
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install frontend dependencies
pip install -r frontend/requirements.txt

# Run the Streamlit app
streamlit run frontend/app.py
```
The frontend UI will automatically open in your default browser at `http://localhost:8501`.

---

## 🎯 Usage Guide

1. **Resume Analysis Tab:** Upload your resume (PDF/DOCX/TXT) and paste the target job description. Click "Analyze with Groq" to receive a comprehensive breakdown of your ATS score, skills, missing fields, and actionable recommendations.
2. **Interview Questions Tab:** Manually paste your resume and job description text to generate a curated list of Technical, HR, and Role-Based interview questions.
3. **AI Interview Chat Tab:** Select an interviewer persona from the dropdown. Paste your context, and begin an interactive chat. Answer the AI's questions, and it will respond with follow-ups to test your knowledge just like a real interview.