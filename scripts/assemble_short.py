import argparse
import json
from pathlib import Path

from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip

TARGET_SIZE = (1080, 1920)


def load_clip(path: Path, duration: float):
    if not path.exists():
        raise FileNotFoundError(f"Missing clip: {path}. Run create_placeholder_assets.py or add real b-roll.")

    clip = VideoFileClip(str(path))
    clip = clip.subclip(0, min(duration, clip.duration))
    clip = clip.resize(height=TARGET_SIZE[1])
    if clip.w < TARGET_SIZE[0]:
        clip = clip.resize(width=TARGET_SIZE[0])
    clip = clip.crop(x_center=clip.w / 2, y_center=clip.h / 2, width=TARGET_SIZE[0], height=TARGET_SIZE[1])
    return clip


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble a YouTube Short from a job JSON videoPlan.")
    parser.add_argument("--job", required=True)
    parser.add_argument("--voiceover", default=None, help="Optional voiceover audio file.")
    parser.add_argument("--music", default=None, help="Optional music bed file.")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    job_path = Path(args.job)
    job = json.loads(job_path.read_text(encoding="utf-8"))
    output = Path(args.output) if args.output else Path("output/shorts") / f"{job_path.stem}.mp4"
    output.parent.mkdir(parents=True, exist_ok=True)

    clips = []
    for item in job["videoPlan"]:
        clip_path = Path("assets") / item["clip"]
        clips.append(load_clip(clip_path, item["duration"]))

    final = concatenate_videoclips(clips, method="compose")

    audio_tracks = []
    if args.voiceover:
        voice = AudioFileClip(args.voiceover).volumex(1.0)
        audio_tracks.append(voice)
    if args.music:
        music = AudioFileClip(args.music).volumex(0.15).set_duration(final.duration)
        audio_tracks.append(music)

    if audio_tracks:
        final = final.set_audio(CompositeAudioClip(audio_tracks))

    final.write_videofile(str(output), fps=30, codec="libx264", audio_codec="aac")
    print(f"✅ Short written: {output}")


if __name__ == "__main__":
    main()
