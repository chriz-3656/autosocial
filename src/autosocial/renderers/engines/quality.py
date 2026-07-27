from typing import Dict, Any

class QualityEngine:
    def __init__(self):
        pass
        
    def score_design(self, plan: Dict[str, Any]) -> int:
        """
        Simulates an algorithmic scoring of the design plan.
        Scores typography pairings, contrast, and layout complexity.
        Returns a score from 0 to 100.
        """
        score = 100
        
        # Penalize if fonts are the same
        if plan.get("headline_font") == plan.get("body_font"):
            score -= 20
            
        # Penalize if there's no highlight for engagement
        if not plan.get("highlight"):
            score -= 10
            
        # If score is too low, we might trigger a regeneration
        return max(0, score)
