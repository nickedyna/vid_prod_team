import argparse
import json
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont

BRAND_BG_TOP = (9, 18, 45)
BRAND_BG_BOTTOM = (19, 93, 102)
ACCENT = (255, 185, 80)
WHITE = (245, 248, 255)
MUTED = (180, 203, 220)


def load_font(size: int, bold: bool = True):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def gradient_background(width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), BRAND_BG_TOP)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / height
        color = tuple(int(BRAND_BG_TOP[i] * (1 - ratio) + BRAND_BG_BOTTOM[i] * ratio) for i in range(3))
        draw.line([(0, y), (width, y)], fill=color)
    return img


def paste_avatar(canvas: Image.Image, avatar_path: Path) -> None:
    if not avatar_path.exists():
        return
    avatar = Image.open(avatar_path).convert("RGBA")
    target_h = int(canvas.height * 0.78)
    ratio = target_h / avatar.height
    avatar = avatar.resize((int(avatar.width * ratio), target_h))
    x = canvas.width - avatar.width - 45
    y = canvas.height - avatar.height
    canvas.alpha_composite(avatar, (x, y))


def draw_wrapped(draw: ImageDraw.ImageDraw, xy, text: str, font, fill, max_chars: int, line_gap: int = 10):
    x, y = xy
    for line in wrap(text, width=max_chars):
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def build_thumbnail(job: dict, output: Path, avatar_path: Path, size=(1280, 720)) -> None:
    canvas = gradient_background(*size).convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    # Brand shapes
    draw.rounded_rectangle((35, 35, size[0] - 35, size[1] - 35), radius=36, outline=(255, 255, 255, 90), width=4)
    draw.rectangle((0, size[1] - 110, size[0], size[1]), fill=(0, 0, 0, 115))

    paste_avatar(canvas, avatar_path)
    draw = ImageDraw.Draw(canvas)

    headline = job["thumbnail"]["headline"].upper()
    subhead = job["thumbnail"].get("subhead", "").upper()
    cta = job["thumbnail"].get("cta", "")

    headline_font = load_font(76, bold=True)
    subhead_font = load_font(34, bold=True)
    cta_font = load_font(34, bold=True)

    y = 85
    y = draw_wrapped(draw, (70, y), headline, headline_font, WHITE, max_chars=18, line_gap=8)
    y += 15
    if subhead:
        draw.text((74, y), subhead, font=subhead_font, fill=ACCENT)
    if cta:
        draw.rounded_rectangle((70, size[1] - 88, 380, size[1] - 38), radius=18, fill=ACCENT)
        draw.text((95, size[1] - 80), cta, font=cta_font, fill=(12, 19, 35))

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, quality=95)
    print(f"✅ Thumbnail written: {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a branded thumbnail from a video job JSON.")
    parser.add_argument("--job", required=True)
    parser.add_argument("--avatar", default="assets/avatar/avatar.png")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    job_path = Path(args.job)
    job = json.loads(job_path.read_text(encoding="utf-8"))
    output = Path(args.output) if args.output else Path("output/thumbnails") / f"{job_path.stem}.jpg"

    build_thumbnail(job, output, Path(args.avatar))


if __name__ == "__main__":
    main()
