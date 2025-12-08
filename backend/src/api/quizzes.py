"""
Quiz API endpoints for chapter assessments
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from ..database.base import get_db
from ..auth.dependencies import get_current_user, get_current_user_optional
from ..services.quiz_service import QuizService
from ..utils.logger import logger

router = APIRouter()


# Pydantic Schemas
class QuestionOption(BaseModel):
    """Question option"""
    id: str
    text: str


class Question(BaseModel):
    """Quiz question (without answer for student view)"""
    id: str
    text: str
    options: List[QuestionOption]


class QuizResponse(BaseModel):
    """Quiz response schema"""
    quiz_id: str
    chapter_id: str
    title: str
    description: Optional[str] = None
    questions: List[Question]
    passing_score: int
    time_limit_minutes: Optional[int] = None
    created_at: Optional[str] = None


class AnswerSubmission(BaseModel):
    """Single answer submission"""
    question_id: str = Field(..., description="Question identifier")
    selected_option: str = Field(..., description="Selected option ID")


class QuizSubmitRequest(BaseModel):
    """Quiz submission request"""
    answers: List[AnswerSubmission] = Field(..., description="List of answers")


class QuestionResult(BaseModel):
    """Result for a single question"""
    question_id: str
    selected: Optional[str]
    correct: str
    is_correct: bool
    explanation: str


class QuizSubmitResponse(BaseModel):
    """Quiz submission response"""
    score: int
    correct_count: int
    total: int
    passed: bool
    passing_score: int
    results: List[QuestionResult]
    feedback: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    message: Optional[str] = None


@router.get("/{chapter_id}", response_model=QuizResponse)
async def get_chapter_quiz(
    chapter_id: str,
    current_user: Optional[dict] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    Get quiz for a specific chapter

    - **chapter_id**: Chapter identifier

    Returns the quiz without correct answers (for student-facing display).
    """
    try:
        service = QuizService(db)
        quiz = await service.get_quiz_by_chapter(chapter_id)

        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "quiz_not_found", "message": f"No quiz found for chapter: {chapter_id}"}
            )

        # Get quiz data without answers
        quiz_dict = quiz.to_dict(include_answers=False)

        return QuizResponse(
            quiz_id=quiz_dict["id"],
            chapter_id=quiz_dict["chapter_id"],
            title=quiz_dict["title"],
            description=quiz_dict["description"],
            questions=[
                Question(
                    id=q["id"],
                    text=q["text"],
                    options=[QuestionOption(**opt) for opt in q["options"]]
                )
                for q in quiz_dict["questions"]
            ],
            passing_score=quiz_dict["passing_score"],
            time_limit_minutes=quiz_dict["time_limit_minutes"],
            created_at=quiz_dict["created_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting quiz for chapter {chapter_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Failed to retrieve quiz"}
        )


@router.post("/{chapter_id}/submit", response_model=QuizSubmitResponse)
async def submit_quiz(
    chapter_id: str,
    request: QuizSubmitRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Submit quiz answers for grading

    - **chapter_id**: Chapter identifier
    - **answers**: List of answer submissions

    Requires authentication. Updates user progress with quiz score.
    """
    user_id = current_user.get("sub")

    try:
        service = QuizService(db)
        quiz = await service.get_quiz_by_chapter(chapter_id)

        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "quiz_not_found", "message": f"No quiz found for chapter: {chapter_id}"}
            )

        # Validate answer format
        answers = [
            {"question_id": a.question_id, "selected_option": a.selected_option}
            for a in request.answers
        ]

        # Grade the submission
        result = await service.submit_quiz(
            quiz_id=quiz.id,
            answers=answers,
            user_id=user_id
        )

        # Generate feedback message
        if result["passed"]:
            if result["score"] >= 90:
                feedback = "Excellent work! You've demonstrated strong understanding of this topic."
            elif result["score"] >= 80:
                feedback = "Great job! You have a solid grasp of the material."
            else:
                feedback = "Good work! You've passed the quiz. Review any missed questions to strengthen your understanding."
        else:
            feedback = f"Keep practicing! You need {result['passing_score']}% to pass. Review the explanations for the questions you missed."

        logger.info(f"Quiz submitted for chapter {chapter_id} by user {user_id}, score: {result['score']}")

        return QuizSubmitResponse(
            score=result["score"],
            correct_count=result["correct_count"],
            total=result["total"],
            passed=result["passed"],
            passing_score=result["passing_score"],
            results=[
                QuestionResult(
                    question_id=r["question_id"],
                    selected=r["selected"],
                    correct=r["correct"],
                    is_correct=r["is_correct"],
                    explanation=r["explanation"]
                )
                for r in result["results"]
            ],
            feedback=feedback
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_answers", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Error submitting quiz: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Failed to submit quiz"}
        )
