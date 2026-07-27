import httpx
import json
from typing import Dict, Any
from autosocial.content.providers.base import AIProvider

class GroqProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def generate_content(self, prompt: str, system_prompt: str = "") -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {"model": self.model, "messages": messages}
        
        with httpx.Client() as client:
            response = client.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()

    def generate_json(self, prompt: str, schema: Dict[str, Any], system_prompt: str = "") -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt + "\n\nReturn ONLY valid JSON matching the requested schema. No markdown wrappers."})
        
        payload = {"model": self.model, "messages": messages, "response_format": {"type": "json_object"}}
        
        with httpx.Client() as client:
            response = client.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"].strip()
            return json.loads(content)
