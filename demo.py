import asyncio
import logging
from autosocial.content.providers.dummy import DummyProvider
from autosocial.content.pipeline import ContentPipeline
from autosocial.queue.manager import QueueManager
from autosocial.renderers.html_renderer import HTMLRenderer
from autosocial.renderers.template_engine import TemplateEngine
from autosocial.brain.orchestrator import BrainOrchestrator
from autosocial.core.interfaces.publisher import PublisherInterface
from autosocial.models.post import PostConfig, StoryConfig, PublisherResult

logging.basicConfig(level=logging.INFO)

# Dummy Publisher just for the demo
class DummyPublisher(PublisherInterface):
    def login(self, u, p, s=None): return True
    def get_session_data(self): return {}
    def publish_post(self, config: PostConfig) -> PublisherResult:
        print(f"\n[DUMMY PUBLISHER] Publishing Post!")
        print(f"Caption: {config.caption}")
        print(f"Media Path: {config.media[0].path}")
        return PublisherResult(success=True, media_id="dummy_id_123")
    def publish_story(self, config: StoryConfig): return PublisherResult(success=True)
    def publish_reel(self, config: PostConfig): return PublisherResult(success=True)

async def main():
    print("--- Starting AutoSocial Fast Demo ---")
    
    # 1. Initialize Components
    provider = DummyProvider()
    pipeline = ContentPipeline(provider)
    queue = QueueManager()
    renderer = HTMLRenderer(output_dir="/tmp/autosocial_demo")
    template_engine = TemplateEngine("src/autosocial/templates")
    publisher = DummyPublisher()
    
    brain = BrainOrchestrator(pipeline, queue, renderer, publisher)
    
    # 2. Generate and Queue
    item_id = await brain.create_and_queue_post("Tech Tips", [])
    item = queue.get_pending()[0]
    
    # 3. Inject HTML Template instead of generic tag
    print("Applying Jinja2 template...")
    html = template_engine.render("basic.html", {"concept": item.concept, "brand": "autosocial.ai"})
    
    # Render Step (mocked to avoid downloading Chromium for the fast demo)
    print("Simulating HTML to PNG rendering...")
    queue.update_state(item_id, "rendering")
    # Simulate a delay or just skip
    path = "/tmp/autosocial_demo/dummy_image.png"
    # Ensure directory exists and touch file
    import os
    os.makedirs("/tmp/autosocial_demo", exist_ok=True)
    with open(path, "w") as f:
        f.write("dummy image data")
        
    item.media_path = path
    queue.update_state(item_id, "ready")
    print(f"Image successfully rendered to: {path}")
    
    # 4. Publish Step
    print("Publishing...")
    await brain.process_publishing()
    
    print("\n--- Demo Complete! ---")

if __name__ == "__main__":
    asyncio.run(main())
