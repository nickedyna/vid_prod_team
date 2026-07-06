# VID Prod Team

AI-powered video production pipeline for the **AI Email Dev** brand.

This repo turns a single structured video job JSON file into a repeatable production workflow for YouTube Shorts and long-form videos.

## Brand

**Nat O’Farril / AI Email Dev**

Default slogan:

> Learn AI. Build proof. Grow your value.

Default CTA:

> Subscribe if you want to become the AI-powered email developer companies cannot ignore.

## What this project does

This repo is designed to become your autonomous-but-human-reviewed video production team:

1. Accept a video job JSON file.
2. Validate the creative plan.
3. Generate thumbnails from brand text and avatar assets.
4. Generate captions/SRT files.
5. Assemble a draft Short from b-roll, overlays, captions, avatar, voiceover, and music.
6. Prepare YouTube metadata.
7. Keep you as the final human reviewer before publish.

## Project structure

```text
vid_prod_team/
  assets/
    avatar/              # avatar images or transparent PNGs
    broll/               # reusable screen recordings and motion clips
    music/               # royalty-free music beds
    voiceover/           # recorded voiceover files
  docs/
    AGENT_LOOP.md
    ASSET_NAMING.md
    CURSOR_PROMPT.md
    MONETIZATION_AND_COMPLIANCE.md
  jobs/
    brief-to-zip_01.json
    schema/video_job.schema.json
  output/
    captions/
    shorts/
    thumbnails/
  prompts/
    ai_email_dev_brand_agent.md
    ai_video_production_agent.md
  scripts/
    assemble_short.py
    create_placeholder_assets.py
    generate_srt.py
    generate_thumbnail.py
    run_job.py
    validate_job.py
```

## Quick start

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python scripts/run_job.py --job jobs/intro-video_01.json --mode preview --platform shorts
```

After recording the voiceover:

```bash
python scripts/run_job.py --job jobs/intro-video_01.json --mode full --platform shorts --voiceover assets/voiceover/intro-video_01_voiceover.wav
```

Each run produces a CapCut-ready review package in `output/review/<job-name>/` with the draft Short, thumbnail, captions, metadata, production notes, CapCut edit plan, import manifest, and a `capcut_import/` folder.

## Human-in-the-loop workflow

1. Write or generate a job JSON file in `jobs/`.
2. Run validation.
3. Generate thumbnails and captions.
4. Assemble the draft video.
5. Review manually in CapCut, Premiere, DaVinci, or directly from `output/shorts/`.
6. Publish only after human approval.

## Current milestone

The first milestone is a working local pipeline for the first Short:

**The Overlooked Path Into Enterprise Marketing: AI Email Development**

This Short supports the larger AI Email Dev roadmap and the Brief-to-ZIP demo series.
