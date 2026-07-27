import pytest
from unittest.mock import MagicMock
from autosocial.content.pipeline import ContentPipeline
from autosocial.content.providers.base import AIProvider

class MockProvider(AIProvider):
    def generate_content(self, prompt: str, system_prompt: str = "") -> str:
        if "caption" in prompt.lower():
            return "This is a great caption!"
        return "This is a great concept."

    def generate_json(self, prompt: str, schema: dict, system_prompt: str = "") -> dict:
        return {"hashtags": ["#test1", "#test2"]}

def test_content_pipeline():
    provider = MockProvider()
    pipeline = ContentPipeline(provider)
    
    concept = pipeline.generate_concept("Tech", ["old tech"])
    assert concept == "This is a great concept."
    
    caption = pipeline.generate_caption(concept, "professional")
    assert caption == "This is a great caption!"
    
    hashtags = pipeline.generate_hashtags(concept)
    assert len(hashtags) == 2
    assert "#test1" in hashtags
