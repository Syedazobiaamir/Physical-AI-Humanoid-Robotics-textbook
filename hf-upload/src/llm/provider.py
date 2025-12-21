"""
Unified LLM provider that selects the best available backend
Priority: Gemini > Anthropic > OpenAI
"""
from typing import List, Optional
import os

# Load environment variables (optional - Vercel uses env vars directly)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not required in production

from ..utils.logger import logger

# Check which providers are available
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Preferred provider order (configurable)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto")  # auto, gemini, anthropic, openai
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "auto")  # auto, gemini, openai


class LLMProvider:
    """
    Unified LLM provider that automatically selects the best available backend
    """

    def __init__(self):
        """Initialize with available clients"""
        self.gemini_client = None
        self.anthropic_client = None
        self.openai_client = None

        # Lazy load clients based on available keys
        if GEMINI_API_KEY:
            try:
                from .gemini_client import gemini_client
                self.gemini_client = gemini_client
                logger.info("Gemini client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini: {e}")

        if ANTHROPIC_API_KEY:
            try:
                from .anthropic_client import anthropic_client
                self.anthropic_client = anthropic_client
                logger.info("Anthropic client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic: {e}")

        if OPENAI_API_KEY:
            try:
                from .openai_client import openai_client
                self.openai_client = openai_client
                logger.info("OpenAI client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")

    def get_available_providers(self) -> List[str]:
        """Get list of available LLM providers"""
        providers = []
        if self.gemini_client and self.gemini_client.is_available():
            providers.append("gemini")
        if self.anthropic_client:
            providers.append("anthropic")
        if self.openai_client:
            providers.append("openai")
        return providers

    def _get_completion_client(self):
        """Get the best available client for completions"""
        if LLM_PROVIDER == "gemini" and self.gemini_client:
            return self.gemini_client
        elif LLM_PROVIDER == "anthropic" and self.anthropic_client:
            return self.anthropic_client
        elif LLM_PROVIDER == "openai" and self.openai_client:
            return self.openai_client
        elif LLM_PROVIDER == "auto":
            # Priority: Gemini > Anthropic > OpenAI
            if self.gemini_client and self.gemini_client.is_available():
                return self.gemini_client
            elif self.anthropic_client:
                return self.anthropic_client
            elif self.openai_client:
                return self.openai_client
        return None

    def _get_embedding_client(self):
        """Get the best available client for embeddings"""
        if EMBEDDING_PROVIDER == "gemini" and self.gemini_client:
            return self.gemini_client
        elif EMBEDDING_PROVIDER == "openai" and self.openai_client:
            return self.openai_client
        elif EMBEDDING_PROVIDER == "auto":
            # Priority: Gemini > OpenAI (Anthropic doesn't have embeddings)
            if self.gemini_client and self.gemini_client.is_available():
                return self.gemini_client
            elif self.openai_client:
                return self.openai_client
        return None

    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using the best available provider"""
        client = self._get_embedding_client()
        if client is None:
            logger.error("No embedding provider available")
            return None
        return await client.generate_embedding(text)

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        client = self._get_embedding_client()
        if client is None:
            logger.error("No embedding provider available")
            return []
        return await client.generate_embeddings_batch(texts)

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """Generate completion using the best available provider"""
        client = self._get_completion_client()
        if client is None:
            logger.error("No LLM provider available")
            return None
        return await client.complete(prompt, system_prompt, temperature, max_tokens)

    async def complete_with_context(
        self,
        query: str,
        context: List[str],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """Generate completion with context (for RAG)"""
        client = self._get_completion_client()
        if client is None:
            logger.error("No LLM provider available")
            return None
        return await client.complete_with_context(query, context, system_prompt, temperature, max_tokens)


# Singleton instance
llm_provider = LLMProvider()
