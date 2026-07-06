# Agent Loop Architecture

This project is designed around a practical human-in-the-loop agent workflow.

## Loop overview

```text
Campaign/video idea
  ↓
AI Email Dev Brand Agent
  ↓
AI Video Production Agent
  ↓
Video job JSON
  ↓
Validation script
  ↓
Thumbnail + captions + draft video
  ↓
Human review in CapCut/Cursor/local preview
  ↓
Publish or revise
  ↓
Performance notes feed the next job
```

## Agent roles

### 1. Brand Strategist Agent

Owns positioning, tone, audience, and CTA.

Output:

- video angle
- audience promise
- hook options
- CTA
- monetization link idea

### 2. Script Agent

Turns the video angle into:

- 60-second Short script
- 5-minute long-form script
- caption timing plan

### 3. Production Planner Agent

Maps the script to exact reusable assets.

Output:

- `videoPlan`
- b-roll filenames
- motion direction
- transition notes

### 4. Thumbnail Agent

Outputs:

- headline
- subhead
- CTA
- emotional angle

### 5. QA Agent

Checks:

- fake guru risk
- copyright risk
- monetization safety
- caption clarity
- no income guarantees
- clear CTA

## Current implementation

The current repo uses one consolidated job JSON file. In future versions, the agents can be split into separate API calls that each enrich the same JSON object.

## Human approval gates

Do not publish automatically until these are reviewed:

- final script
- generated voiceover
- thumbnail
- final MP4
- YouTube title/description

## Scaling path

Version 1: local scripts + manual upload.

Version 2: Cursor/Codex can improve scripts and create a web UI.

Version 3: server queue that accepts briefs and generates drafts.

Version 4: client-facing portal for a video production company.
