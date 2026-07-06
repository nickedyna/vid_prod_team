import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("\n$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local AI video production pipeline.")
    parser.add_argument("--job", required=True, help="Path to job JSON.")
    parser.add_argument("--mode", choices=["preview", "full"], default="preview")
    parser.add_argument("--voiceover", default=None)
    parser.add_argument("--music", default=None)
    args = parser.parse_args()

    job = args.job

    run([sys.executable, "scripts/validate_job.py", "--job", job])
    run([sys.executable, "scripts/generate_thumbnail.py", "--job", job])
    run([sys.executable, "scripts/generate_srt.py", "--job", job])

    if args.mode == "preview":
        run([sys.executable, "scripts/create_placeholder_assets.py", "--job", job])

    cmd = [sys.executable, "scripts/assemble_short.py", "--job", job]
    if args.voiceover:
        cmd += ["--voiceover", args.voiceover]
    if args.music:
        cmd += ["--music", args.music]
    run(cmd)

    print("\n✅ Pipeline complete. Review output/ before publishing.")


if __name__ == "__main__":
    main()
