import asyncio
import logging
from autosocial.core.config import settings
from autosocial.content.providers.openai_provider import OpenAIProvider
from autosocial.content.providers.groq_provider import GroqProvider
from autosocial.content.providers.gemini_provider import GeminiProvider

logging.basicConfig(level=logging.ERROR)

async def check():
    providers = []
    
    if settings.openai_api_key:
        providers.append(("OpenAI", OpenAIProvider(api_key=settings.openai_api_key)))
    if settings.gemini_api_key:
        providers.append(("Gemini", GeminiProvider(api_key=settings.gemini_api_key)))
    if settings.groq_api_key:
        providers.append(("Groq", GroqProvider(api_key=settings.groq_api_key)))
        
    print(f"Testing {len(providers)} providers based on .env keys...\n")
    
    for name, provider in providers:
        print(f"--- Checking {name} ---")
        try:
            response = provider.generate_content("Say the word 'Active' and nothing else.")
            print(f"[SUCCESS] {name} is responding! Output: '{response}'")
        except Exception as e:
            print(f"[FAILED] {name} returned an error: {e}")
        print()

if __name__ == "__main__":
    try:
        asyncio.run(check())
    except KeyboardInterrupt:
        import sys
        sys.exit(130)
