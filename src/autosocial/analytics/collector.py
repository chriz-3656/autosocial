from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class AnalyticsCollector:
    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}

    def record_post_performance(self, post_id: str, likes: int, comments: int, reach: int = 0):
        self.metrics[post_id] = {
            "likes": likes,
            "comments": comments,
            "reach": reach
        }
        logger.info(f"Recorded metrics for post {post_id}: {self.metrics[post_id]}")

    def get_performance(self, post_id: str) -> Dict[str, Any]:
        return self.metrics.get(post_id, {})
        
    def get_all_performance(self) -> Dict[str, Dict[str, Any]]:
        return self.metrics
