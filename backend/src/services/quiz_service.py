"""
Quiz service for managing chapter quizzes
"""
from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from ..models.quiz import Quiz
from ..models.progress_tracking import ProgressTracking
from ..utils.logger import logger


class QuizService:
    """
    Service for managing chapter quizzes

    Features:
    - CRUD operations for quizzes
    - Quiz grading with detailed feedback
    - Progress tracking integration
    - Quiz generation support
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_quiz_by_chapter(self, chapter_id: str) -> Optional[Quiz]:
        """
        Get quiz for a specific chapter

        Args:
            chapter_id: Chapter identifier

        Returns:
            Quiz object if found, None otherwise
        """
        try:
            result = await self.db.execute(
                select(Quiz).where(Quiz.chapter_id == chapter_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting quiz for chapter {chapter_id}: {str(e)}")
            return None

    async def get_quiz_by_id(self, quiz_id: str) -> Optional[Quiz]:
        """
        Get quiz by its ID

        Args:
            quiz_id: Quiz identifier

        Returns:
            Quiz object if found, None otherwise
        """
        try:
            result = await self.db.execute(
                select(Quiz).where(Quiz.id == quiz_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting quiz {quiz_id}: {str(e)}")
            return None

    async def create_quiz(
        self,
        chapter_id: str,
        title: str,
        questions: List[Dict],
        description: Optional[str] = None,
        passing_score: int = 60,
        time_limit_minutes: Optional[int] = None
    ) -> Quiz:
        """
        Create a new quiz

        Args:
            chapter_id: Associated chapter ID
            title: Quiz title
            questions: List of question objects
            description: Optional quiz description
            passing_score: Minimum passing score (default 60%)
            time_limit_minutes: Optional time limit

        Returns:
            Created Quiz object
        """
        try:
            quiz = Quiz(
                id=str(uuid.uuid4()),
                chapter_id=chapter_id,
                title=title,
                description=description,
                questions=questions,
                passing_score=passing_score,
                time_limit_minutes=time_limit_minutes
            )
            self.db.add(quiz)
            await self.db.commit()
            await self.db.refresh(quiz)
            logger.info(f"Created quiz for chapter {chapter_id}")
            return quiz
        except Exception as e:
            logger.error(f"Error creating quiz: {str(e)}")
            await self.db.rollback()
            raise

    async def update_quiz(
        self,
        quiz_id: str,
        questions: Optional[List[Dict]] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        passing_score: Optional[int] = None,
        time_limit_minutes: Optional[int] = None
    ) -> Optional[Quiz]:
        """
        Update an existing quiz

        Args:
            quiz_id: Quiz identifier
            questions: Updated questions (optional)
            title: Updated title (optional)
            description: Updated description (optional)
            passing_score: Updated passing score (optional)
            time_limit_minutes: Updated time limit (optional)

        Returns:
            Updated Quiz object or None if not found
        """
        try:
            quiz = await self.get_quiz_by_id(quiz_id)
            if not quiz:
                return None

            if questions is not None:
                quiz.questions = questions
            if title is not None:
                quiz.title = title
            if description is not None:
                quiz.description = description
            if passing_score is not None:
                quiz.passing_score = passing_score
            if time_limit_minutes is not None:
                quiz.time_limit_minutes = time_limit_minutes

            await self.db.commit()
            await self.db.refresh(quiz)
            logger.info(f"Updated quiz {quiz_id}")
            return quiz
        except Exception as e:
            logger.error(f"Error updating quiz: {str(e)}")
            await self.db.rollback()
            return None

    async def submit_quiz(
        self,
        quiz_id: str,
        answers: List[Dict],
        user_id: Optional[str] = None
    ) -> Dict:
        """
        Submit and grade a quiz

        Args:
            quiz_id: Quiz identifier
            answers: List of answer objects {"question_id": "q1", "selected_option": "a"}
            user_id: Optional user ID for progress tracking

        Returns:
            Grading result with score and feedback
        """
        try:
            quiz = await self.get_quiz_by_id(quiz_id)
            if not quiz:
                raise ValueError(f"Quiz not found: {quiz_id}")

            # Grade the submission
            result = quiz.grade_submission(answers)

            # Update progress if user is authenticated
            if user_id:
                await self._update_progress(user_id, quiz.chapter_id, result["score"])

            logger.info(f"Quiz {quiz_id} submitted, score: {result['score']}")
            return result
        except Exception as e:
            logger.error(f"Error submitting quiz: {str(e)}")
            raise

    async def _update_progress(self, user_id: str, chapter_id: str, score: int) -> None:
        """
        Update user progress after quiz submission

        Args:
            user_id: User identifier
            chapter_id: Chapter identifier
            score: Quiz score
        """
        try:
            # Find existing progress
            result = await self.db.execute(
                select(ProgressTracking).where(
                    ProgressTracking.user_id == user_id,
                    ProgressTracking.chapter_id == chapter_id
                )
            )
            progress = result.scalar_one_or_none()

            from datetime import datetime

            if progress:
                progress.quiz_score = score
                progress.status = "reviewed"
                progress.completed_at = datetime.utcnow()
            else:
                progress = ProgressTracking(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    chapter_id=chapter_id,
                    status="reviewed",
                    quiz_score=score,
                    completed_at=datetime.utcnow()
                )
                self.db.add(progress)

            await self.db.commit()
            logger.info(f"Updated progress for user {user_id}, chapter {chapter_id}")
        except Exception as e:
            logger.error(f"Error updating progress: {str(e)}")
            # Don't raise - progress update failure shouldn't fail quiz submission

    async def get_all_quizzes(self) -> List[Quiz]:
        """Get all quizzes"""
        try:
            result = await self.db.execute(select(Quiz))
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting all quizzes: {str(e)}")
            return []

    async def delete_quiz(self, quiz_id: str) -> bool:
        """
        Delete a quiz

        Args:
            quiz_id: Quiz identifier

        Returns:
            True if deleted, False if not found
        """
        try:
            quiz = await self.get_quiz_by_id(quiz_id)
            if not quiz:
                return False

            await self.db.delete(quiz)
            await self.db.commit()
            logger.info(f"Deleted quiz {quiz_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting quiz: {str(e)}")
            await self.db.rollback()
            return False


# Sample quiz data for testing/seeding
SAMPLE_QUIZ_DATA = {
    "week-1-intro": {
        "title": "Week 1: Introduction to Physical AI Quiz",
        "description": "Test your understanding of Physical AI fundamentals and ROS2 basics",
        "questions": [
            {
                "id": "q1",
                "text": "What is the primary purpose of ROS2 in robotics applications?",
                "options": [
                    {"id": "a", "text": "Web development framework"},
                    {"id": "b", "text": "Robot middleware for communication and tools"},
                    {"id": "c", "text": "Database management system"},
                    {"id": "d", "text": "Machine learning library"}
                ],
                "correct_answer": "b",
                "explanation": "ROS2 (Robot Operating System 2) is a middleware framework that provides communication infrastructure, tools, and libraries for building robot applications."
            },
            {
                "id": "q2",
                "text": "Which communication pattern in ROS2 allows for asynchronous data streaming?",
                "options": [
                    {"id": "a", "text": "Services"},
                    {"id": "b", "text": "Actions"},
                    {"id": "c", "text": "Topics (Publisher/Subscriber)"},
                    {"id": "d", "text": "Parameters"}
                ],
                "correct_answer": "c",
                "explanation": "Topics use the publisher/subscriber pattern for asynchronous, streaming communication between nodes."
            },
            {
                "id": "q3",
                "text": "What distinguishes 'Physical AI' from traditional robotics?",
                "options": [
                    {"id": "a", "text": "Use of more expensive hardware"},
                    {"id": "b", "text": "Integration of AI/ML for adaptive behavior in physical environments"},
                    {"id": "c", "text": "Faster processing speeds"},
                    {"id": "d", "text": "Smaller robot sizes"}
                ],
                "correct_answer": "b",
                "explanation": "Physical AI combines robotics with AI/ML to create systems that can learn, adapt, and make decisions in real-world physical environments."
            },
            {
                "id": "q4",
                "text": "Which ROS2 concept provides request/response style communication?",
                "options": [
                    {"id": "a", "text": "Topics"},
                    {"id": "b", "text": "Services"},
                    {"id": "c", "text": "Parameters"},
                    {"id": "d", "text": "Launch files"}
                ],
                "correct_answer": "b",
                "explanation": "Services provide synchronous request/response communication, where a client sends a request and waits for a response from a server."
            },
            {
                "id": "q5",
                "text": "What is a ROS2 node?",
                "options": [
                    {"id": "a", "text": "A hardware component"},
                    {"id": "b", "text": "A single executable that performs computation"},
                    {"id": "c", "text": "A network router"},
                    {"id": "d", "text": "A type of sensor"}
                ],
                "correct_answer": "b",
                "explanation": "A ROS2 node is a process that performs computation. Nodes communicate with each other through topics, services, and actions."
            }
        ]
    },
    "week-5-computer-vision": {
        "title": "Week 5: Computer Vision for Robotics Quiz",
        "description": "Test your knowledge of perception systems and computer vision in robotics",
        "questions": [
            {
                "id": "q1",
                "text": "What does SLAM stand for in robotics?",
                "options": [
                    {"id": "a", "text": "Simultaneous Localization and Mapping"},
                    {"id": "b", "text": "System Learning and Monitoring"},
                    {"id": "c", "text": "Sensor Layout and Management"},
                    {"id": "d", "text": "Sequential Location Analysis Method"}
                ],
                "correct_answer": "a",
                "explanation": "SLAM (Simultaneous Localization and Mapping) is a technique where a robot builds a map of its environment while simultaneously tracking its location within that map."
            },
            {
                "id": "q2",
                "text": "Which sensor provides depth information for 3D perception?",
                "options": [
                    {"id": "a", "text": "Standard RGB camera"},
                    {"id": "b", "text": "Microphone"},
                    {"id": "c", "text": "RGB-D camera or LiDAR"},
                    {"id": "d", "text": "Temperature sensor"}
                ],
                "correct_answer": "c",
                "explanation": "RGB-D cameras combine color images with depth information, and LiDAR uses laser pulses to measure distances, both providing 3D perception capabilities."
            },
            {
                "id": "q3",
                "text": "What is the primary advantage of using CNNs for object detection?",
                "options": [
                    {"id": "a", "text": "Lower computational requirements"},
                    {"id": "b", "text": "Automatic feature extraction from raw images"},
                    {"id": "c", "text": "No training data required"},
                    {"id": "d", "text": "Works without cameras"}
                ],
                "correct_answer": "b",
                "explanation": "CNNs automatically learn relevant features from training data, eliminating the need for manual feature engineering."
            },
            {
                "id": "q4",
                "text": "Which library is commonly used for computer vision in ROS2?",
                "options": [
                    {"id": "a", "text": "NumPy"},
                    {"id": "b", "text": "OpenCV (cv_bridge)"},
                    {"id": "c", "text": "Matplotlib"},
                    {"id": "d", "text": "Pandas"}
                ],
                "correct_answer": "b",
                "explanation": "OpenCV integrated with ROS2 through cv_bridge is the standard library for image processing and computer vision tasks in robot applications."
            },
            {
                "id": "q5",
                "text": "What is point cloud data commonly used for?",
                "options": [
                    {"id": "a", "text": "Audio processing"},
                    {"id": "b", "text": "3D environment representation and obstacle detection"},
                    {"id": "c", "text": "Network communication"},
                    {"id": "d", "text": "Motor control"}
                ],
                "correct_answer": "b",
                "explanation": "Point clouds represent 3D spatial data from sensors like LiDAR, used for environment mapping, object detection, and obstacle avoidance."
            }
        ]
    }
}
