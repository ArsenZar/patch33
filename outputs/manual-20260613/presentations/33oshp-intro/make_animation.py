from pathlib import Path
from math import sin, pi

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance


ROOT = Path("/Users/senya_zar/Documents/Codex/2026-06-13/files-mentioned-by-the-user-patchpng")
WORKSPACE = ROOT / "outputs/manual-20260613/presentations/33oshp-intro"
ASSET_DIR = WORKSPACE / "assets"
OUTPUT_DIR = WORKSPACE / "output"
SOURCE = Path("/Users/senya_zar/Desktop/patchPNG.png")

W, H = 720, 1280
FPS = 12
FRAME_COUNT = 42
CREAM = (246, 242, 167)
GREEN = (127, 216, 141)

ASSET_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clamp01(value):
    return max(0.0, min(1.0, value))


def smoothstep(edge0, edge1, value):
    t = clamp01((value - edge0) / (edge1 - edge0))
    return t * t * (3 - 2 * t)


def radial_glow(size, center, radius, color, opacity):
    small = Image.new("L", (max(1, size[0] // 4), max(1, size[1] // 4)), 0)
    pixels = small.load()
    cx = center[0] / 4
    cy = center[1] / 4
    r = radius / 4
    for y in range(small.height):
        for x in range(small.width):
            distance = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            strength = max(0.0, 1.0 - distance / r)
            pixels[x, y] = round(255 * opacity * strength * strength)
    alpha = small.resize(size, Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(26))
    layer = Image.new("RGBA", size, (*color, 0))
    layer.putalpha(alpha)
    return layer


source = Image.open(SOURCE).convert("RGBA")
panel_source = source.crop((0, 270, 889, 1820))

title_font = ImageFont.truetype(
    "/Users/senya_zar/Library/Fonts/ST-SimpleSquare.ttf", 84
)
subtitle_font = ImageFont.truetype(
    "/Users/senya_zar/Library/Fonts/KyivTypeSans-Medium-.ttf", 29
)

base = Image.new("RGBA", (W, H), (1, 4, 3, 255))
base.alpha_composite(radial_glow((W, H), (360, -15), 430, GREEN, 0.15))
base.alpha_composite(radial_glow((W, H), (360, 1320), 520, CREAM, 0.40))

frames = []
for index in range(FRAME_COUNT):
    t = index / (FRAME_COUNT - 1)
    hero_in = smoothstep(0.03, 0.48, t)
    title_in = smoothstep(0.28, 0.64, t)
    subtitle_in = smoothstep(0.46, 0.80, t)
    settle = 1 - (1 - hero_in) ** 3
    scale = 0.925 + settle * 0.075
    panel_w = round(575 * scale)
    panel_h = round(panel_source.height / panel_source.width * panel_w)
    left = round((W - panel_w) / 2)
    top = round(250 + (1 - settle) * 35)

    frame = base.copy()

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    pulse = 0.92 + sin(t * pi) * 0.08
    shadow_draw.rounded_rectangle(
        (left + 34, top + 25, left + panel_w - 34, top + panel_h - 10),
        radius=8,
        fill=(*GREEN, round(255 * 0.055 * hero_in * pulse)),
    )
    shadow_draw.rounded_rectangle(
        (left + 15, top + 30, left + panel_w - 15, top + panel_h),
        radius=8,
        fill=(*CREAM, round(255 * 0.045 * hero_in)),
    )
    frame.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(24)))

    panel = panel_source.resize((panel_w, panel_h), Image.Resampling.LANCZOS)
    panel = ImageEnhance.Brightness(panel).enhance(0.68 + 0.32 * hero_in)
    panel.putalpha(round(255 * hero_in))
    frame.alpha_composite(panel, (left, top))

    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)
    y_shift = round((1 - title_in) * 12)

    title = "33ОШП"
    title_box = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_box[2] - title_box[0]
    draw.text(
        ((W - title_w) / 2, 75 + y_shift),
        title,
        font=title_font,
        fill=(*CREAM, round(255 * title_in)),
    )
    draw.rounded_rectangle(
        (285, 174 + y_shift, 435, 176 + y_shift),
        radius=1,
        fill=(*CREAM, round(255 * title_in * 0.65)),
    )

    subtitle = "(Механізований бат)"
    subtitle_box = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_w = subtitle_box[2] - subtitle_box[0]
    draw.text(
        ((W - subtitle_w) / 2, 184 + y_shift),
        subtitle,
        font=subtitle_font,
        fill=(*CREAM, round(255 * subtitle_in)),
    )
    frame.alpha_composite(text_layer)
    frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=192))

gif_path = ASSET_DIR / "33oshp-soft-reveal.gif"
frames[0].save(
    gif_path,
    save_all=True,
    append_images=frames[1:],
    duration=round(1000 / FPS),
    loop=0,
    optimize=True,
    disposal=2,
)

preview_path = OUTPUT_DIR / "33oshp-preview.png"
frames[-1].convert("RGBA").save(preview_path)

print(
    {
        "gif": str(gif_path),
        "preview": str(preview_path),
        "frames": FRAME_COUNT,
        "fps": FPS,
    }
)
