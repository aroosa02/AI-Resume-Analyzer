from backend.services.scoring import ScoringService


class InterviewQuestionService:
    @staticmethod
    def generate_hr_questions() -> list[str]:
        return [
            "Tell me about yourself.",
            "Why are you interested in this role?",
            "What are your biggest strengths?",
            "Describe a challenging situation you handled.",
            "Where do you see yourself in the next 3 years?",
        ]

    @staticmethod
    def generate_technical_questions(skills: list[str]) -> list[str]:
        if not skills:
            return [
                "Explain a technical project you worked on.",
                "How do you solve technical problems?",
                "Describe your strongest technical skill.",
            ]

        return [f"Explain your experience with {skill}." for skill in skills[:5]]

    @staticmethod
    def generate_role_based_questions(missing_skills: list[str]) -> list[str]:
        if not missing_skills:
            return [
                "Why are you a good fit for this role?",
                "How would you contribute to this team?",
                "Describe a similar project you completed.",
            ]

        return [
            f"How would you improve your knowledge in {skill}?"
            for skill in missing_skills[:5]
        ]

    @classmethod
    def generate_questions(
        cls,
        resume_text: str,
        job_description: str,
    ) -> dict[str, list[str]]:
        resume_skills = ScoringService.extract_skills(resume_text)
        job_skills = ScoringService.extract_skills(job_description)

        missing_skills = ScoringService.get_missing_skills(
            resume_skills=resume_skills,
            job_skills=job_skills,
        )

        return {
            "technical_questions": cls.generate_technical_questions(resume_skills),
            "hr_questions": cls.generate_hr_questions(),
            "role_based_questions": cls.generate_role_based_questions(missing_skills),
        }