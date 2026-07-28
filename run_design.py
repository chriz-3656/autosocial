import asyncio
import json
import click
from autosocial.core.config import settings
from autosocial.content.providers.openai_provider import OpenAIProvider
from autosocial.content.providers.groq_provider import GroqProvider
from autosocial.content.providers.gemini_provider import GeminiProvider
from autosocial.content.providers.fallback_provider import FallbackProvider
from autosocial.design.validator import DesignValidator
from autosocial.renderers.design_renderer import DesignRenderer
from autosocial.design.palette_library import PALETTES
from autosocial.design.font_pairing_library import FONT_PAIRINGS
from autosocial.design.spec import DesignSpec

async def main(brief: str):
    print("--- Starting AutoSocial Design Generator ---")
    
    available_providers = []
    if settings.openai_api_key:
        available_providers.append(OpenAIProvider(api_key=settings.openai_api_key))
    if settings.gemini_api_key:
        available_providers.append(GeminiProvider(api_key=settings.gemini_api_key))
    if settings.groq_api_key:
        available_providers.append(GroqProvider(api_key=settings.groq_api_key))

    if not available_providers:
        print("ERROR: No AI Providers configured.")
        return

    provider = FallbackProvider(providers=available_providers)
    
    with open("src/autosocial/design/prompts/art_director.md", "r") as f:
        system_prompt = f.read()
        
    allowed_palettes = json.dumps(list(PALETTES.keys()))
    allowed_font_pairings = json.dumps(list(FONT_PAIRINGS.keys()))
    
    system_prompt = system_prompt.replace("{allowed_palettes}", allowed_palettes)
    system_prompt = system_prompt.replace("{allowed_font_pairings}", allowed_font_pairings)
    
    prompt = f"USER BRIEF: {brief}\n\nReturn ONLY valid JSON."
    
    print("Contacting AI Art Director...")
    raw_json_dict = provider.generate_json(prompt, schema=DesignSpec.model_json_schema(), system_prompt=system_prompt)
    raw_json = json.dumps(raw_json_dict)
    
    print("Validating Design Spec...")
    validator = DesignValidator(llm_provider=provider)
    validation_result = await validator.validate_with_retry(raw_json, brief, system_prompt=system_prompt)
    
    spec = validation_result["spec"]
    resolved = validation_result["resolved"]
    
    print(f"Validated Spec:\n{spec.model_dump_json(indent=2)}")
    
    print("Rendering Image...")
    renderer = DesignRenderer(output_dir="/tmp/autosocial_design")
    path = renderer.render(spec, resolved)
    print(f"Image rendered successfully to: {path}")

@click.command()
@click.option("--brief", required=True, help="Creative brief for the design")
def cli(brief):
    asyncio.run(main(brief))

if __name__ == "__main__":
    cli()
