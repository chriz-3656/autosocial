from typing import Dict, List, Any
import random

# Typography Engine
FONTS = [
    "Inter", "Manrope", "Space Grotesk", "Outfit", "Sora", 
    "Plus Jakarta Sans", "DM Sans", "Poppins", "Playfair Display", 
    "Libre Baskerville", "Lora", "Cormorant Garamond", "Syne", "Cabinet Grotesk"
]

def get_font_pairing() -> Dict[str, str]:
    pairings = [
        {"headline": "Space Grotesk", "body": "Inter"},
        {"headline": "Playfair Display", "body": "Lora"},
        {"headline": "Syne", "body": "Inter"},
        {"headline": "Outfit", "body": "Plus Jakarta Sans"},
        {"headline": "Cormorant Garamond", "body": "Montserrat"},
        {"headline": "DM Sans", "body": "DM Sans"},
        {"headline": "Sora", "body": "Manrope"},
    ]
    return random.choice(pairings)

# Color Engine
PALETTES = {
    "cream_black": {"bg": "#F9F6F0", "text": "#1A1A1A", "accent": "#D4AF37"},
    "midnight_gold": {"bg": "#0A0A0A", "text": "#F5F5F5", "accent": "#C5A059"},
    "sage_minimal": {"bg": "#E9EDE8", "text": "#2C352D", "accent": "#8A9A86"},
    "blush_wine": {"bg": "#FDF7F5", "text": "#3A1F24", "accent": "#8C3A43"},
    "slate_blue": {"bg": "#1E293B", "text": "#F8FAFC", "accent": "#38BDF8"},
    "warm_terracotta": {"bg": "#FAF5F0", "text": "#2C1810", "accent": "#E07A5F"},
    "monochrome_grey": {"bg": "#E5E5E5", "text": "#111111", "accent": "#444444"}
}

# Background Engine
BACKGROUNDS = {
    "solid": "",
    "warm_paper": "background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);",
    "mesh_gradient": "background-image: radial-gradient(at 40% 20%, hsla(28,100%,74%,1) 0px, transparent 50%), radial-gradient(at 80% 0%, hsla(189,100%,56%,1) 0px, transparent 50%);",
    "paper_grain": "background-image: url('data:image/svg+xml,%3Csvg viewBox=%220 0 200 200%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noiseFilter%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.65%22 numOctaves=%223%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23noiseFilter)%22 opacity=%220.05%22/%3E%3C/svg%3E');",
    "soft_beige": "background-color: #F5F5DC;"
}

# Layout Engine
LAYOUTS = [
    "editorial_minimal",
    "magazine_bold",
    "newspaper_classic",
    "luxury_centered",
    "corporate_split",
    "quote_oversized",
    "grid_asymmetrical",
    "card_floating"
]

# Icons Engine
ICONS = {
    "infinity": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12c-2-2.67-4-4-6-4a4 4 0 1 0 0 8c2 0 4-1.33 6-4Zm0 0c2 2.67 4 4 6 4a4 4 0 1 0 0-8c-2 0-4 1.33-6 4Z"/></svg>',
    "diamond": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12l4 6-10 13L2 9Z"/></svg>',
    "leaf": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 22l10-10"/></svg>',
    "target": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "lightbulb": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.9 1.2 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>'
}
