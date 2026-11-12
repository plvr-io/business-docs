#!/usr/bin/env python3
"""Check localized docs against the English source.

Reports, per locale defined in docs.json:
  - English pages with no translated file (or missing from that locale's nav)
  - translated pages whose internal links point at the English tree (missing locale prefix)

Usage: python3 scripts/check-i18n.py   (exit code 1 if anything is wrong)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
docs = json.loads((ROOT / "docs.json").read_text())
langs = docs["navigation"]["languages"]


def nav_pages(lang):
    return [p for t in lang.get("tabs", []) for g in t["groups"] for p in g["pages"]]


en = next(l for l in langs if l["language"] == "en")
en_pages = nav_pages(en)
sections = sorted({p.split("/")[0] for p in en_pages})
# root-relative doc links that skip the locale prefix, e.g. ](/tickets/concepts) or href="/onsite/cases"
unprefixed = re.compile(r'(?:\]\(|href=")/(?:' + "|".join(map(re.escape, sections)) + r')(?=[/)#"])')

problems = 0
for lang in langs:
    if lang is en:
        continue
    pages = nav_pages(lang)
    folder = pages[0].split("/")[0]
    missing_nav = [p for p in en_pages if f"{folder}/{p}" not in pages]
    missing_file = [p for p in en_pages if not (ROOT / folder / f"{p}.mdx").exists()]
    bad_links = []
    for f in sorted((ROOT / folder).rglob("*.mdx")):
        for n, line in enumerate(f.read_text().splitlines(), 1):
            if unprefixed.search(line):
                bad_links.append(f"{f.relative_to(ROOT)}:{n}")
    count = len(missing_nav) + len(missing_file) + len(bad_links)
    problems += count
    print(f"[{lang['language']}] {len(en_pages) - len(missing_file)}/{len(en_pages)} pages translated"
          + ("" if count else " — OK"))
    for p in missing_file:
        print(f"  missing file: {folder}/{p}.mdx")
    for p in missing_nav:
        print(f"  missing from nav: {folder}/{p}")
    for loc in bad_links:
        print(f"  unprefixed link: {loc}")

sys.exit(1 if problems else 0)
