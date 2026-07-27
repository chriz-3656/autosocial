from autosocial.analytics.collector import AnalyticsCollector
from fastapi.testclient import TestClient
from autosocial.dashboard.api import app

def test_analytics_collector():
    collector = AnalyticsCollector()
    collector.record_post_performance("post1", likes=100, comments=10, reach=500)
    
    perf = collector.get_performance("post1")
    assert perf["likes"] == 100
    assert perf["comments"] == 10
    
def test_dashboard_api():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "AutoSocial AI"}
    
    response = client.get("/queue/pending")
    assert response.status_code == 200
    assert "pending" in response.json()
