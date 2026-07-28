import json
from autosocial.design.spec import DesignSpec, AspectRatio
from autosocial.design.palette_library import PALETTES
from autosocial.design.font_pairing_library import FONT_PAIRINGS
from autosocial.design.canvas_utils import get_font, wrap_text, contrast_ratio
from PIL import Image, ImageDraw

class DesignValidator:
    def __init__(self, llm_provider):
        self.llm_provider = llm_provider
    
    def _get_canvas_size(self, aspect_ratio: AspectRatio):
        if aspect_ratio == AspectRatio.SQUARE:
            return (1080, 1080)
        elif aspect_ratio == AspectRatio.PORTRAIT:
            return (1080, 1350)
        elif aspect_ratio == AspectRatio.STORY:
            return (1080, 1920)
        return (1080, 1080)
        
    def _get_safe_zone(self, aspect_ratio: AspectRatio):
        w, h = self._get_canvas_size(aspect_ratio)
        gutter = 144
        if aspect_ratio == AspectRatio.STORY:
            return (w - gutter * 2, h - 600)
        return (w - gutter * 2, h - 400)
        
    async def validate_with_retry(self, raw_json: str, brief: str, system_prompt: str = "", max_retries: int = 2) -> dict:
        current_json = raw_json
        for attempt in range(max_retries + 1):
            try:
                clean_json = current_json.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json[7:]
                elif clean_json.startswith("```"):
                    clean_json = clean_json[3:]
                if clean_json.endswith("```"):
                    clean_json = clean_json[:-3]
                
                data = json.loads(clean_json)
                spec = DesignSpec(**data)
                
                if spec.palette_token not in PALETTES:
                    raise ValueError(f"palette_token '{spec.palette_token}' is not in the allowed list: {list(PALETTES.keys())}")
                if spec.font_pairing_token not in FONT_PAIRINGS:
                    raise ValueError(f"font_pairing_token '{spec.font_pairing_token}' is not in the allowed list: {list(FONT_PAIRINGS.keys())}")
                
                resolved = self._apply_checks(spec)
                return {"spec": spec, "resolved": resolved}
            except Exception as e:
                if attempt == max_retries:
                    print(f"Validation failed after {max_retries} retries: {e}. Falling back to default.")
                    spec = self._fallback_spec(brief)
                    resolved = self._apply_checks(spec)
                    return {"spec": spec, "resolved": resolved}
                
                print(f"Validation error on attempt {attempt+1}: {e}. Retrying...")
                prompt = f"Your previous JSON failed validation with error: {e}\n\nReturn ONLY corrected valid JSON."
                raw_json_dict = self.llm_provider.generate_json(prompt, schema=DesignSpec.model_json_schema(), system_prompt=system_prompt)
                current_json = json.dumps(raw_json_dict)
                
    def _apply_checks(self, spec: DesignSpec):
        max_w, max_h = self._get_safe_zone(spec.aspect_ratio)
        pairing = FONT_PAIRINGS[spec.font_pairing_token]
        img = Image.new('RGBA', (1,1))
        d = ImageDraw.Draw(img)
        
        fs = 80
        while fs > 20:
            font = get_font(pairing["display"], fs)
            lines = wrap_text(spec.quote_text, font, max_w, d)
            total_h = len(lines) * (fs * 1.2)
            if total_h <= max_h:
                break
            fs -= 4
            
        if fs <= 20:
            raise ValueError(f"quote_text is too long to fit in {spec.aspect_ratio} safe zone.")
            
        palette = PALETTES[spec.palette_token]
        # Base contrast check against the lighter of the two gradients (or start)
        cr = contrast_ratio(palette["ink"], palette["gradient_start"])
        resolved_ink = palette["ink"]
        if cr < 3.0:
            cr2 = contrast_ratio(palette["ink_soft"], palette["gradient_start"])
            if cr2 > cr:
                resolved_ink = palette["ink_soft"]
            
        return {
            "font_size": fs,
            "text_color": resolved_ink
        }
        
    def _fallback_spec(self, brief: str) -> DesignSpec:
        return DesignSpec(
            aspect_ratio=AspectRatio.PORTRAIT,
            content_type="quote",
            palette_token="quiet_luxury",
            gradient_angle_deg=45,
            grain_intensity=0.1,
            vignette=False,
            glow="none",
            border_style="none",
            corner_accents=False,
            font_pairing_token="elegant_serif",
            headline_max_chars=120,
            eyebrow_text=None,
            text_alignment="center",
            brand_handle="autosocial",
            branding_placement="bottom_center",
            quote_text="Default safe quote because LLM failed to produce valid JSON."
        )
