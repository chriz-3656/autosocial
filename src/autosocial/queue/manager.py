from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class QueueState(str, Enum):
    PENDING = "pending"
    RENDERING = "rendering"
    READY = "ready"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    RETRY = "retry"

class QueueItem(BaseModel):
    id: str
    state: QueueState
    concept: str
    quote: str
    caption: str
    hashtags: List[str]
    music_vibe: str
    media_path: Optional[str] = None
    error: Optional[str] = None

class QueueManager:
    """
    Manages the state of posts moving through the generation and publishing pipeline.
    Stub implementation backed by in-memory list.
    """
    def __init__(self):
        self._queue: List[QueueItem] = []
        
    def add_item(self, item: QueueItem) -> None:
        self._queue.append(item)
        
    def update_state(self, item_id: str, new_state: QueueState, error: str = None) -> None:
        for item in self._queue:
            if item.id == item_id:
                item.state = new_state
                if error:
                    item.error = error
                break
                
    def get_pending(self) -> List[QueueItem]:
        return [item for item in self._queue if item.state == QueueState.PENDING]
        
    def get_ready(self) -> List[QueueItem]:
        return [item for item in self._queue if item.state == QueueState.READY]
