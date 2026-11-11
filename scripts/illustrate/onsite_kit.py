"""Drawing kit for the Onsite Operations console (dark theme tokens from packages/ui globals.css).

oklch tokens converted to hex:
  background .145 -> #0a0a0a, card .205 -> #171717, muted/secondary/accent .269 -> #262626,
  muted-foreground .708 -> #a1a1a1, foreground .985 -> #fafafa, primary .922 -> #e5e5e5,
  btn-primary (.8223 .2836 289) -> #c696ff, border white/10, input white/15.
"""
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(__file__))
from ui import Canvas, ORANGE, FONT  # noqa: E402

BG, CARD, MUTED = "#0a0a0a", "#171717", "#262626"
FG, MFG = "#fafafa", "#a1a1a1"
BORDER, BORDER_CARD = "#262626", "#303030"
INPUT_BG, INPUT_BORDER = "#181818", "#2f2f2f"
BTN = "#c696ff"
PRIMARY = "#e5e5e5"
DARK = "#171717"

TONES = {  # bg, border, text
    "neutral": ("#262626", "#303030", "#fafafa"),
    "good": ("#022c22", "#065f46", "#d1fae5"),
    "warn": ("#451a03", "#92400e", "#fef3c7"),
    "bad": ("#450a0a", "#991b1b", "#fee2e2"),
    "info": ("#2e1065", "#5b21b6", "#ede9fe"),
}
TONE_TEXT = {"neutral": FG, "good": "#6ee7b7", "warn": "#fcd34d", "bad": "#fca5a5"}
CALLOUT = {  # bg, border, text (dark variants, /40 blended)
    "bad": ("#2a0a0b", "#7f1d1d", "#fee2e2"),
    "warn": ("#2a1204", "#78350f", "#fef3c7"),
    "info": ("#0f1a33", "#1e3a8a", "#dbeafe"),
}

ICONS = {
    "search": ['<circle cx="11" cy="11" r="8"/>', '<path d="m21 21-4.3-4.3"/>'],
    "arrow-right": ['<path d="M5 12h14"/>', '<path d="m12 5 7 7-7 7"/>'],
    "chevron-right": ['<path d="m9 18 6-6-6-6"/>'],
    "chevron-down": ['<path d="m6 9 6 6 6-6"/>'],
    "alert": ['<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/>',
              '<path d="M12 9v4"/>', '<path d="M12 17h.01"/>'],
    "ticket": ['<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/>',
               '<path d="M13 5v2"/>', '<path d="M13 17v2"/>', '<path d="M13 11v2"/>'],
    "radio": ['<circle cx="12" cy="12" r="2"/>', '<path d="M4.93 19.07a10 10 0 0 1 0-14.14"/>',
              '<path d="M7.76 16.24a6 6 0 0 1 0-8.48"/>', '<path d="M16.24 7.76a6 6 0 0 1 0 8.48"/>',
              '<path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>'],
    "wallet": ['<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/>',
               '<path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>'],
    "users": ['<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>', '<circle cx="9" cy="7" r="4"/>',
              '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/>', '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>'],
    "file-text": ['<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>',
                  '<path d="M14 2v4a2 2 0 0 0 2 2h4"/>', '<path d="M10 9H8"/>', '<path d="M16 13H8"/>',
                  '<path d="M16 17H8"/>'],
    "check": ['<path d="M20 6 9 17l-5-5"/>'],
    "circle-dot": ['<circle cx="12" cy="12" r="10"/>', '<circle cx="12" cy="12" r="1"/>'],
    "x-circle": ['<circle cx="12" cy="12" r="10"/>', '<path d="m15 9-6 6"/>', '<path d="m9 9 6 6"/>'],
    "copy": ['<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>',
             '<path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>'],
}


def tw(s, size=14, weight=400):
    """Rough text width in viewBox units."""
    return len(s) * size * (0.58 if weight >= 600 else 0.55)


