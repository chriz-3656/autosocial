import os
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
from autosocial.renderers.engines.theme import PALETTES, BACKGROUNDS, ICONS

class TemplateBuilder:
    def __init__(self, templates_dir: str):
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
    def build_html(self, concept: str, plan: Dict[str, Any]) -> str:
        """Merges the design plan into the universal HTML template."""
        template = self.env.get_template("universal.html")
        
        # Resolve the raw CSS/SVG from the engines
        bg_style = BACKGROUNDS.get(plan["background"], "")
        palette = PALETTES.get(plan["palette"], PALETTES["cream_black"])
        icon_svg = ICONS.get(plan["icon"], "")
        
        # Bold/Highlight the important words in the concept
        highlighted_concept = concept
        for word in plan.get("highlight", []):
            # Simple text replace to wrap in a span with accent color
            highlighted_concept = highlighted_concept.replace(
                word, 
                f'<span style="color: {palette["accent"]}; font-weight: bold; border-bottom: 4px solid {palette["accent"]}">{word}</span>'
            )
            
        return template.render(
            concept=highlighted_concept,
            raw_concept=concept,
            layout_class=plan["template"],
            bg_style=bg_style,
            palette=palette,
            headline_font=plan["headline_font"],
            body_font=plan["body_font"],
            icon_svg=icon_svg,
            footer=plan["footer"]
        )
