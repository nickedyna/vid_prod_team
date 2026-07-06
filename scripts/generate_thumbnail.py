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


SENIOTO_NAVY = (7, 17, 31)
SENIOTO_BLUE = (37, 99, 235)
SENIOTO_TEAL = (20, 184, 166)
SENIOTO_AMBER = (245, 158, 11)
SENIOTO_WHITE = (248, 250, 252)
SENIOTO_SLATE = (148, 163, 184)


def build_senioto_thumbnail(job: dict, output: Path, size=(1280, 720)) -> None:
    """Reference-style anatomy: 3-line text stack left, blue highlight bar,
    amber arrow accent, ghosted workflow art right, dark navy background."""
    img = Image.new("RGB", size, SENIOTO_NAVY)
    draw = ImageDraw.Draw(img)

    # Subtle grid + ghosted workflow nodes on the right third (stand-in for talking head)
    for x in range(0, size[0], 80):
        draw.line([(x, 0), (x, size[1])], fill=(12, 24, 44), width=1)
    for y in range(0, size[1], 80):
        draw.line([(0, y), (size[0], y)], fill=(12, 24, 44), width=1)

    node_labels = ["BRIEF", "AGENT", "HTML", "QA", "ZIP"]
    node_font = load_font(24)
    nx, ny = size[0] - 300, 150
    for i, label in enumerate(node_labels):
        cy = ny + i * 105
        if i < len(node_labels) - 1:
            draw.line([(nx, cy + 22), (nx, cy + 83)], fill=(30, 70, 140), width=4)
        color = SENIOTO_AMBER if label == "ZIP" else SENIOTO_BLUE
        draw.ellipse((nx - 22, cy - 22, nx + 22, cy + 22), outline=color, width=5)
        draw.ellipse((nx - 8, cy - 8, nx + 8, cy + 8), fill=color)
        draw.text((nx + 42, cy - 14), label, font=node_font, fill=SENIOTO_SLATE)

    headline = job["thumbnail"]["headline"].upper()
    subhead = job["thumbnail"].get("subhead", "").lower()
    cta = job["thumbnail"].get("cta", "")

    words = headline.split()
    split_at = max(1, (len(words) + 1) // 2) if len(words) > 2 else len(words) - 1
    line1 = " ".join(words[:split_at])
    line2 = " ".join(words[split_at:]) or subhead.upper()

    line1_font = load_font(118, bold=True)
    line2_font = load_font(76, bold=True)
    line3_font = load_font(44, bold=False)
    cta_font = load_font(36, bold=True)

    # Line 1: giant white
    draw.text((64, 96), line1, font=line1_font, fill=SENIOTO_WHITE)

    # Line 2: solid electric-blue highlight bar
    bbox = draw.textbbox((0, 0), line2, font=line2_font)
    bar_w, bar_h = bbox[2] - bbox[0] + 56, bbox[3] - bbox[1] + 44
    bar_x, bar_y = 64, 258
    draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=10, fill=SENIOTO_BLUE)
    draw.text((bar_x + 28, bar_y + 10), line2, font=line2_font, fill=SENIOTO_WHITE)

    # Line 3: smaller lowercase
    draw.text((68, bar_y + bar_h + 34), subhead, font=line3_font, fill=SENIOTO_WHITE)

    # Amber curved arrow pointing at the highlight bar
    ax = bar_x + bar_w + 46
    draw.arc((ax, bar_y + bar_h - 24, ax + 130, bar_y + bar_h + 96), start=200, end=330, fill=SENIOTO_AMBER, width=10)
    tip_x, tip_y = ax + 8, bar_y + bar_h - 4
    draw.polygon(
        [(tip_x, tip_y), (tip_x + 40, tip_y + 18), (tip_x + 10, tip_y + 44)],
        fill=SENIOTO_AMBER,
    )

    # CTA chip bottom-left
    if cta:
        cta_bbox = draw.textbbox((0, 0), cta, font=cta_font)
        chip_w = cta_bbox[2] - cta_bbox[0] + 64
        draw.rounded_rectangle((64, size[1] - 118, 64 + chip_w, size[1] - 54), radius=16, fill=SENIOTO_AMBER)
        draw.text((96, size[1] - 106), cta, font=cta_font, fill=SENIOTO_NAVY)

    # Brand mark bottom-right
    brand_font = load_font(34)
    draw.text((size[0] - 240, size[1] - 74), "SENIOTO", font=brand_font, fill=SENIOTO_TEAL)

    # Teal top accent line
    draw.rectangle((0, 0, size[0], 8), fill=SENIOTO_TEAL)

    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output, quality=95)
    print(f"✅ Thumbnail written (senioto style): {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a branded thumbnail from a video job JSON.")
    parser.add_argument("--job", required=True)
    parser.add_argument("--avatar", default="assets/avatar/avatar.png")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    job_path = Path(args.job)
    job = json.loads(job_path.read_text(encoding="utf-8"))
    output = Path(args.output) if args.output else Path("output/thumbnails") / f"{job_path.stem}.jpg"

    if job.get("visualStyle") == "senioto_enterprise_ai":
        build_senioto_thumbnail(job, output)
    else:
        build_thumbnail(job, output, Path(args.avatar))


if __name__ == "__main__":
    main()
