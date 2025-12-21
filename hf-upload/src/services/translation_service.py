"""
Translation service for Urdu content translation with caching
"""
import hashlib
import re
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import os

from ..models.translation_cache import TranslationCache
from ..models.chapter import Chapter
from ..utils.logger import logger


class TranslationService:
    """
    Service for translating content to Urdu with caching support

    Features:
    - Caches translations to avoid redundant API calls
    - Preserves code blocks, headings, and markdown formatting
    - Handles technical term transliteration
    - Supports cache invalidation based on content changes
    """

    # Cache duration in days
    CACHE_DURATION_DAYS = 30

    # Technical terms to transliterate (keep in English with Urdu pronunciation)
    TECHNICAL_TERMS = {
        "ROS": "ROS (آر او ایس)",
        "ROS2": "ROS2 (آر او ایس ٹو)",
        "Python": "Python (پائتھون)",
        "API": "API (اے پی آئی)",
        "SDK": "SDK (ایس ڈی کے)",
        "CPU": "CPU (سی پی یو)",
        "GPU": "GPU (جی پی یو)",
        "SLAM": "SLAM (سلیم)",
        "PID": "PID (پی آئی ڈی)",
        "IMU": "IMU (آئی ایم یو)",
        "LiDAR": "LiDAR (لائیڈار)",
        "RGB": "RGB (آر جی بی)",
        "TCP/IP": "TCP/IP (ٹی سی پی/آئی پی)",
        "HTTP": "HTTP (ایچ ٹی ٹی پی)",
        "JSON": "JSON (جے سون)",
        "XML": "XML (ایکس ایم ایل)",
        "YAML": "YAML (یامل)",
        "Git": "Git (گٹ)",
        "Docker": "Docker (ڈوکر)",
        "Kubernetes": "Kubernetes (کوبرنیٹس)",
        "AI": "AI (مصنوعی ذہانت)",
        "ML": "ML (مشین لرننگ)",
        "DL": "DL (ڈیپ لرننگ)",
        "RL": "RL (ریانفورسمنٹ لرننگ)",
        "CNN": "CNN (سی این این)",
        "RNN": "RNN (آر این این)",
        "LSTM": "LSTM (ایل ایس ٹی ایم)",
        "Transformer": "Transformer (ٹرانسفارمر)",
        "OpenAI": "OpenAI (اوپن اے آئی)",
        "Anthropic": "Anthropic (اینتھروپک)",
        "Claude": "Claude (کلاڈ)",
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

    def _compute_content_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content for cache invalidation"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _preserve_code_blocks(self, content: str) -> tuple[str, dict]:
        """
        Extract and preserve code blocks before translation

        Returns:
            Tuple of (content with placeholders, mapping of placeholders to code blocks)
        """
        code_blocks = {}
        placeholder_pattern = "<<<CODE_BLOCK_{0}>>>"

        # Match fenced code blocks
        code_block_regex = r'```(\w+)?\n(.*?)```'
        matches = list(re.finditer(code_block_regex, content, re.DOTALL))

        processed_content = content
        for i, match in enumerate(reversed(matches)):
            placeholder = placeholder_pattern.format(len(matches) - 1 - i)
            code_blocks[placeholder] = match.group(0)
            processed_content = processed_content[:match.start()] + placeholder + processed_content[match.end():]

        return processed_content, code_blocks

    def _restore_code_blocks(self, content: str, code_blocks: dict) -> str:
        """Restore code blocks from placeholders"""
        for placeholder, code_block in code_blocks.items():
            content = content.replace(placeholder, code_block)
        return content

    def _preserve_headings(self, content: str) -> tuple[str, dict]:
        """
        Preserve markdown headings for consistent formatting

        Returns:
            Tuple of (content with placeholders, mapping of placeholders to headings)
        """
        headings = {}
        placeholder_pattern = "<<<HEADING_{0}>>>"

        # Match markdown headings
        heading_regex = r'^(#{1,6})\s+(.+)$'

        lines = content.split('\n')
        processed_lines = []

        heading_count = 0
        for line in lines:
            match = re.match(heading_regex, line)
            if match:
                placeholder = placeholder_pattern.format(heading_count)
                headings[placeholder] = {
                    'level': match.group(1),
                    'text': match.group(2)
                }
                processed_lines.append(f"{match.group(1)} {placeholder}")
                heading_count += 1
            else:
                processed_lines.append(line)

        return '\n'.join(processed_lines), headings

    def _apply_technical_terms(self, content: str) -> str:
        """Apply transliteration for technical terms"""
        for term, transliteration in self.TECHNICAL_TERMS.items():
            # Use word boundaries to avoid partial matches
            pattern = rf'\b{re.escape(term)}\b'
            content = re.sub(pattern, transliteration, content, flags=re.IGNORECASE)
        return content

    async def get_cached_translation(self, chapter_id: str, content_hash: str) -> Optional[str]:
        """
        Get cached translation if available and not expired

        Args:
            chapter_id: Chapter identifier
            content_hash: Hash of original content

        Returns:
            Cached Urdu content if available, None otherwise
        """
        try:
            result = await self.db.execute(
                select(TranslationCache).where(
                    TranslationCache.chapter_id == chapter_id,
                    TranslationCache.content_hash == content_hash
                )
            )
            cache_entry = result.scalar_one_or_none()

            if cache_entry and not cache_entry.is_expired():
                logger.info(f"Cache hit for chapter {chapter_id}")
                return cache_entry.urdu_content

            # Delete expired entry if exists
            if cache_entry and cache_entry.is_expired():
                await self.db.delete(cache_entry)
                await self.db.commit()
                logger.info(f"Deleted expired cache for chapter {chapter_id}")

            return None
        except Exception as e:
            logger.error(f"Error getting cached translation: {str(e)}")
            return None

    async def cache_translation(self, chapter_id: str, content_hash: str, urdu_content: str) -> None:
        """
        Cache a translation for future use

        Args:
            chapter_id: Chapter identifier
            content_hash: Hash of original content
            urdu_content: Translated Urdu content
        """
        try:
            import uuid

            # Delete any existing cache for this chapter/hash combination
            await self.db.execute(
                delete(TranslationCache).where(
                    TranslationCache.chapter_id == chapter_id,
                    TranslationCache.content_hash == content_hash
                )
            )

            # Create new cache entry
            cache_entry = TranslationCache(
                id=str(uuid.uuid4()),
                chapter_id=chapter_id,
                content_hash=content_hash,
                urdu_content=urdu_content,
                expires_at=datetime.now(timezone.utc) + timedelta(days=self.CACHE_DURATION_DAYS)
            )
            self.db.add(cache_entry)
            await self.db.commit()
            logger.info(f"Cached translation for chapter {chapter_id}")
        except Exception as e:
            logger.error(f"Error caching translation: {str(e)}")
            await self.db.rollback()

    async def translate_to_urdu(
        self,
        content: str,
        chapter_id: Optional[str] = None,
        preserve_formatting: bool = True
    ) -> tuple[str, bool]:
        """
        Translate content to Urdu with caching

        Args:
            content: Content to translate
            chapter_id: Optional chapter ID for caching
            preserve_formatting: Whether to preserve code blocks and markdown

        Returns:
            Tuple of (translated content, cache_hit boolean)
        """
        content_hash = self._compute_content_hash(content)

        # Check cache first
        if chapter_id:
            cached = await self.get_cached_translation(chapter_id, content_hash)
            if cached:
                return cached, True

        # Preserve code blocks only (headings should be translated)
        code_blocks = {}

        processed_content = content
        if preserve_formatting:
            # Only preserve code blocks - they should NOT be translated
            processed_content, code_blocks = self._preserve_code_blocks(processed_content)
            # NOTE: We don't preserve headings anymore - they should be fully translated to Urdu

        # Perform translation
        translated = await self._translate_with_llm(processed_content)

        # Restore code blocks only (they stay in English)
        if preserve_formatting and code_blocks:
            translated = self._restore_code_blocks(translated, code_blocks)

        # Apply technical term transliterations
        translated = self._apply_technical_terms(translated)

        # Cache the result
        if chapter_id:
            await self.cache_translation(chapter_id, content_hash, translated)

        return translated, False

    async def _translate_with_llm(self, content: str) -> str:
        """
        Translate content using LLM API

        Uses Gemini, OpenAI, or Anthropic API for translation.
        Falls back to simple placeholder if no API key is configured.
        """
        try:
            if self.gemini_api_key:
                return await self._translate_with_gemini(content)
            elif self.openai_api_key:
                return await self._translate_with_openai(content)
            elif self.anthropic_api_key:
                return await self._translate_with_anthropic(content)
            else:
                # Return placeholder translation for demo/development
                logger.warning("No LLM API key configured, returning placeholder translation")
                return self._placeholder_translation(content)
        except Exception as e:
            logger.error(f"LLM translation error: {str(e)}")
            return self._placeholder_translation(content)

    async def _translate_with_gemini(self, content: str) -> str:
        """Translate using Google Gemini API with chunking for long content"""
        import google.generativeai as genai

        genai.configure(api_key=self.gemini_api_key)
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))

        # For long content, split into chunks and translate each
        # Use smaller chunks to ensure complete translations
        MAX_CHUNK_SIZE = 2000  # Characters per chunk (smaller for better quality)

        if len(content) <= MAX_CHUNK_SIZE:
            # Short content - translate directly
            return await self._translate_chunk_gemini(model, content)
        else:
            # Long content - split into paragraphs and translate in chunks
            logger.info(f"Long content detected ({len(content)} chars), splitting into chunks")
            return await self._translate_in_chunks_gemini(model, content, MAX_CHUNK_SIZE)

    async def _translate_chunk_gemini(self, model, content: str) -> str:
        """Translate a single chunk using Gemini"""
        import google.generativeai as genai

        prompt = f"""آپ ایک ماہر پیشہ ور اردو مترجم ہیں۔ آپ کا کام انگریزی متن کو مکمل طور پر اردو میں ترجمہ کرنا ہے۔

## سخت قواعد - لازمی پیروی کریں:

### 1. ہر لفظ کا ترجمہ کریں
- ہر انگریزی لفظ کا اردو میں ترجمہ ہونا چاہیے
- کوئی انگریزی جملہ یا فقرہ نہ چھوڑیں
- "Introduction", "Chapter", "Learning", "Overview" جیسے عام الفاظ کا بھی ترجمہ کریں

### 2. صرف ٹیکنیکل اصطلاحات کے لیے
Python, ROS, API, CPU, GPU جیسی ٹیکنیکل اصطلاحات کے لیے یہ فارمیٹ استعمال کریں:
انگریزی (اردو تلفظ) - مثال: Python (پائتھون)، API (اے پی آئی)

### 3. مارک ڈاؤن فارمیٹنگ
- عنوانات (#, ##, ###) کا متن اردو میں ترجمہ کریں
- بولڈ (**text**) اور اٹیلک (*text*) فارمیٹنگ رکھیں
- فہرستیں (-, 1., 2.) رکھیں
- کوڈ بلاکس (<<<CODE_BLOCK_N>>>) کو بالکل ایسے ہی رکھیں

### 4. غلط اور درست مثالیں

❌ غلط: "## Introduction to Robotics" → "## Introduction روبوٹکس کا"
✅ درست: "## Introduction to Robotics" → "## روبوٹکس کا تعارف"

❌ غلط: "This chapter covers machine learning" → "This chapter میں machine learning ہے"
✅ درست: "This chapter covers machine learning" → "اس باب میں مشین لرننگ (machine learning) شامل ہے"

❌ غلط: "Learning Objectives" → "Learning Objectives"
✅ درست: "Learning Objectives" → "سیکھنے کے مقاصد"

---

انگریزی متن:
{content}

---

مکمل اردو ترجمہ (ہر لفظ اردو میں):"""

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=16384,  # Maximum output for complete translation
                temperature=0.1,  # Lower temperature for accuracy and consistency
            )
        )
        return response.text

    async def _translate_in_chunks_gemini(self, model, content: str, max_chunk_size: int) -> str:
        """Split long content into chunks and translate each"""
        # Split by double newlines (paragraphs)
        paragraphs = content.split('\n\n')

        chunks = []
        current_chunk = ""

        for para in paragraphs:
            # If adding this paragraph exceeds the limit, save current chunk and start new one
            if len(current_chunk) + len(para) + 2 > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                current_chunk = current_chunk + "\n\n" + para if current_chunk else para

        # Don't forget the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        logger.info(f"Translating {len(chunks)} chunks")

        # Translate each chunk
        translated_chunks = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Translating chunk {i+1}/{len(chunks)} ({len(chunk)} chars)")
            translated = await self._translate_chunk_gemini(model, chunk)
            translated_chunks.append(translated)

        # Combine all translated chunks
        return '\n\n'.join(translated_chunks)

    async def _translate_with_openai(self, content: str) -> str:
        """Translate using OpenAI API"""
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o",
                    "messages": [
                        {
                            "role": "system",
                            "content": """آپ ایک ماہر پیشہ ور اردو مترجم ہیں۔ ہر انگریزی لفظ کا اردو میں ترجمہ کریں۔

سخت قواعد:
1. ہر لفظ اردو میں - کوئی انگریزی نہ چھوڑیں
2. صرف ٹیکنیکل اصطلاحات (Python, API, ROS) کے لیے: انگریزی (اردو تلفظ)
3. "Introduction" → "تعارف"، "Chapter" → "باب"، "Learning" → "سیکھنا"
4. مارک ڈاؤن فارمیٹنگ (#, **, *) رکھیں
5. کوڈ بلاکس (<<<CODE_BLOCK_N>>>) کو ایسے ہی رکھیں

❌ غلط: "## Introduction" → "## Introduction"
✅ درست: "## Introduction" → "## تعارف"

❌ غلط: "This is about robotics" → "This is about روبوٹکس"
✅ درست: "This is about robotics" → "یہ روبوٹکس (robotics) کے بارے میں ہے" """
                        },
                        {
                            "role": "user",
                            "content": f"مکمل اردو ترجمہ کریں (ہر لفظ اردو میں):\n\n{content}"
                        }
                    ],
                    "temperature": 0.1
                },
                timeout=60.0
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                raise Exception(f"OpenAI API error: {response.status_code}")

    async def _translate_with_anthropic(self, content: str) -> str:
        """Translate using Anthropic API"""
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.anthropic_api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 8192,
                    "system": """آپ ایک ماہر پیشہ ور اردو مترجم ہیں۔ ہر انگریزی لفظ کا اردو میں ترجمہ کریں۔

سخت قواعد:
1. ہر لفظ اردو میں - کوئی انگریزی نہ چھوڑیں
2. صرف ٹیکنیکل اصطلاحات (Python, API, ROS) کے لیے: انگریزی (اردو تلفظ)
3. "Introduction" → "تعارف"، "Chapter" → "باب"، "Learning" → "سیکھنا"
4. مارک ڈاؤن فارمیٹنگ (#, **, *) رکھیں
5. کوڈ بلاکس (<<<CODE_BLOCK_N>>>) کو ایسے ہی رکھیں

❌ غلط: "## Introduction" → "## Introduction"
✅ درست: "## Introduction" → "## تعارف"

❌ غلط: "This is about robotics" → "This is about روبوٹکس"
✅ درست: "This is about robotics" → "یہ روبوٹکس (robotics) کے بارے میں ہے" """,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"مکمل اردو ترجمہ کریں (ہر لفظ اردو میں):\n\n{content}"
                        }
                    ]
                },
                timeout=60.0
            )

            if response.status_code == 200:
                data = response.json()
                return data["content"][0]["text"]
            else:
                raise Exception(f"Anthropic API error: {response.status_code}")

    def _placeholder_translation(self, content: str) -> str:
        """
        Generate placeholder translation for development/demo

        This is used when no LLM API key is configured.
        """
        # Add RTL markers and simple prefix to indicate translation
        lines = content.split('\n')
        translated_lines = []

        for line in lines:
            if line.strip():
                # Add Urdu prefix to indicate this is a placeholder
                translated_lines.append(f"[اردو] {line}")
            else:
                translated_lines.append(line)

        return '\n'.join(translated_lines)

    async def get_chapter_translation(self, chapter_id: str) -> Optional[dict]:
        """
        Get the latest cached translation for a chapter

        Args:
            chapter_id: Chapter identifier

        Returns:
            Dictionary with urdu_content and last_updated, or None if not found
        """
        try:
            result = await self.db.execute(
                select(TranslationCache)
                .where(TranslationCache.chapter_id == chapter_id)
                .order_by(TranslationCache.created_at.desc())
            )
            cache_entry = result.scalars().first()

            if cache_entry and not cache_entry.is_expired():
                return {
                    "urdu_content": cache_entry.urdu_content,
                    "last_updated": cache_entry.created_at.isoformat() if cache_entry.created_at else None
                }

            return None
        except Exception as e:
            logger.error(f"Error getting chapter translation: {str(e)}")
            return None

    async def cleanup_expired_cache(self) -> int:
        """
        Clean up expired cache entries

        Returns:
            Number of entries deleted
        """
        try:
            result = await self.db.execute(
                delete(TranslationCache).where(
                    TranslationCache.expires_at < datetime.now(timezone.utc)
                )
            )
            await self.db.commit()
            deleted_count = result.rowcount
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} expired translation cache entries")
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning up cache: {str(e)}")
            await self.db.rollback()
            return 0
