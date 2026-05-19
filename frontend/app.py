import os

import requests
import streamlit as st
from dotenv import load_dotenv

from voice_component import speak_text

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
ALLOWED_FILE_TYPES = ["pdf", "docx", "txt"]
INTERVIEW_ROLES = [
    "HR Interviewer",
    "Senior Developer",
    "Technical Recruiter",
    "Team Lead",
]

st.set_page_config(
    page_title="Resume Analyzer AI",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --bg: #050816;
        --panel: rgba(12, 18, 38, 0.82);
        --panel-strong: rgba(18, 27, 56, 0.96);
        --cyan: #22d3ee;
        --pink: #fb37ff;
        --green: #2cff9d;
        --text: #f8fbff;
        --muted: #a8b3cf;
    }

    .stApp {
        color: var(--text);
        background:
            radial-gradient(circle at 12% 0%, rgba(34, 211, 238, 0.25), transparent 30%),
            radial-gradient(circle at 90% 12%, rgba(251, 55, 255, 0.18), transparent 34%),
            linear-gradient(135deg, #050816 0%, #0a1024 48%, #12091f 100%);
    }

    .block-container {
        max-width: 1240px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 26px 30px;
        border: 1px solid rgba(34, 211, 238, 0.28);
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(13, 22, 49, 0.92), rgba(26, 10, 42, 0.84));
        box-shadow: 0 0 42px rgba(34, 211, 238, 0.14);
        margin-bottom: 18px;
    }

    .hero h1 {
        margin: 0;
        font-size: 42px;
        letter-spacing: 0;
    }

    .hero p {
        margin: 8px 0 0;
        color: var(--muted);
        font-size: 17px;
    }

    .neon-card {
        padding: 20px;
        border-radius: 8px;
        background: var(--panel);
        border: 1px solid rgba(168, 179, 207, 0.16);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 18px 40px rgba(0, 0, 0, 0.22);
        margin-bottom: 16px;
    }

    .score-box {
        text-align: center;
        padding: 24px;
        border-radius: 8px;
        background:
            linear-gradient(135deg, rgba(34, 211, 238, 0.2), rgba(251, 55, 255, 0.22)),
            var(--panel-strong);
        border: 1px solid rgba(44, 255, 157, 0.32);
        box-shadow: 0 0 38px rgba(44, 255, 157, 0.14);
        margin-bottom: 16px;
    }

    .score-box h1 {
        color: var(--green);
        font-size: 58px;
        margin: 0;
        text-shadow: 0 0 18px rgba(44, 255, 157, 0.45);
    }

    .score-box p {
        color: var(--muted);
        margin: 4px 0 0;
    }

    .metric-row {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin-bottom: 18px;
    }

    .mini-metric {
        padding: 16px;
        border-radius: 8px;
        border: 1px solid rgba(34, 211, 238, 0.18);
        background: rgba(255, 255, 255, 0.045);
    }

    .mini-metric span {
        color: var(--muted);
        font-size: 13px;
    }

    .mini-metric strong {
        display: block;
        font-size: 26px;
        color: var(--cyan);
        margin-top: 4px;
    }

    .status-pill {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 999px;
        color: #061018;
        background: linear-gradient(90deg, var(--green), var(--cyan));
        font-weight: 700;
        margin-bottom: 14px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 18px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .stTabs [aria-selected="true"] {
        color: #061018;
        background: linear-gradient(90deg, var(--cyan), var(--green));
    }

    .stButton > button {
        width: 100%;
        height: 3rem;
        border-radius: 8px;
        border: 1px solid rgba(34, 211, 238, 0.45);
        background: linear-gradient(90deg, #06b6d4, #8b5cf6, #fb37ff);
        color: white;
        font-weight: 800;
        box-shadow: 0 0 24px rgba(34, 211, 238, 0.2);
    }

    div[data-testid="stFileUploader"],
    div[data-testid="stTextArea"],
    div[data-testid="stSelectbox"] {
        border-radius: 8px;
    }

    .chat-note {
        color: var(--muted);
        font-size: 14px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def check_backend_health() -> bool:
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def render_list(items: list[str]) -> None:
    if not items:
        st.info("No data available.")
        return

    for item in items:
        st.markdown(f"- {item}")


def render_card(title: str, items: list[str] | str) -> None:
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.subheader(title)
    if isinstance(items, str):
        st.write(items)
    else:
        render_list(items)
    st.markdown("</div>", unsafe_allow_html=True)


def post_json(endpoint: str, payload: dict, timeout: int = 60) -> requests.Response:
    return requests.post(f"{BACKEND_URL}{endpoint}", json=payload, timeout=timeout)


if "last_resume_text" not in st.session_state:
    st.session_state.last_resume_text = ""
if "last_job_description" not in st.session_state:
    st.session_state.last_job_description = ""
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_role" not in st.session_state:
    st.session_state.chat_role = INTERVIEW_ROLES[0]

st.markdown(
    """
    <div class="hero">
        <h1>Resume Analyzer AI</h1>
        <p>Groq-powered resume review, missing-field detection, and realistic interview practice in one focused workspace.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

backend_running = check_backend_health()

if backend_running:
    st.markdown('<span class="status-pill">Backend connected</span>', unsafe_allow_html=True)
else:
    st.error("Backend is not running. Please start the FastAPI server first.")
    st.stop()

tab1, tab2, tab3 = st.tabs(
    [
        "Resume Analysis",
        "Interview Questions",
        "AI Interview Chat",
    ]
)

with tab1:
    left_col, right_col = st.columns([0.42, 0.58], gap="large")

    with left_col:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.subheader("Upload and Target")

        uploaded_resume = st.file_uploader(
            "Upload resume",
            type=ALLOWED_FILE_TYPES,
            help="Supported formats: PDF, DOCX, TXT",
        )

        job_description = st.text_area(
            "Paste job description",
            height=260,
            placeholder="Paste the target job description here...",
        )

        analyze_button = st.button("Analyze with Groq")
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.subheader("What You Get")
        st.markdown(
            "- AI summary and ATS-style match score\n"
            "- Missing resume fields, not just missing skills\n"
            "- Strengths, weaknesses, and practical next steps\n"
            "- Technical, HR, and role-based interview questions"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if analyze_button:
        if not uploaded_resume:
            st.warning("Please upload a resume first.")
        elif not job_description.strip():
            st.warning("Please paste the job description.")
        else:
            with st.spinner("Groq is reviewing your resume like a sharp recruiter..."):
                try:
                    files = {
                        "resume": (
                            uploaded_resume.name,
                            uploaded_resume.getvalue(),
                            uploaded_resume.type,
                        )
                    }
                    data = {"job_description": job_description}

                    response = requests.post(
                        f"{BACKEND_URL}/api/analyze",
                        files=files,
                        data=data,
                        timeout=120,
                    )

                    if response.status_code != 200:
                        st.error(f"Error: {response.text}")
                    else:
                        result = response.json()
                        st.session_state.last_job_description = job_description

                        st.markdown(
                            f"""
                            <div class="score-box">
                                <h1>{result['match_score']}%</h1>
                                <p>Resume Match Score</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.markdown(
                            f"""
                            <div class="metric-row">
                                <div class="mini-metric"><span>Skills Found</span><strong>{len(result['skills_found'])}</strong></div>
                                <div class="mini-metric"><span>Missing Skills</span><strong>{len(result['missing_skills'])}</strong></div>
                                <div class="mini-metric"><span>Missing Fields</span><strong>{len(result['missing_fields'])}</strong></div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        render_card("Candidate Summary", result["candidate_summary"])
                        speak_text(result["candidate_summary"])

                        col1, col2 = st.columns(2)
                        with col1:
                            render_card("Skills Found", result["skills_found"])
                            render_card("Strengths", result["strengths"])
                        with col2:
                            render_card("Missing Skills", result["missing_skills"])
                            render_card("Missing Resume Fields", result["missing_fields"])

                        col3, col4 = st.columns(2)
                        with col3:
                            render_card("Weaknesses", result["weaknesses"])
                        with col4:
                            render_card("Recommendations", result["recommendations"])

                        questions = result["interview_questions"]
                        render_card("Technical Questions", questions["technical_questions"])
                        render_card("HR Questions", questions["hr_questions"])
                        render_card("Role-Based Questions", questions["role_based_questions"])

                except requests.exceptions.RequestException:
                    st.error("Failed to connect to backend.")
                except Exception as error:
                    st.error(f"Unexpected error: {str(error)}")

with tab2:
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.subheader("Generate Interview Questions")

    manual_resume_text = st.text_area(
        "Resume text",
        height=220,
        placeholder="Paste resume text here...",
        key="resume_text",
    )

    manual_job_description = st.text_area(
        "Job description",
        height=220,
        placeholder="Paste job description here...",
        key="job_description_manual",
    )

    generate_questions_button = st.button("Generate Questions")
    st.markdown("</div>", unsafe_allow_html=True)

    if generate_questions_button:
        if not manual_resume_text.strip() or not manual_job_description.strip():
            st.warning("Please fill all fields.")
        else:
            st.session_state.last_resume_text = manual_resume_text
            st.session_state.last_job_description = manual_job_description

            with st.spinner("Building interview questions..."):
                try:
                    payload = {
                        "resume_text": manual_resume_text,
                        "job_description": manual_job_description,
                    }

                    response = post_json("/api/generate-questions", payload)

                    if response.status_code != 200:
                        st.error(f"Error: {response.text}")
                    else:
                        result = response.json()
                        st.success("Questions generated successfully.")
                        render_card("Technical Questions", result["technical_questions"])
                        render_card("HR Questions", result["hr_questions"])
                        render_card("Role-Based Questions", result["role_based_questions"])

                except requests.exceptions.RequestException:
                    st.error("Failed to connect to backend.")
                except Exception as error:
                    st.error(f"Unexpected error: {str(error)}")

with tab3:
    setup_col, chat_col = st.columns([0.36, 0.64], gap="large")

    with setup_col:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.subheader("Interview Setup")

        selected_role = st.selectbox(
            "Interviewer role",
            INTERVIEW_ROLES,
            index=INTERVIEW_ROLES.index(st.session_state.chat_role),
        )

        if selected_role != st.session_state.chat_role:
            st.session_state.chat_role = selected_role
            st.session_state.chat_messages = []

        chat_resume_text = st.text_area(
            "Resume context",
            value=st.session_state.last_resume_text,
            height=180,
            placeholder="Paste your resume text for a more personalized interview...",
        )

        chat_job_description = st.text_area(
            "Job context",
            value=st.session_state.last_job_description,
            height=180,
            placeholder="Paste the job description for role-specific questions...",
        )

        if st.button("Reset Interview"):
            st.session_state.chat_messages = []
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with chat_col:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.subheader(f"Live Interview: {st.session_state.chat_role}")
        st.markdown(
            '<div class="chat-note">Answer honestly. The interviewer will challenge vague answers and ask follow-ups.</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.chat_messages:
            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": (
                        f"Hi, I will be your {st.session_state.chat_role}. "
                        "To start, tell me briefly about yourself and the role you are targeting."
                    ),
                }
            )

        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        user_message = st.chat_input("Type your answer...")

        if user_message:
            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": user_message,
                }
            )

            with st.chat_message("user"):
                st.write(user_message)

            with st.chat_message("assistant"):
                with st.spinner("Interviewer is thinking..."):
                    try:
                        payload = {
                            "role": st.session_state.chat_role,
                            "message": user_message,
                            "resume_text": chat_resume_text,
                            "job_description": chat_job_description,
                            "history": st.session_state.chat_messages[:-1],
                        }

                        response = post_json("/api/interview-chat", payload, timeout=90)

                        if response.status_code != 200:
                            reply = f"Interview chat error: {response.text}"
                        else:
                            reply = response.json()["reply"]

                        st.write(reply)
                        st.session_state.chat_messages.append(
                            {
                                "role": "assistant",
                                "content": reply,
                            }
                        )

                    except requests.exceptions.RequestException:
                        st.error("Failed to connect to backend.")
                    except Exception as error:
                        st.error(f"Unexpected error: {str(error)}")

        st.markdown("</div>", unsafe_allow_html=True)
