from typing import Dict, Any, List
from autosocial.content.providers.base import AIProvider
from autosocial.renderers.engines.theme import PALETTES, BACKGROUNDS, LAYOUTS, ICONS, FONTS
import random

class DesignPlanner:
    def __init__(self, provider: AIProvider):
        self.provider = provider
        
    def generate_plan(self, concept: str, brand_handle: str) -> Dict[str, Any]:
        """Uses the AI Provider to decide on the best design parameters for the concept."""
        schema = {
            "type": "object",
            "properties": {
                "template": {"type": "string", "description": "The best layout"},
                "background": {"type": "string", "description": "The best background texture"},
                "palette": {"type": "string", "description": "The color palette"},
                "headline_font": {"type": "string"},
                "body_font": {"type": "string"},
                "icon": {"type": "string"},
                "highlight": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "1 to 3 words from the concept to highlight or bold"
                }
            },
            "required": ["template", "background", "palette", "headline_font", "body_font", "icon", "highlight"]
        }
        
        prompt = f"""
        Act as a professional editorial art director.
        Concept to design for: "{concept}"
        
        Choose from these exact options:
        Templates: {', '.join(LAYOUTS)}
        Backgrounds: {', '.join(BACKGROUNDS.keys())}
        Palettes: {', '.join(PALETTES.keys())}
        Fonts: {', '.join(FONTS)}
        Icons: {', '.join(ICONS.keys())}
        """
        
        try:
            plan = self.provider.generate_json(prompt, schema, system_prompt="You are an editorial design expert.")
            # Fallbacks in case the AI hallucinates a key
            if plan.get("template") not in LAYOUTS: plan["template"] = random.choice(LAYOUTS)
            if plan.get("background") not in BACKGROUNDS: plan["background"] = "solid"
            if plan.get("palette") not in PALETTES: plan["palette"] = "cream_black"
            if plan.get("icon") not in ICONS: plan["icon"] = "diamond"
            plan["footer"] = brand_handle
            return plan
        except Exception as e:
            # Fallback to random if AI fails
            return {
                "template": random.choice(LAYOUTS),
                "background": "paper_grain",
                "palette": "midnight_gold",
                "headline_font": "Space Grotesk",
                "body_font": "Inter",
                "icon": "diamond",
                "highlight": [],
                "footer": brand_handle
            }
