"""Dark-theme drawing helpers for the Business Portal (tokens from packages/ui globals.css .dark)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from xml.sax.saxutils import escape
from ui import Canvas, ORANGE, FONT

BG, CARD, SEC = "#0a0a0a", "#171717", "#262626"
FG, MUTED = "#fafafa", "#a1a1a1"
BTN = "#c696ff"          # --btn-primary (dark)
BTN_FG = "#171717"       # --primary-foreground (dark)
RED = "#ef4444"          # text-red-500
GREEN = "#22c55e"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

ICONS = {
    "plus": ['M5 12h14', 'M12 5v14'],
    "pencil": ['M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z', 'M15 5l4 4'],
    "trash": ['M3 6h18', 'M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6', 'M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2'],
    "trash2": ['M3 6h18', 'M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6', 'M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2', 'M10 11v6', 'M14 11v6'],
    "copy": ['M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2'],
    "check": ['M20 6 9 17l-5-5'],
    "chevdown": ['m6 9 6 6 6-6'],
    "search": ['m21 21-4.3-4.3'],
    "x": ['M18 6 6 18', 'M6 6l12 12'],
    "upload": ['M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4', 'M17 8l-5-5-5 5', 'M12 3v12'],
    "export": ['m18 9-6-6-6 6', 'M12 3v14', 'M5 21h14'],
    "image": ['m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21'],
    "pin": ['M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0'],
    "circlecheck": ['m9 12 2 2 4-4'],
}
EXTRA = {
    "copy": '<rect x="8" y="8" width="14" height="14" rx="2"/>',
    "search": '<circle cx="11" cy="11" r="8"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/>',
    "pin": '<circle cx="12" cy="10" r="3"/>',
    "circlecheck": '<circle cx="12" cy="12" r="10"/>',
}


class UI(Canvas):
    def __init__(self, w, h, bg=BG):
        super().__init__(w, h, bg)

    def box(self, x, y, w, h, fill=None, r=6, stroke=None, so=0.1, sw=1, fo=1):
        f = f'fill="{fill}"' if fill else 'fill="none"'
        if fill and fo != 1: f += f' fill-opacity="{fo}"'
        s = f' stroke="{stroke}" stroke-opacity="{so}" stroke-width="{sw}"' if stroke else ""
        self.parts.append(f'<rect x="{x+.5 if stroke else x}" y="{y+.5 if stroke else y}" '
                          f'width="{w-1 if stroke else w}" height="{h-1 if stroke else h}" rx="{r}" {f}{s}/>')

    def t(self, x, y, s, size=14, fill=FG, weight=400, anchor="start", font=None):
        ff = f' font-family="{font}"' if font else ""
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
                          f'text-anchor="{anchor}"{ff}>{escape(s)}</text>')

    def tc(self, x, cy, s, size=14, **k):
        """text with vertical centre at cy"""
        self.t(x, round(cy + size * 0.35, 1), s, size, **k)

    def line(self, x1, y1, x2, y2, so=0.1, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-opacity="{so}" stroke-width="{sw}"{d}/>')

    def icon(self, name, x, y, size=16, color=FG, sw=2):
        sc = size / 24
        paths = "".join(f'<path d="{p}"/>' for p in ICONS[name])
        self.parts.append(
            f'<g transform="translate({x} {y}) scale({sc})" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{EXTRA.get(name,"")}{paths}</g>')

    # --- components ---
    def cta(self, x, y, w, label, h=36, icon=None):
        self.box(x, y, w, h, BTN, 6)
        iw = 16 + 8 if icon else 0
        tw = len(label) * 7.6
        sx = x + (w - tw - iw) / 2
        if icon: self.icon(icon, sx, y + h / 2 - 8, 16, BTN_FG)
        self.tc(sx + iw, y + h / 2, label, 14, fill=BTN_FG, weight=500)

    def outline_btn(self, x, y, w, label, h=36, icon=None, color=FG):
        self.box(x, y, w, h, "#fff", 6, stroke="#fff", so=0.15, fo=0.045)
        iw = 16 + 8 if icon else 0
        tw = len(label) * 7.6
        sx = x + (w - tw - iw) / 2
        if icon: self.icon(icon, sx, y + h / 2 - 8, 16, color)
        self.tc(sx + iw, y + h / 2, label, 14, fill=color, weight=500)

    def input(self, x, y, w, text, h=36, color=FG, size=14, weight=400, icon=None, r=6):
        self.box(x, y, w, h, "#fff", r, stroke="#fff", so=0.15, fo=0.045)
        tx = x + 12
        if icon:
            self.icon(icon, x + 12, y + h / 2 - 8, 16, MUTED); tx = x + 40
        self.tc(tx, y + h / 2, text, size, fill=color, weight=weight)

    def select(self, x, y, w, text, h=36, color=FG):
        self.box(x, y, w, h, "#fff", 6, stroke="#fff", so=0.15, fo=0.045)
        self.tc(x + 12, y + h / 2, text, 14, fill=color)
        self.parts.append(f'<g opacity=".5">')
        self.icon("chevdown", x + w - 28, y + h / 2 - 8, 16, MUTED)
        self.parts.append('</g>')

    def label(self, x, y, s, req=False, size=14):
        self.tc(x, y, s, size, weight=500)
        return

    def popover(self, x, y, w, h):
        self.parts.append(f'<rect x="{x}" y="{y+2}" width="{w}" height="{h}" rx="6" fill="#000" fill-opacity=".25"/>')
        self.box(x, y, w, h, CARD, 6, stroke="#fff", so=0.1)

    def callout(self, x, y, n):
        super().callout(x, y, n)

    def ring(self, x, y, w, h, r=8):
        super().ring(x, y, w, h, r)

    def save(self, path):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'font-family="{FONT}">' + "".join(self.parts) + "</svg>")
        open(path, "w").write(svg)
