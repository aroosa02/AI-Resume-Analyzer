from pydantic import BaseModel, Field


class StatusResponse(BaseModel):
    app_name: str
    version: str
    status: str


class HealthResponse(BaseModel):
    status: str = "healthy"


class ErrorResponse(BaseModel):
    detail: str


class QuestionRequest(BaseModel):
    resume_text: str = Field(..., min_length=20)
    job_description: str = Field(..., min_length=20)


class ChatMessage(BaseModel):
    role: str
    content: str


class InterviewChatRequest(BaseModel):
    role: str = Field(..., min_length=2)
    message: str = Field(..., min_length=1)
    resume_text: str | None = None
    job_description: str | None = None
    history: list[ChatMessage] = Field(default_factory=list)


class InterviewChatResponse(BaseModel):
    reply: str


class InterviewQuestionsResponse(BaseModel):
    technical_questions: list[str]
    hr_questions: list[str]
    role_based_questions: list[str]


class AnalyzeResponse(BaseModel):
    candidate_summary: str

    match_score: int = Field(
        ...,
        ge=0,
        le=100,
    )

    skills_found: list[str]

    missing_skills: list[str]

    missing_fields: list[str]

    strengths: list[str]

    weaknesses: list[str]

    recommendations: list[str]

    interview_questions: InterviewQuestionsResponse