def wrap(s, width, size=14, weight=400):
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, size, weight) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class K(Canvas):
    def __init__(self, w, h, bg=BG):
        super().__init__(w, h, bg)
        self.defs = []

    # ---- primitives
    def t(self, x, y, s, size=14, fill=FG, weight=400, anchor="start", mono=False, italic=False):
        fam = ' font-family="ui-monospace,SFMono-Regular,Menlo,monospace"' if mono else ""
        it = ' font-style="italic"' if italic else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{fam}{it}>{escape(s)}</text>')

    def lines(self, x, y, lines, size=13, fill=MFG, weight=400, lh=None):
        lh = lh or size + 5
        for i, ln in enumerate(lines):
            self.t(x, y + i * lh, ln, size, fill, weight)
        return y + len(lines) * lh

    def box(self, x, y, w, h, fill=CARD, stroke=BORDER_CARD, r=10, sw=1, opacity=None):
        o = f' opacity="{opacity}"' if opacity else ""
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}{o}/>')

    def hline(self, x1, x2, y, color=BORDER_CARD):
        self.parts.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="1"/>')

    def vline(self, x, y1, y2, color=BORDER_CARD, sw=1):
        self.parts.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>')

    def dot(self, cx, cy, r, fill):
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>')

    def icon(self, name, x, y, size=16, color=MFG, sw=2):
        sc = size / 24
        self.parts.append(
            f'<g transform="translate({x} {y}) scale({sc})" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">' + "".join(ICONS[name]) + "</g>")

    def fade(self, y, h, w=None, x=0):
        gid = f"f{len(self.defs)}"
        self.defs.append(
            f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{BG}" stop-opacity="1"/></linearGradient>')
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w or self.w}" height="{h}" fill="url(#{gid})"/>')

    # ---- components
    def pill(self, x, y, label, tone="neutral", upper=False, anchor="start"):
        """Badge (rounded-md border px-2 py-0.5 text-xs font-medium). y is top. Returns width."""
        s = label.upper() if upper else label
        w = tw(s, 13, 600) + 18
        if anchor == "end":
            x -= w
        bg, bd, fg = TONES[tone]
        self.box(x, y, w, 24, bg, bd, 6)
        self.t(x + w / 2, y + 17, s, 13, fg, 500, "middle")
        return w

    def button(self, x, y, label, variant="default", h=36, w=None, disabled=False, anchor="start", size=14):
        w = w or tw(label, size, 600) + 32
        if anchor == "end":
            x -= w
        op = 0.5 if disabled else None
        if variant == "default":
            self.box(x, y, w, h, PRIMARY, None, 8, opacity=op)
            self.t(x + w / 2, y + h / 2 + 5, label, size, DARK, 500, "middle")
        elif variant == "cta":
            self.box(x, y, w, h, BTN, None, 8, opacity=op)
            self.t(x + w / 2, y + h / 2 + 5, label, size, DARK, 500, "middle")
        elif variant == "outline":
            self.box(x, y, w, h, INPUT_BG, INPUT_BORDER, 8, opacity=op)
            self.t(x + w / 2, y + h / 2 + 5, label, size, FG, 500, "middle")
        elif variant == "cta-outline":
            self.box(x, y, w, h, INPUT_BG, BTN, 8, opacity=op)
            self.t(x + w / 2, y + h / 2 + 5, label, size, BTN, 500, "middle")
        elif variant == "danger":
            self.box(x, y, w, h, "#dc2626", None, 6)
            self.t(x + w / 2, y + h / 2 + 5, label, size, "#fff", 500, "middle")
        return w

    def input(self, x, y, w, text="", placeholder="", h=36, size=14):
        self.box(x, y, w, h, INPUT_BG, INPUT_BORDER, 8)
        if text:
            self.t(x + 12, y + h / 2 + 5, text, size, FG)
        else:
            self.t(x + 12, y + h / 2 + 5, placeholder, size, MFG)

    def textarea(self, x, y, w, h, text_lines=(), placeholder_lines=()):
        self.box(x, y, w, h, INPUT_BG, INPUT_BORDER, 8)
        if text_lines:
            self.lines(x + 12, y + 23, text_lines, 14, FG, lh=20)
        else:
            self.lines(x + 12, y + 23, placeholder_lines, 14, MFG, lh=20)

    def select(self, x, y, w, text="", placeholder="", h=36):
        self.box(x, y, w, h, INPUT_BG, INPUT_BORDER, 8)
        self.t(x + 12, y + h / 2 + 5, text or placeholder, 14, FG if text else MFG)
        self.icon("chevron-down", x + w - 28, y + h / 2 - 8, 16, MFG)

    def label(self, x, y, text, required=False):
        star = '<tspan fill="#ff6467"> *</tspan>' if required else ""
        self.parts.append(f'<text x="{x}" y="{y}" font-size="14" font-weight="500" fill="{FG}">{escape(text)}{star}</text>')

    def panel(self, x, y, w, h, title, hint=None, action=None, footer=None):
        """Bordered section; returns y of body content start."""
        self.box(x, y, w, h, CARD, BORDER_CARD, 10)
        self.t(x + 16, y + 30, title, 16, FG, 600)
        rx = x + w - 16
        hh = 48
        if action:
            self.t(rx, y + 30, action, 14, BTN, 400, "end")
            rx -= tw(action, 14) + 12
        if hint:
            if tw(title, 16, 600) + tw(hint, 13) + 16 > rx - (x + 16):
                self.t(x + 16, y + 52, hint, 13, MFG)
                hh = 68
            else:
                self.t(rx, y + 29, hint, 13, MFG, 400, "end")
        self.hline(x, x + w, y + hh)
        if footer:
            self.hline(x, x + w, y + h - 38)
            self.t(x + 16, y + h - 14, footer, 13, MFG)
        return y + hh

    def stat(self, x, y, w, h, label, value, foot=(), tone="neutral"):
        self.box(x, y, w, h, CARD, BORDER_CARD, 10)
        self.t(x + 16, y + 27, label, 13, MFG, 500)
        self.t(x + 16, y + 59, value, 24, TONE_TEXT.get(tone, FG), 700)
        self.lines(x + 16, y + 82, foot, 13, MFG, lh=17)

    def note(self, x, y, w, tone, title, body_lines=(), h=None):
        bg, bd, fg = CALLOUT[tone]
        h = h or 22 + 22 + len(body_lines) * 20
        self.box(x, y, w, h, bg, bd, 10)
        self.t(x + 16, y + 28, title, 14, fg, 600)
        self.lines(x + 16, y + 50, body_lines, 14, fg, lh=20)
        return h

    def search_icon_field(self, x, y, w, placeholder, h=36, icon_color=MFG):
        self.input(x, y, w, "", placeholder, h)
        self.icon("search", x + 12, y + h / 2 - 7, 14, icon_color)

    def live(self, xr, y):
        """LIVE pill, right-aligned at xr (top y). Returns width."""
        w = 62
        x = xr - w
        self.box(x, y, w, 26, "#022c22", "#065f46", 6)
        self.dot(x + 14, y + 13, 3.5, "#059669")
        self.t(x + 24, y + 18, "LIVE", 13, "#d1fae5", 500)
        return w

    def header(self, x, y, w, title, eventline=None, subtitle=None, action=None, live=True, pill=None):
        """Console header without workspace nav/breadcrumb. Returns bottom y."""
        self.t(x, y + 30, title, 30, FG, 700)
        yy = y + 30
        if eventline:
            yy += 26
            self.t(x, yy, eventline, 14, MFG)
        if subtitle:
            yy += 21
            self.t(x, yy, subtitle, 14, MFG)
        rx = x + w
        if action:
            bw = self.button(rx, y, action, "default", anchor="end")
            rx -= bw + 8
        if pill:
            pw = self.pill(rx, y + 6, pill[0], pill[1], anchor="end")
            rx -= pw + 8
        if live:
            self.live(rx, y + 5)
        return yy + 10

    def save(self, path):
        clip = f'<clipPath id="pg"><rect width="{self.w}" height="{self.h}"/></clipPath>'
        defs = f"<defs>{clip}{''.join(self.defs)}</defs>"
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'font-family="{FONT}">' + defs + '<g clip-path="url(#pg)">' + "".join(self.parts) + "</g></svg>")
        open(path, "w").write(svg)
