import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an AI video production job JSON file.")
    parser.add_argument("--job", required=True, help="Path to the job JSON file.")
    parser.add_argument(
        "--schema",
        default="jobs/schema/video_job.schema.json",
        help="Path to the JSON schema.",
    )
    parser.add_argument(
        "--check-assets",
        action="store_true",
        help="Also warn about missing b-roll asset files.",
    )
    args = parser.parse_args()

    job_path = Path(args.job)
    schema_path = Path(args.schema)

    job = load_json(job_path)
    schema = load_json(schema_path)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(job), key=lambda e: e.path)

    if errors:
        print(f"❌ Job failed schema validation: {job_path}")
        for error in errors:
            location = "/".join(str(p) for p in error.path) or "root"
            print(f" - {location}: {error.message}")
        raise SystemExit(1)

    print(f"✅ Job schema valid: {job_path}")

    if args.check_assets:
        missing = []
        for item in job.get("videoPlan", []):
            clip_path = Path("assets") / item["clip"]
            if not clip_path.exists():
                missing.append(str(clip_path))

        if missing:
            print("⚠️ Missing b-roll assets:")
            for path in missing:
                print(f" - {path}")
            print("Run: python scripts/create_placeholder_assets.py --job", job_path)
        else:
            print("✅ All referenced b-roll assets exist.")


if __name__ == "__main__":
    main()
