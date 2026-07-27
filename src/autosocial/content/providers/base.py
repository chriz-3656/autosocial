from abc import ABC, abstractmethod
from typing import Dict, Any, List

class AIProvider(ABC):
    """
    Abstract interface for AI Providers (OpenAI, Groq, Gemini).
    """

    @abstractmethod
    def generate_content(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generate raw text content based on the prompt.
        """
        pass

    @abstractmethod
    def generate_json(self, prompt: str, schema: Dict[str, Any], system_prompt: str = "") -> Dict[str, Any]:
        """
        Generate structured JSON output conforming to the provided schema.
        """
        pass
