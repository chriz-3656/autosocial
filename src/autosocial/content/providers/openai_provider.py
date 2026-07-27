import json
from typing import Dict, Any
import openai
from autosocial.content.providers.base import AIProvider

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def generate_content(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content.strip()

    def generate_json(self, prompt: str, schema: Dict[str, Any], system_prompt: str = "") -> Dict[str, Any]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt + "\n\nProvide the output purely as valid JSON conforming strictly to the requested schema. No markdown wrappers."})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content.strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Failed to decode JSON from AI response")
            return {}
