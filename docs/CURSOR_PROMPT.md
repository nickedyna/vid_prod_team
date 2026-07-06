# Cursor / Codex Implementation Prompt

Use this prompt inside Cursor or Codex after cloning the repo.

```text
You are my senior AI video automation engineer.

Project: vid_prod_team
Goal: Build a local-first AI video production pipeline for the AI Email Dev brand.

Current system:
- jobs/*.json contains structured video production specs.
- scripts/validate_job.py validates job JSON.
- scripts/generate_thumbnail.py creates thumbnails.
- scripts/generate_srt.py creates captions.
- scripts/create_placeholder_assets.py creates placeholder b-roll clips.
- scripts/assemble_short.py assembles a vertical YouTube Short.
- scripts/run_job.py runs the preview pipeline.

Your tasks:
1. Review the repo structure.
2. Run the preview pipeline locally.
3. Fix any errors in MoviePy/Pillow setup.
4. Improve the Short assembly to support:
   - text overlays from videoPlan
   - burned-in captions
   - simple transitions
   - avatar picture-in-picture
   - optional voiceover and music
5. Add tests for job validation and timestamp conversion.
6. Add a simple CLI command:
   python scripts/run_job.py --job jobs/brief-to-zip_01.json --mode preview
7. Keep everything local-first and human-reviewable.
8. Do not add automatic publishing yet.

Brand constraints:
- No fake guru language.
- No income guarantees.
- Focus on proof-of-work, enterprise marketing, AI email development, and human review.
- Default slogan: Learn AI. Build proof. Grow your value.
```
