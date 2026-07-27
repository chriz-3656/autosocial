import os
import uuid
from playwright.async_api import async_playwright
from typing import Optional

class HTMLRenderer:
    def __init__(self, output_dir: str = "/tmp"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def render_image(self, html_content: str, width: int = 1080, height: int = 1080) -> Optional[str]:
        output_path = os.path.join(self.output_dir, f"{uuid.uuid4()}.png")
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.set_viewport_size({"width": width, "height": height})
                await page.set_content(html_content)
                try:
                    await page.wait_for_selector('body[data-ready="true"]', timeout=5000)
                except Exception as e:
                    print(f"Renderer warning: data-ready timeout. Taking screenshot anyway. {e}")
                await page.screenshot(path=output_path)
                await browser.close()
            return output_path
        except Exception as e:
            print(f"Renderer error: {e}")
            return None
