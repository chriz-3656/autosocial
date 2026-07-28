from typing import List, Dict, Any
from autosocial.content.providers.base import AIProvider

class ContentPipeline:
    def __init__(self, provider: AIProvider):
        self.provider = provider
        
    def generate_concept(self, category: str, memory_topics: List[str]) -> str:
        prompt = f"Generate a unique Instagram post concept about {category}."
        if memory_topics:
            prompt += f" Do not use these recent topics: {', '.join(memory_topics)}"
        return self.provider.generate_content(prompt, system_prompt="You are a creative director.")
        
    def generate_caption(self, concept: str, brand_voice: str) -> str:
        prompt = f"Write an engaging Instagram caption for this concept: {concept}"
        sys_prompt = f"You are a social media manager. Use a {brand_voice} voice."
        return self.provider.generate_content(prompt, system_prompt=sys_prompt)
        
    def generate_quote(self, concept: str) -> str:
        prompt = f"Extract or write a powerful, short quote (maximum 15 words) that summarizes this concept: {concept}"
        sys_prompt = "You are a master copywriter. Output ONLY the short quote, without quotation marks."
        return self.provider.generate_content(prompt, system_prompt=sys_prompt)
        
    def generate_music_vibe(self, quote: str) -> str:
        prompt = f"Give me exactly one word or a short phrase (e.g., 'chill lofi', 'intense cinematic', 'upbeat pop') representing the musical vibe of this quote: {quote}"
        sys_prompt = "You are a music supervisor. Output ONLY the short genre/vibe keyword."
        return self.provider.generate_content(prompt, system_prompt=sys_prompt)

    def generate_hashtags(self, concept: str, count: int = 10) -> List[str]:
        schema = {
            "type": "object",
            "properties": {
                "hashtags": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["hashtags"]
        }
        prompt = f"Generate exactly {count} relevant hashtags for this concept: {concept}"
        result = self.provider.generate_json(prompt, schema)
        if isinstance(result, list):
            return result
        return result.get("hashtags", [])
