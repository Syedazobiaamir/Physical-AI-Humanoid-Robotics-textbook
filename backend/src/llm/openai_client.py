"""
OpenAI API client for embeddings and completions
"""
from openai import AsyncOpenAI
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
from ..utils.logger import logger

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


class OpenAIClient:
    """
    OpenAI client for text generation and embeddings
    """

    def __init__(self):
        """Initialize OpenAI client"""
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.embedding_model = OPENAI_EMBEDDING_MODEL

    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for text

        Args:
            text: Input text

        Returns:
            Embedding vector or None if failed
        """
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            embedding = response.data[0].embedding
            logger.info(f"Generated embedding for text (length: {len(text)})")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return None

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of input texts

        Returns:
            List of embedding vectors
        """
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=texts
            )
            embeddings = [item.embedding for item in response.data]
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            return []

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        Generate text completion

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text or None if failed
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            completion = response.choices[0].message.content
            logger.info(f"Generated completion (tokens: {response.usage.total_tokens})")
            return completion
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
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
            # Build prompt with context
            context_str = "\n\n".join([f"Context {i+1}:\n{ctx}" for i, ctx in enumerate(context)])
            prompt = f"{context_str}\n\nQuestion: {query}\n\nPlease answer the question based on the context provided above."

            return await self.complete(
                prompt=prompt,
                system_prompt=system_prompt or "You are a helpful assistant for a Physical AI and Humanoid Robotics textbook. Answer questions accurately based on the provided context.",
                temperature=temperature,
                max_tokens=max_tokens
            )
        except Exception as e:
            logger.error(f"Error generating completion with context: {str(e)}")
            return None


# Singleton instance
openai_client = OpenAIClient()
