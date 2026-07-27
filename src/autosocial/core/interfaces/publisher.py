from abc import ABC, abstractmethod
from typing import Dict, Any
from autosocial.models.post import PostConfig, StoryConfig, PublisherResult

class PublisherInterface(ABC):
    """
    Abstract interface for publishing content to social media platforms.
    """
    
    @abstractmethod
    def login(self, username: str, password: str, session_data: dict = None) -> bool:
        """Login and return True if successful."""
        pass
        
    @abstractmethod
    def get_session_data(self) -> dict:
        """Return session data to be stored securely."""
        pass

    @abstractmethod
    def publish_post(self, config: PostConfig) -> PublisherResult:
        """Publish a photo, video, or carousel post to the feed."""
        pass

    @abstractmethod
    def publish_story(self, config: StoryConfig) -> PublisherResult:
        """Publish a photo or video story."""
        pass

    @abstractmethod
    def publish_reel(self, config: PostConfig) -> PublisherResult:
        """Publish a video as a reel."""
        pass
