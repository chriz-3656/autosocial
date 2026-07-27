import logging
from typing import Dict, Any, List
from autosocial.content.providers.base import AIProvider

logger = logging.getLogger(__name__)

class FallbackProvider(AIProvider):
    def __init__(self, providers: List[AIProvider]):
        if not providers:
            raise ValueError("FallbackProvider requires at least one AIProvider.")
        self.providers = providers

    def generate_content(self, prompt: str, system_prompt: str = "") -> str:
        last_exception = None
        for i, provider in enumerate(self.providers):
            provider_name = provider.__class__.__name__
            try:
                logger.info(f"Attempting generate_content with {provider_name}")
                return provider.generate_content(prompt, system_prompt)
            except Exception as e:
                logger.warning(f"{provider_name} failed: {e}. Falling back to next provider.")
                last_exception = e
                
        logger.error("All AI providers failed.")
        raise last_exception

    def generate_json(self, prompt: str, schema: Dict[str, Any], system_prompt: str = "") -> Dict[str, Any]:
        last_exception = None
        for i, provider in enumerate(self.providers):
            provider_name = provider.__class__.__name__
            try:
                logger.info(f"Attempting generate_json with {provider_name}")
                return provider.generate_json(prompt, schema, system_prompt)
            except Exception as e:
                logger.warning(f"{provider_name} failed: {e}. Falling back to next provider.")
                last_exception = e
                
        logger.error("All AI providers failed.")
        raise last_exception
