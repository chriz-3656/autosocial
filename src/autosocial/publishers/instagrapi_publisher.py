import logging
from typing import Dict, Any, Optional

from instagrapi import Client
from instagrapi.exceptions import (
    ChallengeRequired,
    FeedbackRequired,
    LoginRequired,
    PleaseWaitFewMinutes,
    BadPassword
)

from autosocial.core.interfaces.publisher import PublisherInterface
from autosocial.models.post import PostConfig, StoryConfig, PublisherResult

logger = logging.getLogger(__name__)

class InstagrapiPublisher(PublisherInterface):
    """
    Implementation of the PublisherInterface that wraps the instagrapi Client.
    """
    
    def __init__(self, proxy: Optional[str] = None):
        self.client = Client()
        if proxy:
            self.client.set_proxy(proxy)
            
    def login(self, username: str, password: str, session_data: dict = None) -> bool:
        """
        Login with session reuse if session_data is provided.
        """
        try:
            if session_data:
                logger.info(f"Attempting to login {username} using provided session data.")
                self.client.set_settings(session_data)
                
            self.client.login(username, password)
            logger.info(f"Successfully logged in as {username}")
            return True
        except (ChallengeRequired, FeedbackRequired, LoginRequired, PleaseWaitFewMinutes, BadPassword) as e:
            logger.error(f"Login failed for {username}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during login for {username}: {str(e)}")
            return False

    def get_session_data(self) -> dict:
        """
        Get current session settings (cookies, device id, etc.) to persist.
        """
        return self.client.get_settings()

    def publish_post(self, config: PostConfig) -> PublisherResult:
        """
        Publish photo, video, or carousel based on the number and type of media items.
        """
        try:
            if not config.media:
                return PublisherResult(success=False, error="No media provided for post")

            media = None
            if len(config.media) == 1:
                item = config.media[0]
                if item.media_type == "photo":
                    try:
                        music_query = config.music_query if config.music_query else "lofi"
                        tracks = self.client.search_music(music_query)
                        if tracks:
                            track = tracks[0]
                            logger.info(f"Auto-adding vibe matched song ({music_query}): {track.title} by {track.display_artist}")
                            media = self.client.photo_upload_with_music(item.path, config.caption, track=track)
                        else:
                            media = self.client.photo_upload(item.path, config.caption)
                    except Exception as e:
                        logger.warning(f"Failed to add music: {e}. Falling back to normal upload.")
                        media = self.client.photo_upload(item.path, config.caption)
                elif item.media_type == "video":
                    media = self.client.video_upload(item.path, config.caption)
                else:
                    return PublisherResult(success=False, error=f"Unknown media type: {item.media_type}")
            else:
                # Carousel
                paths = [item.path for item in config.media]
                media = self.client.album_upload(paths, config.caption)
                
            return PublisherResult(success=True, media_id=str(media.pk))
        except Exception as e:
            logger.error(f"Failed to publish post: {str(e)}")
            return PublisherResult(success=False, error=str(e))

    def publish_story(self, config: StoryConfig) -> PublisherResult:
        """
        Publish a photo or video story.
        """
        try:
            links = []
            if config.link:
                from instagrapi.types import StoryLink as InstaStoryLink
                links.append(InstaStoryLink(webUri=config.link.url))
                
            media = None
            if config.media.media_type == "photo":
                media = self.client.photo_upload_to_story(config.media.path, links=links)
            elif config.media.media_type == "video":
                media = self.client.video_upload_to_story(config.media.path, links=links)
            else:
                return PublisherResult(success=False, error=f"Unknown media type: {config.media.media_type}")
                
            return PublisherResult(success=True, media_id=str(media.pk))
        except Exception as e:
            logger.error(f"Failed to publish story: {str(e)}")
            return PublisherResult(success=False, error=str(e))

    def publish_reel(self, config: PostConfig) -> PublisherResult:
        """
        Publish a video as a Reel.
        """
        try:
            if not config.media or len(config.media) != 1 or config.media[0].media_type != "video":
                return PublisherResult(success=False, error="Reels require exactly one video media item")
                
            media = self.client.clip_upload(config.media[0].path, config.caption)
            return PublisherResult(success=True, media_id=str(media.pk))
        except Exception as e:
            logger.error(f"Failed to publish reel: {str(e)}")
            return PublisherResult(success=False, error=str(e))
