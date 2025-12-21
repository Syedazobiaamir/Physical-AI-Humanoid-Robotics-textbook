"""
Anthropic Claude API client for fallback completions
"""
from anthropic import AsyncAnthropic
from typing import List, Optional
import os
from dotenv import load_dotenv
from ..utils.logger import logger

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5-20251101")


class AnthropicClient:
    """
    Anthropic Claude client for text generation (fallback)
    """

    def __init__(self):
        """Initialize Anthropic client"""
        self.client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        self.model = ANTHROPIC_MODEL

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        Generate text completion with Claude

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text or None if failed
        """
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt or "You are a helpful assistant for a Physical AI and Humanoid Robotics textbook.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            completion = response.content[0].text
            logger.info(f"Generated Claude completion (tokens: {response.usage.input_tokens + response.usage.output_tokens})")
            return completion
        except Exception as e:
            logger.error(f"Error generating Claude completion: {str(e)}")
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
        Generate completion with context using Claude (for RAG fallback)

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
            logger.error(f"Error generating Claude completion with context: {str(e)}")
            return None


# Singleton instance
anthropic_client = AnthropicClient()
