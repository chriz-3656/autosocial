import os
import math
import uuid
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Optional

class PillowEditorialRenderer:
    def __init__(self, output_dir: str = "/tmp"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.size = (1080, 1080)
        self.colors = {
            'ink_950': (12, 15, 19),
            'ink_900': (20, 24, 30),
            'ink_800': (29, 34, 42),
            'parchment': (234, 227, 210),
            'parchment_dim': (156, 151, 140),
            'brass': (198, 161, 91),
            'brass_dim': (110, 92, 59),
            'teal': (76, 107, 96),
        }
        
        # We assume fonts are downloaded to ./fonts/
        def get_font_path(name):
            if not os.path.exists("fonts"):
                return None
            for root, dirs, files in os.walk("fonts"):
                for f in files:
                    if name.lower() in f.lower() and f.endswith(".ttf"):
                        return os.path.join(root, f)
            return None

        self.font_inter_reg = get_font_path("inter-regular") or get_font_path("inter")
        self.font_inter_med = get_font_path("inter-medium") or self.font_inter_reg
        self.font_plex = get_font_path("ibmplexmono-regular") or get_font_path("plex")
        self.font_fraunces = get_font_path("fraunces-regular") or get_font_path("fraunces")
        
    def hash_string(self, s: str) -> int:
        h = 5381
        for char in s:
            h = ((h << 5) + h) + ord(char)
            h = h & 0xFFFFFFFF
        return abs(h)
        
    def render_image(self, concept: str, brand: str) -> Optional[str]:
        concept = concept.strip()
        brand = brand.strip()
        
        seed = self.hash_string(f"{concept}::{brand}")
        random.seed(seed)
        
        img = Image.new('RGBA', self.size, self.colors['ink_950'])
        
        # BG Mesh Gradients
        bg_layer = Image.new('RGBA', self.size, (0, 0, 0, 0))
        d_bg = ImageDraw.Draw(bg_layer)
        # brass gradient: 198,161,91 at 0.16 -> opacity 40
        d_bg.ellipse([1080*0.08 - 650, 1080*0.06 - 650, 1080*0.08 + 650, 1080*0.06 + 650], fill=(198, 161, 91, 15))
        # teal gradient: 76,107,96 at 0.20 -> opacity 50
        d_bg.ellipse([1080*0.96 - 600, 1080*1.0 - 600, 1080*0.96 + 600, 1080*1.0 + 600], fill=(76, 107, 96, 20))
        
        bg_layer = bg_layer.filter(ImageFilter.GaussianBlur(120))
        img = Image.alpha_composite(img, bg_layer)
        
        # Grid lines
        grid_layer = Image.new('RGBA', self.size, (0, 0, 0, 0))
        d_grid = ImageDraw.Draw(grid_layer)
        for i in range(0, 1080, 54):
            d_grid.line([(0, i), (1080, i)], fill=(234, 227, 210, 8), width=1)
            d_grid.line([(i, 0), (i, 1080)], fill=(234, 227, 210, 8), width=1)
            
        img = Image.alpha_composite(img, grid_layer)
        
        d = ImageDraw.Draw(img)
        
        # Corner marks
        mark_len = 18
        inset = 28
        w, h = self.size
        mark_col = (*self.colors['parchment_dim'], 102) # ~0.4 opacity
        
        d.line([(inset, inset), (inset + mark_len, inset)], fill=mark_col, width=1)
        d.line([(inset, inset), (inset, inset + mark_len)], fill=mark_col, width=1)
        
        d.line([(w - inset - mark_len, inset), (w - inset, inset)], fill=mark_col, width=1)
        d.line([(w - inset, inset), (w - inset, inset + mark_len)], fill=mark_col, width=1)
        
        d.line([(inset, h - inset), (inset + mark_len, h - inset)], fill=mark_col, width=1)
        d.line([(inset, h - inset - mark_len), (inset, h - inset)], fill=mark_col, width=1)
        
        d.line([(w - inset - mark_len, h - inset), (w - inset, h - inset)], fill=mark_col, width=1)
        d.line([(w - inset, h - inset - mark_len), (w - inset, h - inset)], fill=mark_col, width=1)
        
        gutter = 72
        
        # Masthead
        try:
            f_inter_bd = ImageFont.truetype(self.font_inter_med, 15)
            f_mono = ImageFont.truetype(self.font_plex, 12)
        except Exception:
            f_inter_bd = ImageFont.load_default()
            f_mono = ImageFont.load_default()
            
        masthead_y = gutter
        # Brand
        d.text((gutter, masthead_y), "@", font=f_inter_bd, fill=self.colors['brass'])
        at_w = d.textlength("@", font=f_inter_bd)
        brand_clean = brand.replace('@', '')
        d.text((gutter + at_w + 2, masthead_y), brand_clean.upper(), font=f_inter_bd, fill=self.colors['parchment'])
        
        # Date
        months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
        now = datetime.now()
        date_str = f"{now.day:02d} {months[now.month-1]} {now.year}"
        date_w = d.textlength(date_str, font=f_mono)
        d.text((w - gutter - date_w, masthead_y + 2), date_str, font=f_mono, fill=self.colors['parchment_dim'])
        
        # Masthead line
        d.line([(gutter, masthead_y + 26), (w - gutter, masthead_y + 26)], fill=(234,227,210, 46), width=1)
        
        # Footer
        footer_y = h - gutter - 20
        folio_num = 100 + (seed % 900)
        d.text((gutter, footer_y), f"N° {folio_num}", font=f_mono, fill=self.colors['brass'])
        
        # Footer label
        try:
            f_inter_sm = ImageFont.truetype(self.font_inter_med, 11)
        except Exception:
            f_inter_sm = ImageFont.load_default()
            
        label = "EDITORIAL DISPATCH"
        label_w = d.textlength(label, font=f_inter_sm)
        d.text((w - gutter - label_w, footer_y + 2), label, font=f_inter_sm, fill=self.colors['parchment_dim'])
        
        d.line([(gutter, footer_y - 20), (w - gutter, footer_y - 20)], fill=(234,227,210, 46), width=1)
        
        # Eyebrow
        eyebrow_words = ['FIELD NOTE', 'DISPATCH', 'ON RECORD', 'PERSPECTIVE', 'BRIEFING', 'NOTE TO SELF']
        eyebrow_text = eyebrow_words[seed % len(eyebrow_words)]
        
        # Layouts
        if len(concept) <= 26:
            layout = 'cover'
            max_w = 900
            max_fs = 132
            align = 'center'
        elif len(concept) <= 90:
            layout = 'feature'
            max_w = 700
            max_fs = 82
            align = 'left'
        else:
            layout = 'dispatch'
            max_w = 780
            max_fs = 46
            align = 'left'
            
        # Draw Eyebrow
        eb_fs = 13
        try:
            f_inter_eb = ImageFont.truetype(self.font_inter_med, eb_fs)
        except:
            f_inter_eb = ImageFont.load_default()
            
        eb_w = d.textlength(eyebrow_text, font=f_inter_eb) + 15
        
        if layout == 'cover':
            eb_x = (w - eb_w) / 2
        else:
            eb_x = gutter
            
        d.polygon([(eb_x + 3.5, 230), (eb_x + 7, 233.5), (eb_x + 3.5, 237), (eb_x, 233.5)], fill=self.colors['brass'])
        d.text((eb_x + 15, 227), eyebrow_text, font=f_inter_eb, fill=self.colors['brass'])
        
        # Text wrapping and autofit
        def wrap_text(text, font, max_w):
            words = text.split()
            lines = []
            curr = []
            for word in words:
                curr.append(word)
                if d.textlength(" ".join(curr), font=font) > max_w:
                    curr.pop()
                    if curr:
                        lines.append(" ".join(curr))
                    curr = [word]
            if curr:
                lines.append(" ".join(curr))
            return lines

        fs = max_fs
        f_disp = None
        wrapped = []
        while fs > 22:
            try:
                f_disp = ImageFont.truetype(self.font_fraunces, fs)
            except:
                f_disp = ImageFont.load_default()
                break
                
            wrapped = wrap_text(concept, f_disp, max_w)
            total_h = len(wrapped) * (fs * 1.1)
            if total_h <= (footer_y - 20) - 280:
                break
            fs -= 2
            
        y_text = 280
        if layout == 'cover':
            y_text = 280 + ((footer_y - 20 - 280) - (len(wrapped) * fs * 1.1)) / 2
            for line in wrapped:
                lw = d.textlength(line, font=f_disp)
                d.text(((w - lw)/2, y_text), line, font=f_disp, fill=self.colors['parchment'])
                y_text += fs * 1.1
            
            d.line([(w/2 - 32, y_text + 20), (w/2 + 32, y_text + 20)], fill=self.colors['brass'], width=2)
            
            seal_x = w/2
            seal_y = footer_y - 20 - gutter
            seal_r = 59
            
        elif layout == 'feature':
            for line in wrapped:
                d.text((gutter, y_text), line, font=f_disp, fill=self.colors['parchment'])
                y_text += fs * 1.1
            d.line([(gutter, y_text + 20), (gutter + 64, y_text + 20)], fill=self.colors['brass'], width=2)
            
            seal_x = w - gutter - 59
            seal_y = footer_y - 20 - gutter
            seal_r = 59
            
        else:
            for line in wrapped:
                d.text((gutter, y_text), line, font=f_disp, fill=self.colors['parchment'])
                y_text += fs * 1.2
            d.line([(gutter, y_text + 20), (gutter + 64, y_text + 20)], fill=self.colors['brass'], width=2)
            
            seal_x = w - gutter - 42
            seal_y = masthead_y + 26 + 42
            seal_r = 42

        initial = brand_clean.upper()[0] if brand_clean else "•"
        rot = (seed % 24) - 12
        
        d.ellipse([seal_x - seal_r + 2, seal_y - seal_r + 2, seal_x + seal_r - 2, seal_y + seal_r - 2], outline=self.colors['brass_dim'], width=1)
        r_inner = seal_r * 0.82
        d.ellipse([seal_x - r_inner, seal_y - r_inner, seal_x + r_inner, seal_y + r_inner], outline=self.colors['brass'], width=2)
        r_disc = seal_r * 0.72
        d.ellipse([seal_x - r_disc, seal_y - r_disc, seal_x + r_disc, seal_y + r_disc], fill=self.colors['ink_900'], outline=self.colors['brass'], width=2)
        
        try:
            f_seal = ImageFont.truetype(self.font_fraunces, int(seal_r * 0.57))
        except:
            f_seal = ImageFont.load_default()
            
        bbox = d.textbbox((0,0), initial, font=f_seal)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        d.text((seal_x - tw/2, seal_y - th/2 - 4), initial, font=f_seal, fill=self.colors['parchment'])
        
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(self.output_dir, filename)
        img = img.convert('RGB')
        img.save(filepath, quality=95)
        return filepath
