import argparse
import json
from pathlib import Path


def to_srt_timestamp(time_value: str) -> str:
    """Convert M:SS or H:MM:SS timestamp into SRT timestamp format."""
    parts = [int(p) for p in time_value.split(":")]
    if len(parts) == 2:
        hours = 0
        minutes, seconds = parts
    elif len(parts) == 3:
        hours, minutes, seconds = parts
    else:
        raise ValueError(f"Invalid timestamp: {time_value}")
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},000"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an SRT caption file from a job JSON file.")
    parser.add_argument("--job", required=True, help="Path to job JSON.")
    parser.add_argument("--output", default=None, help="Output SRT path.")
    args = parser.parse_args()

    job_path = Path(args.job)
    job = json.loads(job_path.read_text(encoding="utf-8"))

    output = Path(args.output) if args.output else Path("output/captions") / f"{job_path.stem}.srt"
    output.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    for index, caption in enumerate(job["captions"], start=1):
        lines.append(str(index))
        lines.append(f"{to_srt_timestamp(caption['timeStart'])} --> {to_srt_timestamp(caption['timeEnd'])}")
        lines.append(caption["text"])
        lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Captions written: {output}")


if __name__ == "__main__":
    main()
