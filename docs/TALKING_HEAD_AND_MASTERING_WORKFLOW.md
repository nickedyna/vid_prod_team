# Talking Head and Final Mastering Workflow

This workflow supports both faceless videos and videos that include Nat's talking-head clips.

## Modes

### 1. Faceless Short

Uses:
- b-roll
- motion graphics backgrounds
- avatar overlays
- captions
- voiceover

Best for:
- fast daily Shorts
- tutorial teasers
- proof-of-work clips

### 2. Talking-Head Short

Uses:
- Nat's recorded camera clips
- motion background or frame overlay
- caption overlays
- b-roll cutaways
- CTA end card

Best for:
- motivational clips
- credibility-building commentary
- personal story clips

### 3. Hybrid Long Form

Uses:
- talking head for intro/outro
- screen recordings for demos
- motion cards for chapters
- generated captions/SRT
- final mastered audio

Best for:
- full tutorials
- build-in-public episodes
- course-style lessons

## Suggested folder structure

```text
assets/talking_head/
  nat_intro_01.mp4
  nat_reaction_01.mp4
  nat_cta_01.mp4

assets/motion/backgrounds/
  enterprise_grid_pulse.mp4
  brief_to_zip_flow_map.mp4
  code_rain_lite.mp4
  corporate_war_room.mp4

assets/motion/overlays/
  talking_head_tech_frame.mov
  ai_email_dev_corner_bug.png

assets/motion/lower_thirds/
  nat_lower_third.mp4

assets/motion/end_cards/
  subscribe_end_card.mp4
```

## Job JSON extension idea

Future job files can include this section:

```json
"productionMode": "hybrid",
"visualStyle": "enterprise_grid_pulse",
"talkingHead": {
  "enabled": true,
  "clips": [
    {
      "clip": "talking_head/nat_intro_01.mp4",
      "role": "hook",
      "duration": 8
    }
  ],
  "frameOverlay": "motion/overlays/talking_head_tech_frame.mov"
},
"mastering": {
  "targetLoudness": "-14 LUFS",
  "truePeak": "-1 dBTP",
  "musicDuckPercent": 15,
  "captionStyle": "bold_center_bottom"
}
```

## Final editing/mastering checklist

Before publishing:

- [ ] Hook lands in first 2 seconds.
- [ ] Captions are readable on mobile.
- [ ] Voice is clear over music.
- [ ] No copyrighted music or borrowed footage without rights.
- [ ] Thumbnail is readable at phone size.
- [ ] CTA is clear.
- [ ] No income guarantees.
- [ ] Video teaches, demonstrates, or adds original commentary.
- [ ] Description and pinned comment match the video.

## Mastering targets

For YouTube/social:

- Voice should be the loudest element.
- Music should sit under voice at roughly 12% to 18%.
- Avoid harsh clipping.
- Keep captions in the safe zone away from platform UI.
- Export Shorts as 1080x1920 MP4.
- Export long form as 1920x1080 MP4.

## Cursor build path

Ask Cursor to add:

1. `productionMode` support: `faceless`, `talking_head`, `hybrid`.
2. `visualStyle` support: choose a motion background automatically.
3. Talking-head clip handling.
4. Avatar picture-in-picture.
5. Caption burn-in.
6. Final review package export.
7. Long-form assembly script after Shorts pipeline is stable.
