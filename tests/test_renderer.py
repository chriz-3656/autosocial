import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
from autosocial.renderers.template_engine import TemplateEngine
from autosocial.renderers.html_renderer import HTMLRenderer

def test_template_engine(tmp_path):
    # Create a dummy template
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "test.html"
    template_file.write_text("<h1>Hello {{ name }}</h1>")
    
    engine = TemplateEngine(str(template_dir))
    rendered = engine.render("test.html", {"name": "World"})
    assert rendered == "<h1>Hello World</h1>"

@pytest.mark.asyncio
async def test_html_renderer_mocked():
    with patch("autosocial.renderers.html_renderer.async_playwright") as mock_playwright:
        mock_p = MagicMock()
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        
        mock_playwright.return_value.__aenter__.return_value = mock_p
        mock_p.chromium.launch = AsyncMock(return_value=mock_browser)
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        
        renderer = HTMLRenderer(output_dir="/tmp/autosocial_render")
        result = await renderer.render_image("<html></html>")
        
        assert result is not None
        assert result.startswith("/tmp/autosocial_render/")
        assert result.endswith(".png")
        
        mock_page.set_content.assert_called_once_with("<html></html>")
        mock_page.screenshot.assert_called_once()
