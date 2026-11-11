"""Drawing kit for the Tickets / Payment Links illustrations.

Tokens come from packages/ui/src/styles/globals.css (.dark block), converted
from oklch to hex. Components mirror shadcn sizes used by the Business Portal
(h-9 inputs and selects, rounded-md = 8, text-sm = 14).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from xml.sax.saxutils import escape
from ui import Canvas, ORANGE

BG = "#0a0a0a"        # --background
CARD = "#171717"      # --card / --popover
MUTED = "#262626"     # --muted / --secondary / --accent
FG = "#fafafa"
MFG = "#a1a1a1"       # --muted-foreground
BTN = "#c696ff"       # --btn-primary (dark)
BTN_FG = "#171717"    # --primary-foreground (dark)
GREEN5, GREEN6 = "#22c55e", "#16a34a"
GRAY5, NEUT4 = "#6b7280", "#a3a3a3"
AMBER5 = "#f59e0b"
RED5, RED = "#ef4444", "#ff6467"
ORANGE5 = "#f97316"
YELLOW5 = "#eab308"
BORDER_OP = 0.10      # --border: white 10%
INPUT_OP = 0.15       # --input: white 15%

ICONS = {
    "plus": ['<path d="M5 12h14M12 5v14"/>'],
    "search": ['<circle cx="11" cy="11" r="8"/>', '<path d="m21 21-4.3-4.3"/>'],
    "pencil": ['<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/>', '<path d="m15 5 4 4"/>'],
    "chevron-right": ['<path d="m9 18 6-6-6-6"/>'],
    "chevron-left": ['<path d="m15 18-6-6 6-6"/>'],
    "chevron-down": ['<path d="m6 9 6 6 6-6"/>'],
    "chevron-up": ['<path d="m18 15-6-6-6 6"/>'],
    "chevrons-up-down": ['<path d="m7 15 5 5 5-5"/>', '<path d="m7 9 5-5 5 5"/>'],
    "chevrons-left": ['<path d="m11 17-5-5 5-5"/>', '<path d="m18 17-5-5 5-5"/>'],
    "chevrons-right": ['<path d="m6 17 5-5-5-5"/>', '<path d="m13 17 5-5-5-5"/>'],
    "grip": ['<circle cx="9" cy="12" r="1"/>', '<circle cx="9" cy="5" r="1"/>', '<circle cx="9" cy="19" r="1"/>',
             '<circle cx="15" cy="12" r="1"/>', '<circle cx="15" cy="5" r="1"/>', '<circle cx="15" cy="19" r="1"/>'],
    "history": ['<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>', '<path d="M3 3v5h5"/>', '<path d="M12 7v5l4 2"/>'],
    "rotate-ccw": ['<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>', '<path d="M3 3v5h5"/>'],
    "copy": ['<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>', '<path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>'],
    "trash": ['<path d="M3 6h18"/>', '<path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>', '<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>', '<path d="M10 11v6"/>', '<path d="M14 11v6"/>'],
    "x": ['<path d="M18 6 6 18"/>', '<path d="m6 6 12 12"/>'],
    "download": ['<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>', '<path d="m7 10 5 5 5-5"/>', '<path d="M12 15V3"/>'],
    "upload": ['<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>', '<path d="m17 8-5-5-5 5"/>', '<path d="M12 3v12"/>'],
    "calendar": ['<path d="M8 2v4"/>', '<path d="M16 2v4"/>', '<rect width="18" height="18" x="3" y="4" rx="2"/>', '<path d="M3 10h18"/>'],
    "more-vertical": ['<circle cx="12" cy="12" r="1"/>', '<circle cx="12" cy="5" r="1"/>', '<circle cx="12" cy="19" r="1"/>'],
    "info": ['<circle cx="12" cy="12" r="10"/>', '<path d="M12 16v-4"/>', '<path d="M12 8h.01"/>'],
    "triangle-alert": ['<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/>', '<path d="M12 9v4"/>', '<path d="M12 17h.01"/>'],
    "circle-check": ['<circle cx="12" cy="12" r="10"/>', '<path d="m9 12 2 2 4-4"/>'],
    "circle-check-big": ['<path d="M21.801 10A10 10 0 1 1 17 3.335"/>', '<path d="m9 11 3 3L22 4"/>'],
    "arrow-up-from-line": ['<path d="m18 9-6-6-6 6"/>', '<path d="M12 3v14"/>', '<path d="M5 21h14"/>'],
    "file-spreadsheet": ['<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>', '<path d="M14 2v4a2 2 0 0 0 2 2h4"/>', '<path d="M8 13h2"/>', '<path d="M14 13h2"/>', '<path d="M8 17h2"/>', '<path d="M14 17h2"/>'],
    "check": ['<path d="M20 6 9 17l-5-5"/>'],
    "circle-dashed": ['<path d="M10.1 2.182a10 10 0 0 1 3.8 0"/>', '<path d="M13.9 21.818a10 10 0 0 1-3.8 0"/>', '<path d="M17.609 3.721a10 10 0 0 1 2.69 2.7"/>', '<path d="M2.182 13.9a10 10 0 0 1 0-3.8"/>', '<path d="M20.279 17.609a10 10 0 0 1-2.7 2.69"/>', '<path d="M21.818 10.1a10 10 0 0 1 0 3.8"/>', '<path d="M3.721 6.391a10 10 0 0 1 2.7-2.69"/>', '<path d="M6.391 20.279a10 10 0 0 1-2.69-2.7"/>'],
    "circle-slash": ['<circle cx="12" cy="12" r="10"/>', '<path d="M9 15 15 9"/>'],
    "sort-up": ['<path d="m8 14 4-4 4 4"/>'],
    "sort-down": ['<path d="m8 10 4 4 4-4"/>'],
}


def est(s, size=14, bold=False):
    return len(s) * size * (0.56 if bold else 0.53)


class K(Canvas):
    def __init__(self, w, h):
        super().__init__(w, h, BG)

    # ---- primitives
    def box(self, x, y, w, h, fill=None, stroke=None, r=8, so=1.0, op=None, sw=1):
        a = [f'x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"']
        a.append(f'fill="{fill}"' if fill else 'fill="none"')
        if op is not None and fill:
            a.append(f'fill-opacity="{op}"')
        if stroke:
            a.append(f'stroke="{stroke}" stroke-opacity="{so}" stroke-width="{sw}"')
        self.parts.append(f'<rect {" ".join(a)}/>')

    def line(self, x1, y1, x2, y2, color="#fff", op=BORDER_OP, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-opacity="{op}" stroke-width="{sw}"{d}/>')

    def t(self, x, y, s, size=14, fill=FG, weight=400, anchor="start", op=None, deco=None):
        extra = (f' fill-opacity="{op}"' if op is not None else "") + (f' text-decoration="{deco}"' if deco else "")
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{extra}>{escape(s)}</text>')

    def dot(self, cx, cy, r, fill):
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>')

    def icon(self, name, x, y, size=16, color=FG, sw=2, op=None):
        s = size / 24
        o = f' stroke-opacity="{op}"' if op is not None else ""
        self.parts.append(
            f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{color}"{o} stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{"".join(ICONS[name])}</g>')

    # ---- components
    def surface(self, x, y, w, h, r=8):
        """rounded-md border on background."""
        self.box(x, y, w, h, BG, "#fff", r, BORDER_OP)

    def card(self, x, y, w, h, r=14):
        self.box(x, y, w, h, CARD, "#fff", r, BORDER_OP)

    def label(self, x, y, s, color=FG):
        """FormLabel: text-sm font-medium. y is the baseline."""
        self.t(x, y, s, 14, color, 500)

    def desc(self, x, y, s):
        self.t(x, y, s, 14, MFG)

    def field(self, x, y, w, value="", placeholder="", h=36, prefix=None, icon=None, disabled=False,
              mono=False, right_icon=None):
        op = 0.5 if disabled else 1
        self.box(x, y, w, h, "#fff", "#fff", 8, INPUT_OP, op=0.045)
        if disabled:
            self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{BG}" fill-opacity="0.35"/>')
        tx = x + 12
        if icon:
            self.icon(icon, x + 8, y + (h - 16) / 2, 16, MFG)
            tx = x + 32
        if prefix:
            self.t(x + 12, y + h / 2 + 5, prefix, 14, MFG)
            tx = x + 46
        if value:
            self.t(tx, y + h / 2 + 5, value, 14, FG, op=op)
        elif placeholder:
            self.t(tx, y + h / 2 + 5, placeholder, 14, MFG)
        if right_icon:
            self.icon(right_icon, x + w - 24, y + (h - 16) / 2, 16, MFG, op=0.7)

    def textarea(self, x, y, w, h, value="", placeholder="", lines=None):
        self.box(x, y, w, h, "#fff", "#fff", 8, INPUT_OP, op=0.045)
        yy = y + 24
        if value:
            for ln in (lines or [value]):
                self.t(x + 12, yy, ln, 14, FG)
                yy += 20
        else:
            for ln in (lines or [placeholder]):
                self.t(x + 12, yy, ln, 14, MFG)
                yy += 20

    def select(self, x, y, w, value=None, placeholder=None, dot=None, h=36, disabled=False, hint=None,
               clear=False, chevron=True, small=False):
        op = 0.5 if disabled else 1
        self.box(x, y, w, h, "#fff", "#fff", 8, INPUT_OP, op=0.045)
        cy = y + h / 2
        tx = x + 12
        if dot:
            self.dot(x + 16, cy, 4, dot)
            tx = x + 28
        if value is not None:
            self.t(tx, cy + 5, value, 14, FG, op=op)
            if hint:
                self.t(tx + est(value) + 8, cy + 5, hint, 14, MFG, op=op)
        elif placeholder is not None:
            self.t(tx, cy + 5, placeholder, 14, MFG)
        if chevron:
            self.icon("chevron-down", x + w - 28 + (0 if not clear else -20), cy - 8, 16, MFG, op=0.5 * op)
        if clear:
            self.icon("x", x + w - 28, cy - 8, 16, MFG, op=0.6)

    def button(self, x, y, w, label, variant="default", icon=None, h=36, color=None, size=14):
        fill, fg, stroke, sop, fop = BTN, BTN_FG, None, 1, None
        if variant == "outline":
            fill, fg, stroke, sop, fop = "#fff", BTN, BTN, 1, 0.045
        elif variant == "secondary":
            fill, fg = MUTED, FG
        elif variant == "ghost":
            fill, fg = None, FG
        elif variant == "plain-outline":
            fill, fg, stroke, sop, fop = "#fff", FG, "#fff", INPUT_OP, 0.045
        if color:
            fg = color
        if fill:
            self.box(x, y, w, h, fill, stroke, 8, sop, op=fop)
        elif stroke:
            self.box(x, y, w, h, None, stroke, 8, sop)
        cy = y + h / 2
        iw = 16 + 8 if icon else 0
        tw = est(label, size, True) if label else 0
        sx = x + (w - tw - iw) / 2
        if icon:
            self.icon(icon, sx, cy - 8, 16, fg)
        if label:
            self.t(sx + iw, cy + 5, label, size, fg, 500)

    def icon_button(self, x, y, icon, size=36, color=FG, box=False):
        if box:
            self.box(x, y, size, size, MUTED, None, 8)
        self.icon(icon, x + (size - 16) / 2, y + (size - 16) / 2, 16, color)

    def switch(self, x, y, on=True, color=BTN):
        w, h = 32, 18.4
        self.box(x, y, w, h, color if on else "#fff", None, 9.2, op=None if on else 0.12)
        tx = x + w - 17 if on else x + 1
        self.dot(tx + 8, y + h / 2, 8, BTN_FG if on else FG)

    def checkbox(self, x, y, on=True):
        self.box(x, y, 16, 16, BTN if on else "#fff", "#fff" if not on else BTN, 4, INPUT_OP, op=None if on else 0.045)
        if on:
            self.icon("check", x + 2, y + 2, 12, BTN_FG, 3)

    def tabs(self, x, y, items, active=0, w=None, widths=None):
        """TabsList: h-9, bg-muted, rounded-lg, p-[3px]; active trigger is raised."""
        widths = widths or [int(est(s, 14, True)) + 20 for s in items]
        total = w or sum(widths) + 6
        if w:
            widths = [(w - 6) / len(items)] * len(items)
        self.box(x, y, total, 36, MUTED, None, 10)
        cx = x + 3
        for i, (s, wd) in enumerate(zip(items, widths)):
            if i == active:
                self.box(cx, y + 3, wd, 30, "#fff", "#fff", 8, INPUT_OP, op=0.045)
            self.t(cx + wd / 2, y + 23, s, 14, FG if i == active else MFG, 500, "middle")
            cx += wd
        return total

    def badge_pill(self, x, y, s, fill, size=13, color="#fff", icon=None, h=22):
        iw = 18 if icon else 0
        w = len(s) * size * 0.6 + 18 + iw
        self.box(x, y, w, h, fill, None, h / 2)
        tx = x + 8
        if icon:
            self.icon(icon, tx, y + (h - 14) / 2, 14, color, 2)
            tx += iw
        self.t(tx, y + h / 2 + 4.5, s, size, color, 600)
        return w

    def chip(self, x, y, s, size=13):
        """bg-accent text-muted-foreground rounded text-xs px-1."""
        w = est(s, size) + 10
        self.box(x, y, w, 20, MUTED, None, 4)
        self.t(x + 5, y + 14.5, s, size, MFG)
        return w

    def progress(self, x, y, pct, on, w=112, tick=98):
        self.box(x, y, w, 6, MUTED, None, 3)
        if pct > 0:
            self.box(x, y, max(6, w * pct / 100), 6, GREEN5 if on else NEUT4, None, 3)
        tx = x + w * tick / 100
        self.parts.append(f'<rect x="{tx - 0.5}" y="{y - 2}" width="1" height="10" fill="{FG}" fill-opacity="0.4"/>')

    def th(self, x, y, s, **kw):
        self.t(x, y, s, 14, FG, 500, **kw)

    def kv_row(self, x, y, w, k, v, bold=False):
        self.t(x, y, k, 14, FG, 700 if bold else 400)
        self.t(x + w, y, v, 14, FG, 700 if bold else 400, "end")

    def flag(self, x, y, kind):
        w, h = 18, 12
        self.parts.append(f'<clipPath id="fl{x}{y}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2"/></clipPath><g clip-path="url(#fl{x}{y})">')
        if kind == "SG":
            self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h/2}" fill="#ef3340"/><rect x="{x}" y="{y+h/2}" width="{w}" height="{h/2}" fill="#fff"/>')
        elif kind == "JP":
            self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/><circle cx="{x+w/2}" cy="{y+h/2}" r="3.4" fill="#bc002d"/>')
        elif kind == "DE":
            self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="4" fill="#000"/><rect x="{x}" y="{y+4}" width="{w}" height="4" fill="#dd0000"/><rect x="{x}" y="{y+8}" width="{w}" height="4" fill="#ffce00"/>')
        elif kind == "FR":
            self.parts.append(f'<rect x="{x}" y="{y}" width="6" height="{h}" fill="#0055a4"/><rect x="{x+6}" y="{y}" width="6" height="{h}" fill="#fff"/><rect x="{x+12}" y="{y}" width="6" height="{h}" fill="#ef4135"/>')
        self.parts.append('</g>')

    def qr(self, x, y, size=200, seed=7):
        """Decorative fake QR-like pattern (not scannable)."""
        n = 25
        c = size / n
        self.box(x, y, size, size, "#fff", None, 0)
        import random
        rnd = random.Random(seed)

        def finder(fx, fy):
            self.box(x + fx * c, y + fy * c, 7 * c, 7 * c, "#000", None, 0)
            self.box(x + (fx + 1) * c, y + (fy + 1) * c, 5 * c, 5 * c, "#fff", None, 0)
            self.box(x + (fx + 2) * c, y + (fy + 2) * c, 3 * c, 3 * c, "#000", None, 0)
        for i in range(n):
            for j in range(n):
                if (i < 8 and j < 8) or (i > n - 9 and j < 8) or (i < 8 and j > n - 9):
                    continue
                if rnd.random() < 0.5:
                    self.parts.append(f'<rect x="{x + i * c:.1f}" y="{y + j * c:.1f}" width="{c:.1f}" height="{c:.1f}" fill="#000"/>')
        finder(0, 0); finder(n - 7, 0); finder(0, n - 7)

    def callout_at(self, x, y, n):
        self.callout(x, y, n)

    def edge_cut(self, x, y, w, top=True):
        """Fade-less crop edge: nothing to draw, kept for readability of scripts."""
        pass
