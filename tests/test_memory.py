import pytest
from datetime import datetime
from autosocial.memory.engine import MemoryEngine, PostMemory

def test_memory_engine_add_and_retrieve():
    engine = MemoryEngine()
    
    post = PostMemory(
        id="123",
        topic="AI in Healthcare",
        caption="Exploring AI.",
        hashtags=["#ai", "#health"],
        published_at=datetime.utcnow()
    )
    
    engine.add_post(post)
    
    recent = engine.get_recent_topics()
    assert len(recent) == 1
    assert recent[0] == "AI in Healthcare"
    
def test_memory_engine_duplicate_detection():
    engine = MemoryEngine()
    
    post = PostMemory(
        id="123",
        topic="Tech Trends",
        caption="Tech.",
        hashtags=["#tech"],
        published_at=datetime.utcnow()
    )
    
    engine.add_post(post)
    
    assert engine.is_duplicate("Tech Trends") is True
    assert engine.is_duplicate("Future of Work") is False
