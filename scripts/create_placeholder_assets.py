import argparse
import json
from pathlib import Path
from textwrap import wrap

from moviepy import CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont

SIZE = (1080, 1920)

NAVY = (9, 18, 45)
DEEP_TEAL = (19, 93, 102)
ELECTRIC_BLUE = (59, 130, 246)
AMBER = (255, 185, 80)
WHITE = (245, 248, 255)
MUTED = (110, 140, 170)

FLOW_NODES = ["BRIEF", "AGENT", "HTML", "QA", "ZIP"]


def load_font(size: int):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def gradient(width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), NAVY)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = (y / height) ** 1.4
        color = tuple(int(NAVY[i] * (1 - ratio) + DEEP_TEAL[i] * ratio) for i in range(3))
        draw.line([(0, y), (width, y)], fill=color)
    return img


def draw_grid(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    grid_color = (22, 36, 70)
    for x in range(0, width, 135):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 135):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)


def draw_flow_nodes(draw: ImageDraw.ImageDraw, width: int, y: int) -> None:
    node_font = load_font(26)
    n = len(FLOW_NODES)
    margin = 80
    span = width - 2 * margin
    radius = 12
    for i, label in enumerate(FLOW_NODES):
        cx = margin + int(span * i / (n - 1))
        if i < n - 1:
            nx = margin + int(span * (i + 1) / (n - 1))
            draw.line([(cx + radius, y), (nx - radius, y)], fill=ELECTRIC_BLUE, width=3)
        fill = AMBER if label == "ZIP" else ELECTRIC_BLUE
        draw.ellipse((cx - radius, y - radius, cx + radius, y + radius), fill=fill)
        bbox = draw.textbbox((0, 0), label, font=node_font)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw / 2, y + 22), label, font=node_font, fill=MUTED)


def text_card(text: str, out_png: Path, size=SIZE) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    img = gradient(*size)
    draw = ImageDraw.Draw(img)

    draw_grid(draw, *size)

    # Accent framing
    draw.rectangle((0, 0, size[0], 10), fill=ELECTRIC_BLUE)
    draw.rectangle((60, 210, 68, 300), fill=AMBER)

    kicker_font = load_font(40)
    draw.text((92, 228), "AI EMAIL DEV", font=kicker_font, fill=AMBER)

    headline_font = load_font(92)
    lines = wrap(text, width=16)[:7]
    line_height = 112
    total_h = len(lines) * line_height
    y = (size[1] - total_h) // 2 - 80
    for line in lines:
        draw.text((70, y), line, font=headline_font, fill=WHITE)
        y += line_height

    draw_flow_nodes(draw, size[0], size[1] - 420)

    # Slogan bar
    draw.rectangle((0, size[1] - 240, size[0], size[1]), fill=(13, 62, 70))
    draw.rectangle((0, size[1] - 240, size[0], size[1] - 232), fill=ELECTRIC_BLUE)
    slogan_font = load_font(38)
    draw.text((70, size[1] - 170), "Learn AI. Build proof. Grow your value.", font=slogan_font, fill=WHITE)

    img.save(out_png)


def create_clip(text: str, output_mp4: Path, duration: float) -> None:
    temp_png = Path("output") / "tmp" / f"{output_mp4.stem}.png"
    text_card(text, temp_png)
    base = ImageClip(str(temp_png)).with_duration(duration)
    # Subtle push-in so placeholders don't feel static.
    zooming = base.resized(lambda t: 1.02 + 0.012 * t).with_position("center")
    clip = CompositeVideoClip([zooming], size=SIZE).with_duration(duration)
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    clip.write_videofile(str(output_mp4), fps=30, codec="libx264", audio=False, logger=None)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create local placeholder b-roll clips for testing.")
    parser.add_argument("--job", required=True)
    parser.add_argument("--force", action="store_true", help="Regenerate placeholder clips even if they exist.")
    args = parser.parse_args()

    job_path = Path(args.job)
    job = json.loads(job_path.read_text(encoding="utf-8"))

    for item in job["videoPlan"]:
        clip_path = Path("assets") / item["clip"]
        marker = clip_path.with_suffix(".placeholder")
        if clip_path.exists() and not (args.force and marker.exists()):
            print(f"Skipping existing asset: {clip_path}")
            continue
        create_clip(item["overlayText"], clip_path, item["duration"])
        # Marker lets downstream tooling distinguish placeholders from real footage.
        marker.touch()
        print(f"✅ Placeholder asset created: {clip_path}")

    print("Done. Replace these placeholder clips with real screen recordings when ready.")


if __name__ == "__main__":
    main()
