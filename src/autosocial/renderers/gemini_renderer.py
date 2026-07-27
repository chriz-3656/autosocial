import base64
import os
import uuid
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GeminiRenderer:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def render_image(self, concept: str, caption: str) -> Optional[str]:
        """
        Uses the official Google GenAI SDK and gemini-3.1-flash-lite-image 
        to generate a breathtaking image based on the post concept.
        """
        try:
            from google import genai
            from autosocial.core.config import settings
        except ImportError:
            logger.error("google-genai SDK is not installed.")
            return None
            
        api_key = settings.gemini_api_key
        if not api_key:
            logger.error("GEMINI_API_KEY not found in settings.")
            return None
            
        client = genai.Client(api_key=api_key)
        
        # We inject the best image prompt based on the user's concept and caption!
        prompt = (
            f"Create a stunning, highly detailed, Instagram-worthy image representing this concept: '{concept}'. "
            f"The image should visually convey the core message of this caption: '{caption[:200]}'. "
            "Make it photorealistic, vibrant, and perfectly composed for social media."
        )
        
        generation_config = {
            'temperature': 1,
            'max_output_tokens': 65536,
            'top_p': 0.95,
            'thinking_level': 'low',
            'image_config': {
                'image_size': '1K',
            },
        }
        
        try:
            interaction = client.interactions.create(
                model='models/gemini-3.1-flash-lite-image',
                input=prompt,
                generation_config=generation_config,
                response_modalities=['image', 'text'],
            )
            
            # Extract the image data
            for step in interaction.steps:
                if step.type == 'model_output' and step.content:
                    for part in step.content:
                        if part.type == 'image':
                            # We found the image! Let's decode and save it.
                            filename = f"{uuid.uuid4()}.jpg"
                            filepath = os.path.join(self.output_dir, filename)
                            
                            with open(filepath, "wb") as f:
                                f.write(base64.b64decode(part.data))
                                
                            return filepath
                            
            logger.error("Gemini API succeeded but returned no image parts.")
            return None
            
        except Exception as e:
            logger.error(f"Error calling Gemini Image API: {str(e)}")
            return None
