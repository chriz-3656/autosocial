from autosocial.queue.manager import QueueManager, QueueItem, QueueState

def test_queue_lifecycle():
    manager = QueueManager()
    item = QueueItem(
        id="123",
        state=QueueState.PENDING,
        concept="concept",
        caption="caption",
        hashtags=["#tag"]
    )
    
    manager.add_item(item)
    assert len(manager.get_pending()) == 1
    
    manager.update_state("123", QueueState.READY)
    assert len(manager.get_pending()) == 0
    assert len(manager.get_ready()) == 1
