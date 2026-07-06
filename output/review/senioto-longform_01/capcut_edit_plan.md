# CapCut Edit Plan — senioto-longform_01 (Long-Form)

Platform: **longForm** — 1920x1080, 16:9, MP4, 30fps, AAC.
Production mode: **hybrid** (talking head + motion cards + screen-recording b-roll).
Style source: `config/senioto_visual_style.json` (senioto_enterprise_ai) + `docs/REFERENCE_STYLE_GUIDE.md`.

## 1. Import folder

Import the whole folder into a new CapCut Desktop project:

```text
output/review/senioto-longform_01/capcut_import/
  01_draft_short.mp4        ← full draft assembly (use as timing reference track)
  02_voiceover.wav          ← when recorded
  03_music.mp3              ← optional music bed
  04_captions.srt           ← chapter-level captions
  05_thumbnail.jpg          ← thumbnail reference
  06_motion_background.mp4  ← flow map background
```

Also import `assets/talking_head/`, `assets/broll/`, and `assets/motion/` folders directly once real footage exists — the draft MP4 is the placeholder skeleton, and each real clip replaces its placeholder at the same timecode (see `shot_list.md` for the exact 37-shot map).

## 2. Timeline structure (tracks, top to bottom)

1. **Text overlays / keyword pops** — on-screen text from the shot list.
2. **Lower thirds + chapter cards** — see styles below.
3. **B-roll / motion graphics** — cutaways over the talking head.
4. **Talking head** — base video track.
5. **Voiceover** — primary audio.
6. **Music bed** — secondary audio, ducked.
7. **SFX** — soft whooshes on chapter cards only.

Workflow: lay the voiceover down first, cut the talking head to it, then place chapter cards at the 10 chapter boundaries (0:00, 0:40, 1:20, 2:20, 3:20, 4:40, 6:40, 7:50, 8:50, 9:20), then fill b-roll cutaways per the shot list.

## 3. Chapter cards

- Style: midnight blue `#0B1220` background with subtle grid, oversized electric-blue `#2563EB` chapter number top-left, soft-white bold title (max 4 words), cyan-teal `#14B8A6` underline sweeping left→right (400ms).
- In: hard cut. Out: 200ms cross-dissolve into the section.
- Duration: 4–5s each. Soft whoosh, no impact hit.
- Build once in CapCut as a compound clip, duplicate 8x, change number + title.

## 4. Captions and keyword overlays

- Long-form uses **keyword pops**, not full subtitles: 1–4 word phrases synced to VO, soft white `#F8FAFC` bold, amber `#F59E0B` for the key noun, pop-in scale 95%→100% over 150ms.
- Import `04_captions.srt` only as a chapter-level guide, or enable YouTube captions from the voiceover at upload.
- Persistent lower-third strap "Brief → Agent → HTML → QA → ZIP" during the whole section 6 walkthrough (4:40–6:40).

## 5. Lower third

- First talking-head appearance (0:00–0:15) and after each chapter card: "Nat O'Farril" / "Senioto — Learn AI. Build proof. Grow your value."
- Electric-blue 6px left rule, deep-navy panel at 80% opacity, slide in from left 250ms, hold 4s, slide out.

## 6. Talking-head treatment

- Punch-ins (108–112%) on: "wrong" (0:05), "a download, not a skill" (2:30), "one finished system beats twenty toys" (3:58), "five minutes and no patience" (8:40).
- Optional: `assets/motion/overlays/talking_head_tech_frame.mov` as a corner frame overlay during bridge segments.
- Color: keep neutral, slight contrast lift; the backdrop should read near-black navy, not gray.

## 7. B-roll cutaway rules

- Never let the talking head run past ~15s without a cutaway or punch-in (reference pacing: visual change every 33–45s max, we cut faster).
- Screen recordings play at 100–130% speed with cursor highlights.
- The ZIP-open shot is the signature beat — give it a 0.5s hold with a soft riser before chapter 06.

## 8. Music and audio mastering

- Voice is primary: target -14 LUFS integrated, -1 dBTP ceiling. High-pass at 80Hz, gentle 3–5kHz presence lift.
- Music bed at **8–15% under voice**, auto-duck 3–4dB under speech (CapCut audio ducking on).
- Music: clean corporate tech, no vocals; subtle energy lift at chapter cards and the CTA. If no licensed track, ship voice-only.
- SFX: soft whoosh on chapter cards, single soft riser before the ZIP reveal. Nothing else.

## 9. End card (9:40–10:00)

- Subscribe button pulse (amber `#F59E0B` fill, navy text) + next-video preview slot on the right.
- Keep VO's final line finishing over the end card, then 2s of music-only tail.

## 10. Final export

```text
Resolution: 1920x1080
Aspect: 16:9
Format: MP4
Frame rate: 30fps (or source-matched)
Bitrate: high / recommended
Audio: AAC, voice primary
```

Upload with `metadata.json` (title, description with chapters, tags, pinned comment). Thumbnail: rebuild `05_thumbnail.jpg` in Canva per the thumbnail spec in `config/senioto_visual_style.json` (3-line stack, blue highlight bar, amber arrow, talking head right).

No automated publishing. Human review before upload.
