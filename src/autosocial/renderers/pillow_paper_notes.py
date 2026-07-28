import os
import uuid
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Optional

class PillowPaperNotesRenderer:
    def __init__(self, output_dir: str = "/tmp"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.size = (1080, 1080)
        
        self.papers = [
            (226, 200, 192), # blush
            (201, 191, 175), # taupe
            (222, 208, 178), # sand
            (217, 190, 175)  # dust
        ]
        self.ink = (24, 20, 15)
        self.ink_soft = (74, 68, 60)
        self.mark_yellow = (242, 222, 73)
        self.mark_red = (198, 71, 46)
        
        def get_font_path(name):
            if not os.path.exists("fonts"): return None
            for root, dirs, files in os.walk("fonts"):
                for f in files:
                    if name.lower() in f.lower() and f.endswith(".ttf"):
                        return os.path.join(root, f)
            return None

        # Fallbacks: since we don't have Lora/Baloo, we use Fraunces as serif and Inter as sans.
        self.font_sans_reg = get_font_path("inter-regular") or get_font_path("inter")
        self.font_sans_bd = get_font_path("inter-medium") or self.font_sans_reg
        self.font_serif = get_font_path("fraunces") or get_font_path("inter")

    def hash_string(self, s: str) -> int:
        h = 5381
        for char in s:
            h = ((h << 5) + h) + ord(char)
            h = h & 0xFFFFFFFF
        return abs(h)
        
    def find_split(self, text: str):
        delims = [' — ', ' – ', ' - ', ': ', '; ']
        for delim in delims:
            idx = text.find(delim)
            if idx > 0 and idx < len(text) - len(delim):
                return text[:idx], text[idx + len(delim):]
        return None

    def wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_w: int, draw: ImageDraw.Draw):
        words = text.split()
        lines = []
        curr = []
        for word in words:
            curr.append(word)
            bbox = draw.textbbox((0,0), " ".join(curr), font=font)
            if (bbox[2] - bbox[0]) > max_w:
                curr.pop()
                if curr:
                    lines.append(" ".join(curr))
                curr = [word]
        if curr:
            lines.append(" ".join(curr))
        return lines

    def render_image(self, concept: str, brand: str) -> Optional[str]:
        concept = concept.strip()
        brand = brand.strip().replace('@', '')
        
        seed = self.hash_string(f"{concept}::{brand}")
        random.seed(seed)
        
        bg_color = self.papers[seed % len(self.papers)]
        img = Image.new('RGBA', self.size, bg_color)
        d = ImageDraw.Draw(img)
        
        w, h = self.size
        gutter = 64
        
        split = self.find_split(concept)
        if split:
            layout = 'statement'
        elif len(concept) <= 30:
            layout = 'symbol'
        elif len(concept) <= 75:
            layout = 'highlight'
        else:
            layout = 'diagonal'
            
        # Draw diagonal overlay if needed
        if layout == 'diagonal':
            # Create a separate layer for the multiply blend
            diag = Image.new('RGBA', self.size, (0,0,0,0))
            d_diag = ImageDraw.Draw(diag)
            
            # Draw diagonal stripes
            stripe_w = 26
            gap = 76
            for i in range(-2000, 2000, stripe_w + gap):
                d_diag.polygon([
                    (i, 0), (i + stripe_w, 0), 
                    (i + stripe_w - 2000, 2000), (i - 2000, 2000)
                ], fill=(0, 0, 0, 18))
            
            img = Image.alpha_composite(img, diag)
            d = ImageDraw.Draw(img) # Re-bind draw to the composited image

        # Helpers for fonts
        def get_font(path, size):
            try: return ImageFont.truetype(path, size)
            except: return ImageFont.load_default()

        if layout == 'symbol':
            f_serif = get_font(self.font_serif, 34)
            f_brand = get_font(self.font_sans_reg, 14)
            
            symbols = ["✦", "♥", "★", "∞", "●"]
            sym = symbols[seed % len(symbols)]
            
            f_sym = get_font(self.font_sans_reg, 72)
            
            # draw symbol
            sw = d.textlength(sym, font=f_sym)
            d.text(((w - sw)/2, 280), sym, font=f_sym, fill=self.ink)
            
            # draw caption
            lines = self.wrap_text(concept, f_serif, 620, d)
            y = 420
            for line in lines:
                lw = d.textlength(line, font=f_serif)
                d.text(((w - lw)/2, y), line, font=f_serif, fill=self.ink)
                y += 44
                
            # draw brand
            bw = d.textlength(f"@{brand}", font=f_brand)
            d.text(((w - bw)/2, h - gutter - 20), f"@{brand}", font=f_brand, fill=self.ink_soft)

        elif layout == 'highlight':
            f_disp = get_font(self.font_sans_bd, 56)
            f_brand = get_font(self.font_serif, 17)
            
            # top left brand
            d.text((gutter, 40), f"@{brand}", font=f_brand, fill=self.ink)
            
            words = concept.split()
            n = len(words)
            hc = max(1, round(n/3))
            uc = max(1, round(n/3))
            if hc + uc > n:
                hc = math.ceil(n/2)
                uc = n - hc
                
            # We must draw word by word to do inline backgrounds and underlines
            x, y = gutter, 320
            max_w = 760
            
            d.text((x, y), "“", font=get_font(self.font_serif, 56), fill=self.ink)
            x += d.textlength("“", font=get_font(self.font_serif, 56))
            
            for i, word in enumerate(words):
                ww = d.textlength(word + " ", font=f_disp)
                if x + ww > gutter + max_w:
                    x = gutter
                    y += 66
                
                # Highlight background
                if i < hc:
                    bbox = d.textbbox((x, y), word, font=f_disp)
                    d.rectangle([bbox[0]-4, bbox[1], bbox[2]+4, bbox[3]], fill=self.mark_yellow)
                
                # Text
                d.text((x, y), word, font=f_disp, fill=self.ink)
                
                # Underline
                if i >= n - uc:
                    bbox = d.textbbox((x, y), word, font=f_disp)
                    uy = bbox[3] + 4
                    d.line([(bbox[0], uy), (bbox[2], uy)], fill=self.mark_red, width=2)
                    d.line([(bbox[0], uy+4), (bbox[2], uy+4)], fill=self.mark_red, width=2)
                
                x += ww
                
            d.text((x, y), "”", font=get_font(self.font_serif, 56), fill=self.ink)

        elif layout == 'statement':
            head, sub = split
            f_head = get_font(self.font_sans_bd, 46)
            f_sub = get_font(self.font_serif, 26)
            f_brand = get_font(self.font_sans_bd, 15)
            
            lines_h = self.wrap_text(head, f_head, 760, d)
            y = 300
            
            # draw quote mark
            d.text((gutter-20, y), "“", font=get_font(self.font_serif, 46), fill=self.ink)
            
            for line in lines_h:
                d.text((gutter, y), line, font=f_head, fill=self.ink)
                y += 54
                
            # end quote mark
            lw = d.textlength(lines_h[-1], font=f_head)
            d.text((gutter + lw + 4, y - 54), "”", font=get_font(self.font_serif, 46), fill=self.ink)
            
            y += 20
            lines_s = self.wrap_text(sub, f_sub, 560, d)
            for line in lines_s:
                d.text((gutter, y), line, font=f_sub, fill=self.ink_soft)
                y += 34
                
            # Bottom brand
            brand_txt = f"@{brand}".upper()
            d.text((gutter, h - 48 - 15), brand_txt, font=f_brand, fill=self.ink)
            
            # Avatar chip
            initial = brand[0].upper() if brand else "•"
            cx = w - gutter - 20
            cy = h - 40 - 20
            d.ellipse([cx-20, cy-20, cx+20, cy+20], fill=self.ink)
            f_init = get_font(self.font_sans_bd, 16)
            iw = d.textlength(initial, font=f_init)
            d.text((cx - iw/2, cy - 10), initial, font=f_init, fill=self.papers[2])

        elif layout == 'diagonal':
            f_eye = get_font(self.font_serif, 20)
            f_body = get_font(self.font_serif, 30)
            f_brand = get_font(self.font_sans_bd, 15)
            
            tags = ['A Field Note', 'On Reflection', 'A Reminder', 'Worth Repeating', 'Some Perspective']
            eye = tags[seed % len(tags)]
            
            y = 260
            d.text((gutter, y), f"“{eye}”", font=f_eye, fill=self.ink_soft)
            y += 40
            
            lines = self.wrap_text(concept, f_body, 660, d)
            for line in lines:
                d.text((gutter, y), line, font=f_body, fill=self.ink)
                y += 42
                
            brand_txt = f"@{brand}"
            bw = d.textlength(brand_txt, font=f_brand)
            d.text(((w - bw)/2, h - gutter - 15), brand_txt, font=f_brand, fill=self.ink)

        # Grain effect
        noise = Image.effect_noise(self.size, 12).convert('RGBA')
        noise.putalpha(15)
        img = Image.alpha_composite(img, noise)

        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(self.output_dir, filename)
        img = img.convert('RGB')
        img.save(filepath, quality=95)
        return filepath
