from typing import Dict, Any
from autosocial.content.providers.base import AIProvider

class DummyProvider(AIProvider):
    def generate_content(self, prompt: str, system_prompt: str = "") -> str:
        if "caption" in prompt.lower():
            return "This is a lightning-fast, AI-generated caption built by AutoSocial!"
        return "5 Ways to Optimize Your Code Fast"

    def generate_json(self, prompt: str, schema: Dict[str, Any], system_prompt: str = "") -> Dict[str, Any]:
        return {"hashtags": ["#AutoSocial", "#Fast", "#Coding"]}
