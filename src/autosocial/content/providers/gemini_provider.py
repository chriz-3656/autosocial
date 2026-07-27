import httpx
import json
from typing import Dict, Any
from autosocial.content.providers.base import AIProvider

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gemini-flash-latest"):
        self.api_key = api_key
        self.model = model
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def generate_content(self, prompt: str, system_prompt: str = "") -> str:
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key
        }
        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": f"System Instruction: {system_prompt}"}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})
        
        payload = {"contents": contents}
        
        with httpx.Client() as client:
            response = client.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    def generate_json(self, prompt: str, schema: Dict[str, Any], system_prompt: str = "") -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key
        }
        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": f"System Instruction: {system_prompt}"}]})
        contents.append({"role": "user", "parts": [{"text": prompt + "\n\nReturn ONLY valid JSON. No markdown wrappers."}]})
        
        # We can pass response_mime_type to Gemini 1.5
        payload = {
            "contents": contents,
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }
        
        with httpx.Client() as client:
            response = client.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            content = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            return json.loads(content)
