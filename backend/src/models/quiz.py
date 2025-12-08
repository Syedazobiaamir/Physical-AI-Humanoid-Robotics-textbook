"""
Quiz model for chapter assessments
"""
from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.orm import relationship
from ..database.base import Base
from .base import BaseModel


class Quiz(Base, BaseModel):
    """
    Quiz entity for chapter assessments

    Attributes:
        id: Unique quiz identifier
        chapter_id: Reference to associated chapter
        title: Quiz title
        description: Quiz description
        questions: JSON array of question objects
        passing_score: Minimum score to pass (default 60)
        time_limit_minutes: Optional time limit in minutes
        created_at: Creation timestamp
        updated_at: Last update timestamp

    Question Object Structure:
    {
        "id": "q1",
        "text": "Question text",
        "options": [
            {"id": "a", "text": "Option A"},
            {"id": "b", "text": "Option B"},
            {"id": "c", "text": "Option C"},
            {"id": "d", "text": "Option D"}
        ],
        "correct_answer": "a",
        "explanation": "Explanation of the correct answer"
    }
    """

    __tablename__ = "quizzes"

    chapter_id = Column(String(255), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(String(1000), nullable=True)
    questions = Column(JSON, nullable=False, default=[])
    passing_score = Column(Integer, nullable=False, default=60)
    time_limit_minutes = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Quiz(id={self.id}, chapter_id={self.chapter_id}, title={self.title})>"

    def to_dict(self, include_answers: bool = False):
        """
        Convert quiz to dictionary

        Args:
            include_answers: Whether to include correct answers in output
        """
        questions = self.questions or []

        if not include_answers:
            # Remove correct answers for student-facing responses
            questions = [
                {
                    "id": q.get("id"),
                    "text": q.get("text"),
                    "options": q.get("options", [])
                }
                for q in questions
            ]

        return {
            "id": self.id,
            "chapter_id": self.chapter_id,
            "title": self.title,
            "description": self.description,
            "questions": questions,
            "passing_score": self.passing_score,
            "time_limit_minutes": self.time_limit_minutes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def get_question_count(self) -> int:
        """Get the number of questions in the quiz"""
        return len(self.questions) if self.questions else 0

    def grade_submission(self, answers: list) -> dict:
        """
        Grade a quiz submission

        Args:
            answers: List of {"question_id": "q1", "selected_option": "a"} objects

        Returns:
            Grading result with score and detailed feedback
        """
        if not self.questions:
            return {"score": 0, "total": 0, "results": [], "passed": False}

        # Build answer lookup
        answer_lookup = {a.get("question_id"): a.get("selected_option") for a in answers}

        results = []
        correct_count = 0

        for question in self.questions:
            q_id = question.get("id")
            correct_answer = question.get("correct_answer")
            selected = answer_lookup.get(q_id)

            is_correct = selected == correct_answer

            if is_correct:
                correct_count += 1

            results.append({
                "question_id": q_id,
                "selected": selected,
                "correct": correct_answer,
                "is_correct": is_correct,
                "explanation": question.get("explanation", "")
            })

        total = len(self.questions)
        score = round((correct_count / total) * 100) if total > 0 else 0
        passed = score >= self.passing_score

        return {
            "score": score,
            "correct_count": correct_count,
            "total": total,
            "results": results,
            "passed": passed,
            "passing_score": self.passing_score
        }
