import os
import uuid
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from autosocial.design.spec import DesignSpec, AspectRatio
from autosocial.design.palette_library import PALETTES
from autosocial.design.font_pairing_library import FONT_PAIRINGS
from autosocial.design.canvas_utils import get_font, wrap_text, make_gradient

class DesignRenderer:
    def __init__(self, output_dir: str = "/tmp/autosocial_real"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def _get_canvas_size(self, aspect_ratio: AspectRatio):
        if aspect_ratio == AspectRatio.SQUARE:
            return (1080, 1080)
        elif aspect_ratio == AspectRatio.PORTRAIT:
            return (1080, 1350)
        elif aspect_ratio == AspectRatio.STORY:
            return (1080, 1920)
        return (1080, 1080)

    def render(self, spec: DesignSpec, resolved: dict) -> str:
        size = self._get_canvas_size(spec.aspect_ratio)
        w, h = size
        palette = PALETTES[spec.palette_token]
        pairing = FONT_PAIRINGS[spec.font_pairing_token]
        
        # 1. Base Gradient
        img = make_gradient(size, palette["gradient_start"], palette["gradient_end"], spec.gradient_angle_deg)
        
        # 2. Glow/Vignette
        if spec.vignette:
            vignette_layer = Image.new('RGBA', size, (0, 0, 0, 0))
            dv = ImageDraw.Draw(vignette_layer)
            dv.ellipse([-w*0.5, -h*0.5, w*1.5, h*1.5], outline=(0, 0, 0, 80), width=int(min(w,h)*0.2))
            vignette_layer = vignette_layer.filter(ImageFilter.GaussianBlur(150))
            img = Image.alpha_composite(img, vignette_layer)
            
        if spec.glow and spec.glow != "none":
            glow_layer = Image.new('RGBA', size, (0, 0, 0, 0))
            dg = ImageDraw.Draw(glow_layer)
            glow_col = (*palette["accent"], 60)
            
            if spec.glow == "soft_center":
                dg.ellipse([w*0.1, h*0.1, w*0.9, h*0.9], fill=glow_col)
            elif spec.glow == "top_left":
                dg.ellipse([-w*0.5, -h*0.5, w*0.8, h*0.8], fill=glow_col)
            elif spec.glow == "bottom_right":
                dg.ellipse([w*0.2, h*0.2, w*1.5, h*1.5], fill=glow_col)
                
            glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(200))
            img = Image.alpha_composite(img, glow_layer)
            
        # 3. Border and Corner Accents
        d = ImageDraw.Draw(img)
        inset = 50
        if spec.border_style == "thin_rule":
            d.rectangle([inset, inset, w - inset, h - inset], outline=palette["ink_soft"], width=1)
        elif spec.border_style == "double_rule":
            d.rectangle([inset, inset, w - inset, h - inset], outline=palette["ink_soft"], width=2)
            d.rectangle([inset + 10, inset + 10, w - inset - 10, h - inset - 10], outline=palette["ink_soft"], width=1)
        elif spec.border_style == "frame_with_corners":
            d.rectangle([inset, inset, w - inset, h - inset], outline=palette["ink_soft"], width=1)
            
        if spec.corner_accents:
            cl = 30
            c_col = palette["accent"]
            d.line([(inset, inset), (inset + cl, inset)], fill=c_col, width=3)
            d.line([(inset, inset), (inset, inset + cl)], fill=c_col, width=3)
            
            d.line([(w - inset, inset), (w - inset - cl, inset)], fill=c_col, width=3)
            d.line([(w - inset, inset), (w - inset, inset + cl)], fill=c_col, width=3)
            
            d.line([(inset, h - inset), (inset + cl, h - inset)], fill=c_col, width=3)
            d.line([(inset, h - inset), (inset, h - inset - cl)], fill=c_col, width=3)
            
            d.line([(w - inset, h - inset), (w - inset - cl, h - inset)], fill=c_col, width=3)
            d.line([(w - inset, h - inset), (w - inset, h - inset - cl)], fill=c_col, width=3)
            
        # 4. Procedural Grain
        if spec.grain_intensity > 0.0:
            noise = Image.effect_noise(size, 12).convert('RGBA')
            noise.putalpha(int(255 * spec.grain_intensity))
            img = Image.alpha_composite(img, noise)
            
        # 5. Typography
        d = ImageDraw.Draw(img)
        fs = resolved["font_size"]
        text_col = resolved["text_color"]
        
        font_display = get_font(pairing["display"], fs)
        font_body = get_font(pairing["body"], 24)
        font_eyebrow = get_font(pairing["body"], 18)
        
        gutter = 144
        max_w = w - gutter * 2
        
        lines = wrap_text(spec.quote_text, font_display, max_w, d)
        total_quote_h = len(lines) * (fs * 1.2)
        
        start_y = (h - total_quote_h) / 2
        
        if spec.eyebrow_text:
            eb_w = d.textlength(spec.eyebrow_text, font=font_eyebrow)
            eb_x = gutter if spec.text_alignment == "left" else (w - eb_w) / 2
            d.text((eb_x, start_y - 60), spec.eyebrow_text.upper(), font=font_eyebrow, fill=palette["accent"])
            
        y = start_y
        for line in lines:
            lw = d.textlength(line, font=font_display)
            if spec.text_alignment == "left":
                x = gutter
            elif spec.text_alignment == "right":
                x = w - gutter - lw
            else:
                x = (w - lw) / 2
            d.text((x, y), line, font=font_display, fill=text_col)
            y += fs * 1.2
            
        # Branding
        b_txt = f"@{spec.brand_handle}"
        bw = d.textlength(b_txt, font=font_body)
        
        if spec.branding_placement == "bottom_center":
            bx = (w - bw) / 2
            by = h - 100
        elif spec.branding_placement == "bottom_left":
            bx = gutter
            by = h - 100
        elif spec.branding_placement == "top_center":
            bx = (w - bw) / 2
            by = 80
        elif spec.branding_placement == "corner_chip":
            bx = w - gutter - bw
            by = h - 100
        else:
            bx = (w - bw) / 2
            by = h - 100
            
        d.text((bx, by), b_txt, font=font_body, fill=palette["ink_soft"])
        
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(self.output_dir, filename)
        img = img.convert('RGB')
        img.save(filepath, quality=95)
        return filepath
