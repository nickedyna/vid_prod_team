import argparse
import json
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
    parser.add_argument("--platform", choices=["shorts", "longForm", "linkedin"], default="shorts")
    parser.add_argument("--voiceover", default=None)
    parser.add_argument("--music", default=None)
    args = parser.parse_args()

    job = args.job
    job_data = json.loads(Path(job).read_text(encoding="utf-8"))

    voiceover = args.voiceover
    if not voiceover and args.mode == "full":
        candidate = job_data.get("voiceover")
        if candidate and Path(candidate).exists():
            voiceover = candidate

    run([sys.executable, "scripts/validate_job.py", "--job", job])
    run([sys.executable, "scripts/generate_thumbnail.py", "--job", job])
    run([sys.executable, "scripts/generate_srt.py", "--job", job])

    # Always fill gaps with branded placeholders so the draft renders end to end.
    run([sys.executable, "scripts/create_placeholder_assets.py", "--job", job, "--platform", args.platform])

    cmd = [sys.executable, "scripts/assemble_short.py", "--job", job, "--platform", args.platform]
    if voiceover:
        cmd += ["--voiceover", voiceover]
    if args.music:
        cmd += ["--music", args.music]
    run(cmd)

    pkg_cmd = [
        sys.executable,
        "scripts/build_review_package.py",
        "--job",
        job,
        "--platform",
        args.platform,
    ]
    if voiceover:
        pkg_cmd += ["--voiceover", voiceover]
    if args.music:
        pkg_cmd += ["--music", args.music]
    run(pkg_cmd)

    print("\n✅ Pipeline complete. Review output/review/ before publishing.")


if __name__ == "__main__":
    main()
