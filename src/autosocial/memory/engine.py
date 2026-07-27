from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

class PostMemory(BaseModel):
    id: str
    topic: str
    caption: str
    hashtags: List[str]
    published_at: datetime
    performance: Optional[Dict[str, Any]] = None

class MemoryEngine:
    """
    Tracks all generated content to prevent duplicates and maintain context.
    Currently a stub implementation; to be backed by SQLAlchemy in next iteration.
    """
    
    def __init__(self):
        self._history: List[PostMemory] = []
        
    def add_post(self, post: PostMemory) -> None:
        self._history.append(post)
        
    def get_recent_topics(self, limit: int = 10) -> List[str]:
        return [p.topic for p in self._history[-limit:]]
        
    def is_duplicate(self, topic: str, similarity_threshold: float = 0.8) -> bool:
        # Stub logic for duplicate detection
        recent = self.get_recent_topics()
        return topic in recent
