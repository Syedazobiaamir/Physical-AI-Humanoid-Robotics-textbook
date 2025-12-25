"""
Google Gemini API client for embeddings and completions
"""
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing import List, Optional
import os
from dotenv import load_dotenv
from ..utils.logger import logger

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/text-embedding-004")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Safety settings for educational content - allow technical discussions
SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
}


class GeminiClient:
    """
    Google Gemini client for text generation and embeddings
    """

    def __init__(self):
        """Initialize Gemini client"""
        self.model_name = GEMINI_MODEL
        self.embedding_model = GEMINI_EMBEDDING_MODEL
        self.model = None
        if GEMINI_API_KEY:
            self.model = genai.GenerativeModel(self.model_name)

    def is_available(self) -> bool:
        """Check if Gemini is configured"""
        return GEMINI_API_KEY is not None and self.model is not None

    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for text using Gemini

        Args:
            text: Input text

        Returns:
            Embedding vector or None if failed
        """
        if not self.is_available():
            logger.warning("Gemini not configured, skipping embedding")
            return None

        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            embedding = result['embedding']
            logger.info(f"Generated Gemini embedding for text (length: {len(text)})")
            return embedding
        except Exception as e:
            logger.error(f"Error generating Gemini embedding: {str(e)}")
            return None

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of input texts

        Returns:
            List of embedding vectors
        """
        if not self.is_available():
            logger.warning("Gemini not configured, skipping batch embeddings")
            return []

        try:
            embeddings = []
            for text in texts:
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            logger.info(f"Generated {len(embeddings)} Gemini embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating batch Gemini embeddings: {str(e)}")
            return []

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        Generate text completion using Gemini

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text or None if failed
        """
        if not self.is_available():
            logger.warning("Gemini not configured, skipping completion")
            return None

        try:
            # Combine system prompt with user prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )

            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config,
                safety_settings=SAFETY_SETTINGS
            )

            # Check if response was blocked
            if not response.candidates:
                block_reason = getattr(response.prompt_feedback, 'block_reason', 'Unknown')
                logger.warning(f"Gemini response blocked: {block_reason}")
                return None

            # Check if candidate has content
            candidate = response.candidates[0]
            if not candidate.content or not candidate.content.parts:
                finish_reason = getattr(candidate, 'finish_reason', 'Unknown')
                logger.warning(f"Gemini candidate has no content. Finish reason: {finish_reason}")
                return None

            completion = candidate.content.parts[0].text
            logger.info(f"Generated Gemini completion successfully")
            return completion
        except Exception as e:
            logger.error(f"Error generating Gemini completion: {str(e)}")
            return None

    async def complete_with_context(
        self,
        query: str,
        context: List[str],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        Generate completion with context (for RAG)

        Args:
            query: User query
            context: List of context chunks
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated response or None if failed
        """
        try:
            # Build prompt with context - limit context to avoid token limits
            limited_context = context[:5]  # Limit to 5 context chunks
            context_str = "\n\n".join([f"Context {i+1}:\n{ctx[:2000]}" for i, ctx in enumerate(limited_context)])
            prompt = f"{context_str}\n\nQuestion: {query}\n\nPlease answer the question based on the context provided above."

            result = await self.complete(
                prompt=prompt,
                system_prompt=system_prompt or "You are a helpful assistant for a Physical AI and Humanoid Robotics textbook. Answer questions accurately based on the provided context.",
                temperature=temperature,
                max_tokens=max_tokens
            )

            if result:
                logger.info(f"RAG completion successful for query: {query[:50]}...")
            else:
                logger.warning(f"RAG completion returned None for query: {query[:50]}...")

            return result
        except Exception as e:
            logger.error(f"Error generating Gemini completion with context: {str(e)}")
            return None


# Singleton instance
gemini_client = GeminiClient()
