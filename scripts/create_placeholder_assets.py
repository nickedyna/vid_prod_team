import argparse
import json
from pathlib import Path

from moviepy import ImageClip
from PIL import Image, ImageDraw, ImageFont

SIZE = (1080, 1920)


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


def text_card(text: str, out_png: Path, size=SIZE) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", size, (10, 18, 40, 255))
    draw = ImageDraw.Draw(img)
    font = load_font(72)
    small = load_font(34)

    draw.rectangle((0, 0, size[0], size[1]), fill=(10, 18, 40, 255))
    draw.rectangle((0, size[1] - 260, size[0], size[1]), fill=(16, 104, 115, 255))
    draw.text((70, 130), "AI EMAIL DEV", font=small, fill=(255, 190, 90, 255))

    words = text.split()
    lines = []
    current = []
    for word in words:
        current.append(word)
        if len(" ".join(current)) > 16:
            lines.append(" ".join(current[:-1]))
            current = [word]
    if current:
        lines.append(" ".join(current))

    y = 420
    for line in lines[:6]:
        draw.text((70, y), line, font=font, fill=(245, 248, 255, 255))
        y += 92

    draw.text((70, size[1] - 180), "Learn AI. Build proof. Grow your value.", font=small, fill=(255, 255, 255, 255))
    img.save(out_png)


def create_clip(text: str, output_mp4: Path, duration: float) -> None:
    temp_png = Path("output") / "tmp" / f"{output_mp4.stem}.png"
    text_card(text, temp_png)
    clip = ImageClip(str(temp_png)).with_duration(duration).resized(SIZE)
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    clip.write_videofile(str(output_mp4), fps=30, codec="libx264", audio=False, logger=None)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create local placeholder b-roll clips for testing.")
    parser.add_argument("--job", required=True)
    args = parser.parse_args()

    job_path = Path(args.job)
    job = json.loads(job_path.read_text(encoding="utf-8"))

    for item in job["videoPlan"]:
        clip_path = Path("assets") / item["clip"]
        if clip_path.exists():
            print(f"Skipping existing asset: {clip_path}")
            continue
        create_clip(item["overlayText"], clip_path, item["duration"])
        # Marker lets downstream tooling distinguish placeholders from real footage.
        clip_path.with_suffix(".placeholder").touch()
        print(f"✅ Placeholder asset created: {clip_path}")

    print("Done. Replace these placeholder clips with real screen recordings when ready.")


if __name__ == "__main__":
    main()
