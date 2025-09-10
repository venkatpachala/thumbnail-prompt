from __future__ import annotations

from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps


CANVAS_SIZE = (1280, 720)


def fit_canvas(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """Resize image to fit exact canvas size."""
    return ImageOps.fit(img, size, method=Image.Resampling.LANCZOS)


def choose_contrast_color(rgb: Tuple[int, int, int]) -> Tuple[str, str]:
    """Return (fill, stroke) colors based on background brightness."""
    brightness = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
    if brightness < 128:
        return ("#ffffff", "#000000")
    return ("#000000", "#ffffff")


def place_subject(bg: Image.Image, subject: Image.Image, side: str = "right") -> Image.Image:
    bg = bg.convert("RGBA")
    subject = subject.convert("RGBA")
    h = int(bg.height * 0.6)
    ratio = h / subject.height
    w = int(subject.width * ratio)
    subject = subject.resize((w, h), Image.Resampling.LANCZOS)

    # drop shadow
    shadow = Image.new("RGBA", subject.size, color=(0, 0, 0, 0))
    alpha = subject.split()[-1]
    shadow.putalpha(alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    shadow_pos = (int(bg.width * (0.66 if side == "left" else 0.34)) - w // 2 + 10,
                  bg.height // 2 - h // 2 + 10)
    bg.paste(shadow, shadow_pos, shadow)

    pos = (int(bg.width * (0.66 if side == "right" else 0.34)) - w // 2,
           bg.height // 2 - h // 2)
    bg.paste(subject, pos, subject)
    return bg


def add_headline(img: Image.Image, text: str, side: str = "right") -> Image.Image:
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=80)
    except Exception:
        font = ImageFont.load_default()

    text_w, text_h = draw.textsize(text, font=font)
    padding = 40
    x = padding if side == "right" else img.width - text_w - padding
    y = img.height - text_h - padding

    # sample background region
    region = img.crop((x, y, x + text_w, y + text_h)).resize((1, 1))
    fill, stroke = choose_contrast_color(region.getpixel((0, 0)))

    draw.text((x+3, y+3), text, font=font, fill=stroke)
    draw.text((x, y), text, font=font, fill=fill, stroke_width=3, stroke_fill=stroke)
    return img
