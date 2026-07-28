from typing import List, Optional
from pydantic import BaseModel, Field

class MediaItem(BaseModel):
    path: str = Field(description="Local path to the media file")
    media_type: str = Field(description="Type of media: 'photo' or 'video'")

class StoryLink(BaseModel):
    url: str

class PostConfig(BaseModel):
    caption: str = Field(default="", description="Caption for the post")
    media: List[MediaItem] = Field(description="List of media items for the post")
    location_name: Optional[str] = Field(default=None, description="Optional location to tag")
    music_query: Optional[str] = Field(default=None, description="Music genre or keyword to search for")
    
class StoryConfig(BaseModel):
    media: MediaItem
    link: Optional[StoryLink] = None
    mentions: List[str] = Field(default_factory=list)

class PublisherResult(BaseModel):
    success: bool
    media_id: Optional[str] = None
    error: Optional[str] = None
