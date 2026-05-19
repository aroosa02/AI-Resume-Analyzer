from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.models.schemas import (
    AnalyzeResponse,
    HealthResponse,
    InterviewChatRequest,
    InterviewChatResponse,
    InterviewQuestionsResponse,
    QuestionRequest,
    StatusResponse,
)
from backend.services.ai_analyzer import AIAnalyzerService
from backend.services.interview_questions import InterviewQuestionService
from backend.services.resume_parser import ResumeParserService

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_analyzer = AIAnalyzerService()


@app.get("/", response_model=StatusResponse)
def root() -> StatusResponse:
    return StatusResponse(
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        status="running",
    )


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> AnalyzeResponse:
    if len(job_description.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Job description must contain at least 20 characters.",
        )

    resume_text = await ResumeParserService.parse_resume(resume)

    analysis_result = ai_analyzer.analyze_resume(
        resume_text=resume_text,
        job_description=job_description,
    )

    return AnalyzeResponse(**analysis_result)


@app.post(
    "/api/generate-questions",
    response_model=InterviewQuestionsResponse,
)
def generate_questions(
    request: QuestionRequest,
) -> InterviewQuestionsResponse:
    questions = InterviewQuestionService.generate_questions(
        resume_text=request.resume_text,
        job_description=request.job_description,
    )

    return InterviewQuestionsResponse(**questions)


@app.post("/api/interview-chat", response_model=InterviewChatResponse)
def interview_chat(
    request: InterviewChatRequest,
) -> InterviewChatResponse:
    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in request.history
    ]

    reply = ai_analyzer.generate_interview_reply(
        role=request.role,
        message=request.message,
        history=history,
        resume_text=request.resume_text,
        job_description=request.job_description,
    )

    return InterviewChatResponse(reply=reply)
