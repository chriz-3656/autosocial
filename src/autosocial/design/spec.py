from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, Field

class AspectRatio(str, Enum):
    SQUARE = "1:1"
    PORTRAIT = "4:5"
    STORY = "9:16"

class Alignment(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class DesignSpec(BaseModel):
    aspect_ratio: AspectRatio
    content_type: Literal["quote", "statement", "announcement", "certificate", "banner", "thumbnail"]

    # Palette
    palette_token: str
    gradient_angle_deg: int = Field(ge=0, le=90)

    # Texture / atmosphere
    grain_intensity: float = Field(ge=0.0, le=0.3)
    vignette: bool
    glow: Optional[Literal["none", "soft_center", "top_left", "bottom_right"]] = "none"

    # Structure
    border_style: Literal["none", "thin_rule", "frame_with_corners", "double_rule"] = "none"
    corner_accents: bool = False

    # Typography
    font_pairing_token: str
    headline_max_chars: int = Field(le=120, default=120)
    eyebrow_text: Optional[str] = Field(default=None, max_length=40)
    text_alignment: Alignment = Alignment.CENTER

    # Branding
    brand_handle: str
    branding_placement: Literal["bottom_center", "bottom_left", "top_center", "corner_chip"] = "bottom_center"

    quote_text: str = Field(max_length=400)
