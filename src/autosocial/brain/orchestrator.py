import uuid
import logging
from typing import Optional

from autosocial.content.pipeline import ContentPipeline
from autosocial.queue.manager import QueueManager, QueueItem, QueueState
from autosocial.renderers.html_renderer import HTMLRenderer
from autosocial.core.interfaces.publisher import PublisherInterface
from autosocial.models.post import PostConfig, MediaItem

logger = logging.getLogger(__name__)

class BrainOrchestrator:
    def __init__(
        self,
        pipeline: ContentPipeline,
        queue: QueueManager,
        renderer: HTMLRenderer,
        publisher: PublisherInterface
    ):
        self.pipeline = pipeline
        self.queue = queue
        self.renderer = renderer
        self.publisher = publisher
        
    async def create_and_queue_post(self, category: str, memory_topics: list) -> str:
        """Step 1: Generate Content and Queue it"""
        concept = self.pipeline.generate_concept(category, memory_topics)
        caption = self.pipeline.generate_caption(concept, "witty")
        hashtags = self.pipeline.generate_hashtags(concept)
        
        item_id = str(uuid.uuid4())
        item = QueueItem(
            id=item_id,
            state=QueueState.PENDING,
            concept=concept,
            caption=caption,
            hashtags=hashtags
        )
        self.queue.add_item(item)
        logger.info(f"Queued post {item_id}")
        return item_id
        
    async def process_rendering(self):
        """Step 2: Render pending items"""
        pending = self.queue.get_pending()
        for item in pending:
            self.queue.update_state(item.id, QueueState.RENDERING)
            html = f"<html><body><h1>{item.concept}</h1></body></html>"
            path = await self.renderer.render_image(html)
            if path:
                item.media_path = path
                self.queue.update_state(item.id, QueueState.READY)
            else:
                self.queue.update_state(item.id, QueueState.FAILED, "Rendering failed")
                
    async def process_publishing(self):
        """Step 3: Publish ready items"""
        ready = self.queue.get_ready()
        for item in ready:
            self.queue.update_state(item.id, QueueState.PUBLISHING)
            
            full_caption = f"{item.caption}\n\n{' '.join(item.hashtags)}"
            config = PostConfig(
                caption=full_caption,
                media=[MediaItem(path=item.media_path, media_type="photo")]
            )
            
            result = self.publisher.publish_post(config)
            if result.success:
                self.queue.update_state(item.id, QueueState.PUBLISHED)
            else:
                self.queue.update_state(item.id, QueueState.FAILED, result.error)
