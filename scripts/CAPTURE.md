# Screenshot capture standard

Sharp, consistently sized screenshots. Follow this and nothing needs resizing afterwards.

## Set up
- Use a **demo organization** with fake data: names and emails at `@example.com`, no real revenue, no client events.
- Use **dark mode** for every shot, so the docs look consistent.
- Browser window **1280 px wide** (CSS px) at **2x pixel density** (any Retina Mac does this by default; in Chrome DevTools use the device toolbar, 1280 x 800, DPR 2).
  - Why: the docs column is about 700 px wide. A 2,000+ px-wide window shrinks UI text to a third of its size; a 1280 window at 2x stays readable and crisp.

## Capture
- **Crop to what the reader needs**: one section, dialog or panel. Do not capture a whole page when a section makes the point.
- Aim for an aspect ratio no taller than about 1.2 (height / width). If a page is long, capture the relevant section only. No scroll stitching.
- Save as **PNG**. Never resize, upscale, re-save as JPEG, or screenshot a screenshot.
- Dialogs: capture at natural size with a little margin; they do not need to match full-page widths.

## Callouts
- Number steps with orange circles (1, 2, 3...) next to the element, and an orange outline around it. Keep the same style on every shot.
- Number in the order the page text refers to them.

## Name and place
- Save at the path in `SCREENSHOTS.md` (for example `images/events/rsvp-page-overview.png`).
- Replace the marker in the page with:
  `<Frame><img src="/images/events/rsvp-page-overview.png" alt="Short description" /></Frame>`
- Run `python3 scripts/check-images.py` and fix anything it flags.
