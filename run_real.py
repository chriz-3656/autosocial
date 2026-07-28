import asyncio
import logging
from autosocial.core.config import settings
from autosocial.content.providers.openai_provider import OpenAIProvider
from autosocial.content.providers.groq_provider import GroqProvider
from autosocial.content.providers.gemini_provider import GeminiProvider
from autosocial.content.providers.fallback_provider import FallbackProvider
from autosocial.content.pipeline import ContentPipeline
from autosocial.queue.manager import QueueManager
from autosocial.renderers.html_renderer import HTMLRenderer
from autosocial.renderers.template_engine import TemplateEngine
from autosocial.brain.orchestrator import BrainOrchestrator
from autosocial.publishers.instagrapi_publisher import InstagrapiPublisher

logging.basicConfig(level=logging.ERROR)

async def main():
    print("--- Starting AutoSocial Real Run with AI Fallbacks ---")
    
    if not settings.instagram_username or not settings.instagram_password:
        print("ERROR: Missing required credentials in .env file.")
        print("Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD.")
        return

    # Initialize Available AI Providers
    available_providers = []
    if settings.openai_api_key:
        available_providers.append(OpenAIProvider(api_key=settings.openai_api_key))
    if settings.gemini_api_key:
        available_providers.append(GeminiProvider(api_key=settings.gemini_api_key))
    if settings.groq_api_key:
        available_providers.append(GroqProvider(api_key=settings.groq_api_key))

    if not available_providers:
        print("ERROR: No AI Providers configured. Please set at least one API key (OPENAI_API_KEY, GEMINI_API_KEY, GROQ_API_KEY).")
        return

    # 1. Initialize Real Components
    print(f"Initializing FallbackProvider with {len(available_providers)} AI Engines...")
    provider = FallbackProvider(providers=available_providers)
    pipeline = ContentPipeline(provider)
    queue = QueueManager()
    renderer = HTMLRenderer(output_dir="/tmp/autosocial_real")
    template_engine = TemplateEngine("src/autosocial/templates")
    publisher = InstagrapiPublisher()
    
    # Try logging into Instagram
    print(f"Logging into Instagram as {settings.instagram_username}...")
    try:
        publisher.login(settings.instagram_username, settings.instagram_password)
    except Exception as e:
        print(f"Instagram Login Failed: {e}")
        return

    brain = BrainOrchestrator(pipeline, queue, renderer, publisher)
    
    # 2. Generate and Queue
    print("Contacting OpenAI to generate post concept...")
    item_id = await brain.create_and_queue_post("Productivity", [])
    item = queue.get_pending()[0]
    
    # Clean formatting colors
    C_MAG='\033[35m'
    C_CYAN='\033[36m'
    C_YEL='\033[33m'
    C_DIM='\033[2m'
    C_RST='\033[0m'

    print(f"\n{C_MAG}╭────────────────────────────────────────────────────────╮{C_RST}")
    print(f"{C_MAG}│{C_RST} {C_YEL}✨ AI GENERATED CONCEPT{C_RST}                                {C_MAG}│{C_RST}")
    print(f"{C_MAG}├────────────────────────────────────────────────────────┤{C_RST}")
    # Indent concept text nicely
    for line in item.concept.split('\n'):
        print(f"{C_MAG}│{C_RST} {C_DIM}{line}{C_RST}")
    print(f"{C_MAG}╰────────────────────────────────────────────────────────╯{C_RST}")
    
    print(f"\n{C_MAG}╭────────────────────────────────────────────────────────╮{C_RST}")
    print(f"{C_MAG}│{C_RST} {C_YEL}✍️ SHORT QUOTE (For Image Rendering){C_RST}                   {C_MAG}│{C_RST}")
    print(f"{C_MAG}├────────────────────────────────────────────────────────┤{C_RST}")
    print(f"{C_MAG}│{C_RST} {C_DIM}{item.quote}{C_RST}")
    print(f"{C_MAG}╰────────────────────────────────────────────────────────╯{C_RST}")

    print(f"\n{C_CYAN}╭────────────────────────────────────────────────────────╮{C_RST}")
    print(f"{C_CYAN}│{C_RST} {C_YEL}📝 INSTAGRAM CAPTION{C_RST}                                   {C_CYAN}│{C_RST}")
    print(f"{C_CYAN}├────────────────────────────────────────────────────────┤{C_RST}")
    for line in item.caption.split('\n'):
        print(f"{C_CYAN}│{C_RST} {line}")
    print(f"{C_CYAN}├────────────────────────────────────────────────────────┤{C_RST}")
    if item.hashtags:
        print(f"{C_CYAN}│{C_RST} {C_MAG}{' '.join(item.hashtags)}{C_RST}")
    print(f"{C_CYAN}╰────────────────────────────────────────────────────────╯{C_RST}\n")
    
    # 3. Render High-End AI Image using the Pure-Python Pillow Editorial Engine
    print("Generating Image using Pillow Editorial Engine...")
    print(f"Vibe Music Query: {item.music_vibe}")
    queue.update_state(item_id, "rendering")
    
    from autosocial.renderers.pillow_editorial import PillowEditorialRenderer
    
    renderer = PillowEditorialRenderer(output_dir="/tmp/autosocial_real")
    path = renderer.render_image(concept=item.quote, brand=settings.default_brand)
    
    if not path:
        print("Rendering failed.")
        return
    
    item.media_path = path
    queue.update_state(item_id, "ready")
    print(f"Image rendered to: {path}")
    
    # 4. Publish
    print("Publishing to Instagram...")
    await brain.process_publishing()
    
    published_items = queue.get_ready()
    # It should be empty if successful
    if not published_items:
        print("\n--- Successfully Published! ---")
    else:
        print("\n--- Publishing Failed. Check logs. ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        C_MAG = '\033[35m'
        C_RED = '\033[31m'
        C_RST = '\033[0m'
        print("\n\n" + f"{C_MAG}╭{'─'*56}╮{C_RST}")
        print(f"{C_MAG}│{C_RST} {C_RED}🛑 AutoSocial AI Shutdown Safely{C_RST}{' '*22}{C_MAG}│{C_RST}")
        print(f"{C_MAG}╰{'─'*56}╯{C_RST}\n")
        import sys
        sys.exit(0)
