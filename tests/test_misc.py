import os
from autosocial.cleanup.service import CleanupService
from autosocial.research.engine import ResearchEngine
from autosocial.trends.detection import TrendDetection

def test_cleanup_service(tmp_path):
    # create a dummy file
    test_file = tmp_path / "test.png"
    test_file.write_text("dummy")
    
    service = CleanupService(tmp_dir=str(tmp_path))
    service.clean()
    
    assert not test_file.exists()
    
def test_research_engine():
    engine = ResearchEngine()
    topics = engine.gather_topics()
    assert len(topics) > 0
    assert "Tech trends" in topics
    
def test_trend_detection():
    detection = TrendDetection()
    topics = ["Zebra", "Apple", "Mango"]
    ranked = detection.rank_trends(topics)
    assert ranked == ["Apple", "Mango", "Zebra"]
