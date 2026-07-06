# CapCut Finishing Workflow

CapCut is the finishing station for creator-friendly polish after the repo generates the structured video package.

## Reality of the integration

At this stage, treat CapCut as a **human-in-the-loop finishing tool**, not a fully automated headless renderer.

The repo should generate a CapCut-ready review package containing:

```text
output/review/<job-name>/
  short.mp4
  thumbnail.jpg
  captions.srt
  metadata.json
  production_notes.md
  capcut_edit_plan.md
  capcut_import_manifest.json
```

Nat then imports the media package into CapCut, applies final polish, reviews it, and exports the final video.

## Why this is the safest workflow

CapCut is excellent for fast creator editing, captions, overlays, templates, and final social polish. But the reliable automation layer should stay in this repo:

- job JSON
- captions/SRT
- thumbnails
- b-roll draft
- metadata
- edit notes
- review package

CapCut becomes the final visual polish layer.

## CapCut import folder

Each job should export an import-ready folder:

```text
output/review/brief-to-zip_01/capcut_import/
  01_draft_short.mp4
  02_voiceover.wav
  03_music.mp3
  04_captions.srt
  05_thumbnail.jpg
  06_motion_background.mp4
  07_talking_head_frame.mov
  08_end_card.mp4
```

## CapCut edit plan

The repo should generate `capcut_edit_plan.md` with:

- timeline order
- punch-in moments
- caption styling notes
- b-roll cutaways
- music volume guidance
- transition suggestions
- final export settings

## CapCut manual finishing steps

1. Open CapCut Desktop.
2. Create a new project.
3. Import the full `capcut_import/` folder.
4. Add `01_draft_short.mp4` to the timeline.
5. Import `04_captions.srt` if using editable captions.
6. Apply the AI Email Dev caption style:
   - bold white text
   - amber highlight on key proof phrases
   - bottom safe-zone placement
   - high contrast background if needed
7. Add talking-head frame overlay if the job uses talking-head mode.
8. Add motion background or b-roll cutaways as needed.
9. Set music under voice at roughly 10% to 18%.
10. Export final video as 1080x1920 MP4 for Shorts.

## CapCut export settings

### YouTube Shorts / TikTok / Reels

```text
Resolution: 1080x1920
Aspect ratio: 9:16
Format: MP4
Frame rate: 30fps or source-matched
Bitrate: high / recommended
Audio: AAC
```

### YouTube long form

```text
Resolution: 1920x1080
Aspect ratio: 16:9
Format: MP4
Frame rate: 30fps or source-matched
Bitrate: high / recommended
Audio: AAC
```

## CapCut role in the agent team

### Local repo agents

Generate:

- script
- job JSON
- draft MP4
- captions
- thumbnail
- metadata
- import manifest
- edit plan

### CapCut finishing agent

Guides:

- final pacing
- caption polish
- punch-ins
- transitions
- b-roll cutaways
- talking-head cleanup
- music ducking
- final export settings

### Human reviewer

Approves:

- voice clarity
- edit quality
- brand fit
- claims safety
- final publish

## Future automation options

Version 1:
Manual CapCut import and export from generated review package.

Version 2:
Generate CapCut-ready edit decision notes and asset manifest.

Version 3:
If CapCut exposes a usable API or project-file workflow in your environment, add a connector that creates draft projects automatically.

Version 4:
Support multiple finishing apps: CapCut, DaVinci Resolve, Premiere Pro, and FFmpeg-only final exports.
