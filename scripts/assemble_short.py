import argparse
import json
from pathlib import Path

from moviepy import (
    AudioFileClip,
    CompositeAudioClip,
    VideoFileClip,
    concatenate_videoclips,
)

PLATFORM_SIZES = {
    "shorts": (1080, 1920),
    "longForm": (1920, 1080),
    "linkedin": (1080, 1350),
}


def load_clip(path: Path, duration: float, target_size: tuple[int, int]):
    if not path.exists():
        raise FileNotFoundError(f"Missing clip: {path}. Run create_placeholder_assets.py or add real b-roll.")

    clip = VideoFileClip(str(path))
    clip = clip.subclipped(0, min(duration, clip.duration))
    clip = clip.resized(height=target_size[1])
    if clip.w < target_size[0]:
        clip = clip.resized(width=target_size[0])
    clip = clip.cropped(x_center=clip.w / 2, y_center=clip.h / 2, width=target_size[0], height=target_size[1])
    return clip


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble a video from a job JSON videoPlan.")
    parser.add_argument("--job", required=True)
    parser.add_argument("--platform", choices=list(PLATFORM_SIZES), default="shorts")
    parser.add_argument("--voiceover", default=None, help="Optional voiceover audio file.")
    parser.add_argument("--music", default=None, help="Optional music bed file.")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    target_size = PLATFORM_SIZES[args.platform]

    job_path = Path(args.job)
    job = json.loads(job_path.read_text(encoding="utf-8"))
    output = Path(args.output) if args.output else Path("output/shorts") / f"{job_path.stem}.mp4"
    output.parent.mkdir(parents=True, exist_ok=True)

    clips = []
    for item in job["videoPlan"]:
        clip_path = Path("assets") / item["clip"]
        clips.append(load_clip(clip_path, item["duration"], target_size))

    final = concatenate_videoclips(clips, method="compose")

    audio_tracks = []
    if args.voiceover:
        if Path(args.voiceover).exists():
            audio_tracks.append(AudioFileClip(args.voiceover))
        else:
            print(f"⚠️ Voiceover not found, rendering silent draft: {args.voiceover}")
    if args.music:
        if Path(args.music).exists():
            music = AudioFileClip(args.music).with_volume_scaled(0.15)
            if music.duration > final.duration:
                music = music.subclipped(0, final.duration)
            audio_tracks.append(music)
        else:
            print(f"⚠️ Music not found, skipping music bed: {args.music}")

    if audio_tracks:
        final = final.with_audio(CompositeAudioClip(audio_tracks))

    final.write_videofile(str(output), fps=30, codec="libx264", audio_codec="aac")
    print(f"✅ Short written: {output}")


if __name__ == "__main__":
    main()
