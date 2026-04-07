"""
Port: LLMProvider — Interface for Large Language Model narrative generation.

Allows the domain to request AI-generated text without coupling to any
specific provider (Anthropic, Google, OpenAI, Ollama, …).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class LLMProvider(ABC):
    """Abstract contract for LLM-based narrative generation."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable provider identifier (e.g. ``'claude'``, ``'gemini'``)."""
        ...

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int = 2000,
        system_context: Optional[str] = None,
    ) -> str:
        """Send a prompt and return the generated text.

        Parameters
        ----------
        prompt:
            The user/instruction prompt.
        temperature:
            Sampling temperature (lower = more deterministic).
        max_tokens:
            Maximum tokens in the response.
        system_context:
            Optional system-level instruction prepended to the prompt.

        Returns
        -------
        str
            Raw text response from the LLM.

        Raises
        ------
        ConnectionError
            If the provider API is unreachable.
        RuntimeError
            If the provider returns an error status.
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check whether the provider is configured and reachable."""
        ...
