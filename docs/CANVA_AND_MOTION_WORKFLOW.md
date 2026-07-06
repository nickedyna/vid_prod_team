# Canva and Motion Graphics Workflow

This workflow adds a design layer to the AI video production system.

## Current connector reality

The repo is built so Canva can be added later through an API/connector or handled manually from exported assets.

For now, Canva should be treated as a design and template system, while Cursor/local Python handles the repeatable asset generation and packaging.

## Recommended creative stack

### Local automation

Use the repo for:

- JSON video jobs
- generated thumbnails
- generated captions
- placeholder b-roll
- MP4 draft assembly
- production notes
- asset naming consistency

### Canva

Use Canva for:

- high-polish thumbnail templates
- animated intro/outro cards
- motion graphics backgrounds
- quote cards
- lower-third designs
- course/workshop promo slides
- talking-head frame overlays

### CapCut / DaVinci / Premiere

Use editing software for:

- final timing polish
- audio mastering
- manual jump cuts
- talking-head cleanup
- export review

## Canva template categories to create

Create these Canva templates manually first, then export them as MP4/PNG assets into this repo.

```text
Canva Project: AI Email Dev Motion Pack

Templates:
1. AI Email Dev Thumbnail
2. Animated Hook Background
3. Brief-to-ZIP Workflow Background
4. Talking Head Tech Frame
5. Lower Third - Nat O’Farril
6. Proof-of-Work Quote Card
7. Subscribe End Card
8. Long Form Chapter Card
9. Workshop Promo Slide
10. Lead Magnet PDF Promo
```

## Export locations

Export Canva files into these repo paths:

```text
assets/motion/backgrounds/
assets/motion/overlays/
assets/motion/lower_thirds/
assets/motion/end_cards/
assets/canva/exports/
```

## Motion background options for AI Email Dev

### 1. Enterprise Grid Pulse

Look:
Dark navy background, subtle grid, slow blue/teal pulse, faint data lines.

Best for:
- AI email workflow videos
- serious enterprise topics
- long-form intros

Filename:

```text
assets/motion/backgrounds/enterprise_grid_pulse.mp4
```

### 2. Brief-to-ZIP Flow Map

Look:
Animated workflow nodes: Brief → AI Agent → HTML → QA → ZIP.

Best for:
- proof-of-work demos
- system-building videos
- Shorts about automation

Filename:

```text
assets/motion/backgrounds/brief_to_zip_flow_map.mp4
```

### 3. Code Rain Lite

Look:
Soft HTML/code snippets moving slowly in the background, not Matrix-style, more corporate tech.

Best for:
- HTML email development
- Copilot/Cursor content
- technical breakdowns

Filename:

```text
assets/motion/backgrounds/code_rain_lite.mp4
```

### 4. Corporate War Room

Look:
Blurred dashboard wall, marketing metrics, email previews, QA checkmarks.

Best for:
- enterprise marketing strategy
- career positioning
- agency/client-style videos

Filename:

```text
assets/motion/backgrounds/corporate_war_room.mp4
```

### 5. Talking Head Tech Frame

Look:
Transparent overlay frame with title bar, lower third, subtle animated corners.

Best for:
- Nat talking-head clips
- expert commentary
- course/workshop clips

Filename:

```text
assets/motion/overlays/talking_head_tech_frame.mov
```

## Talking-head integration

If a job includes Nat talking-head footage, use this asset pattern:

```json
{
  "clip": "talking_head/nat_intro_01.mp4",
  "duration": 8,
  "overlayText": "This is the overlooked path into enterprise marketing.",
  "motion": "center crop with talking_head_tech_frame overlay",
  "transition": "quick cut"
}
```

## Canva prompt for manual template creation

Paste this into Canva or use as a design brief:

```text
Create a modern AI Email Dev motion graphics template pack for a YouTube channel about AI-powered email development, enterprise marketing automation, proof-of-work projects, and career growth.

Brand tone: confident, practical, motivational, technically credible, not fake guru.

Visual style: dark navy, teal, electric blue, warm amber accents, clean enterprise tech UI, subtle grids, workflow nodes, HTML email/code details, QA checkmarks, ZIP/package iconography, modern lower-thirds.

Text themes:
- Learn AI. Build proof. Grow your value.
- From overlooked to enterprise-ready.
- Brief → AI Agent → HTML → QA → ZIP
- AI Email Dev
- Proof-of-work gets you noticed.

Create templates for:
1. YouTube thumbnail
2. Short intro hook card
3. Animated background
4. Talking-head frame
5. Lower third
6. End card
7. Long-form chapter card
```

## Automation path

Version 1:
Manual Canva exports copied into `assets/motion/`.

Version 2:
Cursor reads job JSON and selects motion background by `visualStyle`.

Version 3:
Canva API/connector creates design exports from JSON.

Version 4:
Full client portal: brief in, video package out.
