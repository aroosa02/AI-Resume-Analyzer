from pathlib import Path
from uuid import uuid4

from docx import Document
from fastapi import HTTPException, UploadFile
from pypdf import PdfReader

from backend.config import settings


class ResumeParserService:
    @staticmethod
    async def validate_file(file: UploadFile) -> None:
        if not file.filename:
            raise HTTPException(status_code=400, detail="File name is missing.")

        extension = Path(file.filename).suffix.lower()

        if extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only PDF, DOCX, and TXT files are allowed.",
            )

    @staticmethod
    async def save_upload(file: UploadFile) -> Path:
        file_content = await file.read()

        if len(file_content) > settings.max_upload_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit.",
            )

        extension = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid4().hex}{extension}"
        file_path = settings.UPLOAD_DIR / unique_filename

        with open(file_path, "wb") as uploaded_file:
            uploaded_file.write(file_content)

        return file_path

    @staticmethod
    def extract_text_from_pdf(file_path: Path) -> str:
        try:
            reader = PdfReader(str(file_path))
            extracted_text = ""

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

            return extracted_text.strip()

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse PDF file: {str(error)}",
            )

    @staticmethod
    def extract_text_from_docx(file_path: Path) -> str:
        try:
            document = Document(str(file_path))
            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            return "\n".join(paragraphs).strip()

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse DOCX file: {str(error)}",
            )

    @staticmethod
    def extract_text_from_txt(file_path: Path) -> str:
        try:
            return file_path.read_text(encoding="utf-8", errors="ignore").strip()

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse TXT file: {str(error)}",
            )

    @classmethod
    async def parse_resume(cls, file: UploadFile) -> str:
        await cls.validate_file(file)
        file_path = await cls.save_upload(file)

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            extracted_text = cls.extract_text_from_pdf(file_path)
        elif extension == ".docx":
            extracted_text = cls.extract_text_from_docx(file_path)
        elif extension == ".txt":
            extracted_text = cls.extract_text_from_txt(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in resume.",
            )

        return extracted_text