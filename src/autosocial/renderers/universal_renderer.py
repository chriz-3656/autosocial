import os
from typing import Dict, Any
from autosocial.content.providers.base import AIProvider
from autosocial.renderers.design_planner import DesignPlanner
from autosocial.renderers.template_builder import TemplateBuilder
from autosocial.renderers.engines.quality import QualityEngine
from autosocial.renderers.html_renderer import HTMLRenderer
import logging

logger = logging.getLogger(__name__)

class UniversalRenderer:
    def __init__(self, provider: AIProvider, templates_dir: str, output_dir: str):
        self.planner = DesignPlanner(provider)
        self.builder = TemplateBuilder(templates_dir)
        self.quality = QualityEngine()
        self.renderer = HTMLRenderer(output_dir)
        
    async def render_post(self, concept: str, brand_handle: str) -> str:
        """
        Orchestrates the entire editorial design process:
        Concept -> Design Plan -> Score -> HTML -> Image
        """
        logger.info("Generating Editorial Design Plan...")
        plan = self.planner.generate_plan(concept, brand_handle)
        
        # Quality Engine Check
        score = self.quality.score_design(plan)
        logger.info(f"Design Quality Score: {score}/100")
        
        if score < 80:
            logger.info("Score below threshold. Regenerating Design Plan...")
            plan = self.planner.generate_plan(concept, brand_handle)
            
        logger.info(f"Selected Layout: {plan['template']}, Palette: {plan['palette']}")
        
        html_content = self.builder.build_html(concept, plan)
        
        # Render the final image using Playwright
        logger.info("Rendering High DPI PNG via Playwright...")
        image_path = await self.renderer.render_image(html_content)
        return image_path
