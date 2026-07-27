import pytest
from unittest.mock import MagicMock, AsyncMock
from autosocial.brain.orchestrator import BrainOrchestrator
from autosocial.queue.manager import QueueManager, QueueState

@pytest.mark.asyncio
async def test_brain_orchestrator():
    pipeline = MagicMock()
    pipeline.generate_concept.return_value = "Test Concept"
    pipeline.generate_caption.return_value = "Test Caption"
    pipeline.generate_hashtags.return_value = ["#test"]
    
    queue = QueueManager()
    
    renderer = AsyncMock()
    renderer.render_image.return_value = "/tmp/image.png"
    
    publisher = MagicMock()
    result = MagicMock()
    result.success = True
    publisher.publish_post.return_value = result
    
    brain = BrainOrchestrator(pipeline, queue, renderer, publisher)
    
    # 1. Create and queue
    item_id = await brain.create_and_queue_post("Tech", [])
    assert len(queue.get_pending()) == 1
    
    # 2. Process rendering
    await brain.process_rendering()
    assert len(queue.get_pending()) == 0
    assert len(queue.get_ready()) == 1
    
    # 3. Process publishing
    await brain.process_publishing()
    assert len(queue.get_ready()) == 0
    
    # Check published state
    item = queue._queue[0]
    assert item.state == QueueState.PUBLISHED
