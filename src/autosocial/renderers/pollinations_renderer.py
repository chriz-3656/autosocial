import os
import uuid
import logging
import urllib.parse
import requests
from typing import Optional

logger = logging.getLogger(__name__)

class PollinationsRenderer:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def render_image(self, concept: str, caption: str) -> Optional[str]:
        """
        Uses Pollinations.ai for 100% free, unlimited, keyless AI Image Generation.
        """
        try:
            # Construct a rich prompt
            prompt_text = (
                f"Create a stunning, highly detailed, Instagram-worthy photorealistic image representing this concept: '{concept}'. "
                f"The image should visually convey the core message of this caption: '{caption[:200]}'."
            )
            
            # URL encode the prompt
            encoded_prompt = urllib.parse.quote(prompt_text)
            
            # Construct URL (1080x1080 for Instagram, nologo=true removes the watermark)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"
            
            logger.info(f"Downloading image from Pollinations: {url}")
            
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                filename = f"{uuid.uuid4()}.jpg"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                    
                return filepath
            else:
                logger.error(f"Pollinations returned status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Pollinations API: {str(e)}")
            return None
