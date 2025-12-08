"""
Content service for managing textbook chapters and content
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from ..models.chapter import Chapter
from ..utils.logger import logger
from ..utils.errors import NotFoundError


class ContentService:
    """
    Service for managing textbook content
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize content service

        Args:
            db: Database session
        """
        self.db = db

    async def get_chapter_by_id(self, chapter_id: str) -> Optional[Chapter]:
        """
        Get chapter by ID

        Args:
            chapter_id: Chapter identifier

        Returns:
            Chapter object or None if not found
        """
        try:
            result = await self.db.execute(
                select(Chapter).where(Chapter.id == chapter_id)
            )
            chapter = result.scalar_one_or_none()

            if chapter:
                logger.info(f"Retrieved chapter: {chapter.title}")
            else:
                logger.warning(f"Chapter not found: {chapter_id}")

            return chapter
        except Exception as e:
            logger.error(f"Error retrieving chapter: {str(e)}")
            return None

    async def get_chapters(
        self,
        module: Optional[str] = None,
        week_from: Optional[int] = None,
        week_to: Optional[int] = None
    ) -> List[Chapter]:
        """
        Get chapters with optional filters

        Args:
            module: Filter by module
            week_from: Filter by week range (start)
            week_to: Filter by week range (end)

        Returns:
            List of chapters
        """
        try:
            query = select(Chapter)
            filters = []

            if module:
                filters.append(Chapter.module == module)
            if week_from is not None:
                filters.append(Chapter.week >= week_from)
            if week_to is not None:
                filters.append(Chapter.week <= week_to)

            if filters:
                query = query.where(and_(*filters))

            query = query.order_by(Chapter.week)

            result = await self.db.execute(query)
            chapters = result.scalars().all()

            logger.info(f"Retrieved {len(chapters)} chapters")
            return list(chapters)
        except Exception as e:
            logger.error(f"Error retrieving chapters: {str(e)}")
            return []

    async def create_chapter(self, chapter_data: Dict[str, Any]) -> Chapter:
        """
        Create a new chapter

        Args:
            chapter_data: Chapter data dictionary

        Returns:
            Created chapter object
        """
        try:
            chapter = Chapter(**chapter_data)
            self.db.add(chapter)
            await self.db.commit()
            await self.db.refresh(chapter)

            logger.info(f"Created chapter: {chapter.title}")
            return chapter
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating chapter: {str(e)}")
            raise

    async def update_chapter(self, chapter_id: str, chapter_data: Dict[str, Any]) -> Chapter:
        """
        Update an existing chapter

        Args:
            chapter_id: Chapter identifier
            chapter_data: Chapter data to update

        Returns:
            Updated chapter object

        Raises:
            NotFoundError: If chapter not found
        """
        try:
            chapter = await self.get_chapter_by_id(chapter_id)
            if not chapter:
                raise NotFoundError(f"Chapter not found: {chapter_id}")

            for key, value in chapter_data.items():
                if hasattr(chapter, key):
                    setattr(chapter, key, value)

            await self.db.commit()
            await self.db.refresh(chapter)

            logger.info(f"Updated chapter: {chapter.title}")
            return chapter
        except NotFoundError:
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating chapter: {str(e)}")
            raise

    async def delete_chapter(self, chapter_id: str) -> bool:
        """
        Delete a chapter

        Args:
            chapter_id: Chapter identifier

        Returns:
            True if deleted successfully

        Raises:
            NotFoundError: If chapter not found
        """
        try:
            chapter = await self.get_chapter_by_id(chapter_id)
            if not chapter:
                raise NotFoundError(f"Chapter not found: {chapter_id}")

            await self.db.delete(chapter)
            await self.db.commit()

            logger.info(f"Deleted chapter: {chapter_id}")
            return True
        except NotFoundError:
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting chapter: {str(e)}")
            raise

    async def get_next_chapter(self, current_chapter_id: str) -> Optional[Chapter]:
        """
        Get the next chapter in sequence

        Args:
            current_chapter_id: Current chapter ID

        Returns:
            Next chapter or None if current is last
        """
        try:
            current = await self.get_chapter_by_id(current_chapter_id)
            if not current:
                return None

            result = await self.db.execute(
                select(Chapter)
                .where(Chapter.week > current.week)
                .order_by(Chapter.week)
                .limit(1)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting next chapter: {str(e)}")
            return None

    async def get_previous_chapter(self, current_chapter_id: str) -> Optional[Chapter]:
        """
        Get the previous chapter in sequence

        Args:
            current_chapter_id: Current chapter ID

        Returns:
            Previous chapter or None if current is first
        """
        try:
            current = await self.get_chapter_by_id(current_chapter_id)
            if not current:
                return None

            result = await self.db.execute(
                select(Chapter)
                .where(Chapter.week < current.week)
                .order_by(Chapter.week.desc())
                .limit(1)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting previous chapter: {str(e)}")
            return None
