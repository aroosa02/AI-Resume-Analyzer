import re


class ScoringService:
    COMMON_SKILLS = [
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "nextjs",
        "fastapi",
        "django",
        "flask",
        "nodejs",
        "sql",
        "mongodb",
        "postgresql",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "git",
        "github",
        "html",
        "css",
        "tailwind",
        "machine learning",
        "data analysis",
        "communication",
        "leadership",
        "problem solving",
        "teamwork",
    ]

    @classmethod
    def normalize_text(
        cls,
        text: str,
    ) -> str:
        return text.lower().strip()

    @classmethod
    def extract_skills(
        cls,
        text: str,
    ) -> list[str]:
        normalized_text = cls.normalize_text(text)

        detected_skills = []

        for skill in cls.COMMON_SKILLS:
            pattern = (
                r"\b"
                + re.escape(skill)
                + r"\b"
            )

            if re.search(pattern, normalized_text):
                detected_skills.append(skill)

        return sorted(
            list(set(detected_skills))
        )

    @classmethod
    def calculate_match_score(
        cls,
        resume_skills: list[str],
        job_skills: list[str],
    ) -> int:
        if not job_skills:
            return 50

        matched_skills = set(
            resume_skills
        ).intersection(
            set(job_skills)
        )

        score = (
            len(matched_skills)
            / len(job_skills)
        ) * 100

        return round(score)

    @classmethod
    def get_missing_skills(
        cls,
        resume_skills: list[str],
        job_skills: list[str],
    ) -> list[str]:
        missing_skills = (
            set(job_skills)
            - set(resume_skills)
        )

        return sorted(
            list(missing_skills)
        )

    @classmethod
    def generate_strengths(
        cls,
        resume_skills: list[str],
    ) -> list[str]:
        strengths = []

        if len(resume_skills) >= 5:
            strengths.append(
                "Strong technical skill coverage."
            )

        if "communication" in resume_skills:
            strengths.append(
                "Good communication skills."
            )

        if "leadership" in resume_skills:
            strengths.append(
                "Leadership experience identified."
            )

        if "teamwork" in resume_skills:
            strengths.append(
                "Shows teamwork and collaboration ability."
            )

        if not strengths:
            strengths.append(
                "Basic technical profile detected."
            )

        return strengths

    @classmethod
    def generate_weaknesses(
        cls,
        missing_skills: list[str],
    ) -> list[str]:
        weaknesses = []

        if missing_skills:
            weaknesses.append(
                "Some required job skills are missing."
            )

        if len(missing_skills) > 5:
            weaknesses.append(
                "Large skill gap for the target role."
            )

        if not weaknesses:
            weaknesses.append(
                "No major weaknesses identified."
            )

        return weaknesses

    @classmethod
    def generate_recommendations(
        cls,
        missing_skills: list[str],
    ) -> list[str]:
        recommendations = []

        for skill in missing_skills[:5]:
            recommendations.append(
                f"Improve knowledge in {skill}."
            )

        if not recommendations:
            recommendations.append(
                "Resume aligns well with the job description."
            )

        return recommendations