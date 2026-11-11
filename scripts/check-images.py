#!/usr/bin/env python3
"""Flag screenshots that will look blurry, tiny or too tall in the docs. See CAPTURE.md."""
import glob, os, statistics
from PIL import Image, ImageChops

root = os.path.join(os.path.dirname(__file__), '..', 'images')
rows = []
for path in sorted(glob.glob(os.path.join(root, '**', '*.png'), recursive=True)):
    name = os.path.relpath(path, root)
    if name.startswith('favicon'):
        continue
    im = Image.open(path)
    w, h = im.size
    g = im.convert('L')
    low = g.resize((max(1, w // 2), max(1, h // 2)), Image.LANCZOS).resize((w, h), Image.LANCZOS)
    detail = statistics.fmean(ImageChops.difference(g, low).tobytes())
    issues = []
    if w > 1800:
        issues.append('window too wide (text will look tiny); recapture at 1280 px wide, 2x')
    if w > 900 and h / w > 1.3:
        issues.append('too tall; crop to the relevant section')
    if detail < 0.6 and w > 700:
        issues.append('soft; looks upscaled or low-resolution, recapture at 2x')
    rows.append((name, w, h, issues))

for name, w, h, issues in rows:
    mark = 'WARN' if issues else ' ok '
    print(f'[{mark}] {name}  {w}x{h}')
    for i in issues:
        print(f'         - {i}')
flagged = sum(1 for r in rows if r[3])
print(f'\n{flagged} of {len(rows)} images flagged')
