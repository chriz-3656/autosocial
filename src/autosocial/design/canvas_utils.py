import os
import math
from PIL import Image, ImageDraw, ImageFont

def get_font_path(name: str):
    if not os.path.exists("fonts"):
        return None
    for root, dirs, files in os.walk("fonts"):
        for f in files:
            if name.lower() in f.lower() and f.endswith(".ttf"):
                return os.path.join(root, f)
    return None

def get_font(name: str, size: int):
    path = get_font_path(name)
    if path:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def wrap_text(text: str, font, max_w: int, draw: ImageDraw.Draw):
    words = text.split()
    lines = []
    curr = []
    for word in words:
        curr.append(word)
        bbox = draw.textbbox((0, 0), " ".join(curr), font=font)
        w = bbox[2] - bbox[0]
        if w > max_w:
            curr.pop()
            if curr:
                lines.append(" ".join(curr))
            curr = [word]
    if curr:
        lines.append(" ".join(curr))
    return lines

def luminance(color):
    r, g, b = [x / 255.0 for x in color[:3]]
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(c1, c2):
    l1 = luminance(c1)
    l2 = luminance(c2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

def make_gradient(size, start_color, end_color, angle_deg):
    w, h = size
    base = Image.new('RGB', (1, 256))
    d = ImageDraw.Draw(base)
    for i in range(256):
        pos = i / 255.0
        r = int(start_color[0] + (end_color[0] - start_color[0]) * pos)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * pos)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * pos)
        d.point((0, i), fill=(r, g, b))
    
    diagonal = int(math.sqrt(w*w + h*h))
    grad = base.resize((diagonal, diagonal))
    grad = grad.rotate(-angle_deg, resample=Image.BICUBIC, expand=True)
    
    gw, gh = grad.size
    left = (gw - w) // 2
    top = (gh - h) // 2
    return grad.crop((left, top, left + w, top + h)).convert('RGBA')
