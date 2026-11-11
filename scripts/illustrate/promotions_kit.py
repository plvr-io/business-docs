"""Drawing kit for the Promotions pages (dark theme tokens from packages/ui globals.css)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from xml.sax.saxutils import escape
from ui import Canvas, FONT, ORANGE

# oklch tokens converted to sRGB hex
BG, FG, CARD = "#0a0a0a", "#fafafa", "#171717"
MUTED, MFG = "#262626", "#a1a1a1"
PRIM, PRIMFG = "#e5e5e5", "#171717"      # --primary / --primary-foreground (plain Button)
BTN = "#c696ff"                          # --btn-primary (CtaButton)
BORDER = "#232323"                       # white 10% over background
BORDER_CARD = "#2e2e2e"                  # white 10% over card
INPUT_BORDER = "#2f2f2f"                 # white 15%
INPUT_BG = "#151515"                     # input/30 over background
GREEN, GRAY, ORANGE500, RED = "#22c55e", "#6b7280", "#f97316", "#ff6467"

ICON_DIR = ("/Users/a57/src/github.com/plvr-io/plvr-client/node_modules/.pnpm/"
            "lucide-react@0.554.0_react@19.1.0/node_modules/lucide-react/dist/esm/icons")


def tw(s, size=14, weight=400):
    return len(s) * size * (0.56 if weight < 500 else 0.58 if weight < 600 else 0.6)


def _attrs(d):
    return "".join(f' {k}="{v}"' for k, v in d.items() if k != "key")


def icon_svg(name, x, y, size=16, color=FG, sw=2):
    src = open(f"{ICON_DIR}/{name}.js").read()
    m = re.search(r"from '\./(.+?)\.js'", src)
    if "__iconNode" not in src and m:
        return icon_svg(m.group(1), x, y, size, color, sw)
    body = src.split("const __iconNode = ")[1].split("];")[0] + "]"
    els = re.findall(r'\[\s*"(\w+)",\s*(\{.*?\})\s*\]', body, re.S)
    out = []
    for tag, attrs in els:
        d = dict(re.findall(r'(\w+): "(.*?)"', attrs))
        out.append(f"<{tag}{_attrs(d)}/>")
    s = size / 24
    return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">' + "".join(out) + "</g>")


class K(Canvas):
    def icon(self, name, x, y, size=16, color=FG, sw=2):
        self.parts.append(icon_svg(name, x, y, size, color, sw))

    def t(self, x, y, s, size=14, fill=FG, weight=400, anchor="start", mono=False):
        fam = ' font-family="ui-monospace,Menlo,Consolas,monospace"' if mono else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{fam}>{escape(s)}</text>')

    def rich(self, x, y, parts, size=14, fill=FG, anchor="start"):
        """parts = [(text, weight)] in one text element so spacing is exact."""
        spans = "".join(f'<tspan font-weight="{w}">{escape(t)}</tspan>' for t, w in parts)
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" xml:space="preserve">{spans}</text>')

    def line(self, x1, y1, x2, y2, color=BORDER, w=1):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"/>')

    def circle(self, cx, cy, r, fill):
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>')

    # --- buttons -------------------------------------------------
    def cta(self, x, y, label, ic=None, outline=False, h=36, w=None, disabled=False, plain_icon_gap=8):
        """CtaButton (blocks/button): filled --btn-primary or outline with btn-primary border/text."""
        pad = 16 if not ic else 12
        w = w or int(pad * 2 + tw(label, 14, 500) + (16 + 8 if ic else 0))
        op = 0.5 if disabled else 1
        self.parts.append(f'<g opacity="{op}">')
        if outline:
            self.rect(x, y, w, h, INPUT_BG, 6, BTN)
            col = BTN
        else:
            self.rect(x, y, w, h, BTN, 6)
            col = PRIMFG
        cx = x + pad
        if ic:
            self.icon(ic, cx, y + h / 2 - 8, 16, col)
            cx += 24
        self.t(cx, y + h / 2 + 5, label, 14, col, 500)
        self.parts.append("</g>")
        return w

    def btn(self, x, y, label, ic=None, outline=False, h=36, w=None, ic_right=False, pad=None):
        """Plain ui Button: default (bg-primary) or outline (border-input)."""
        pad = pad or (16 if not ic else 12)
        w = w or int(pad * 2 + tw(label, 14, 500) + (16 + 8 if ic else 0))
        if outline:
            self.rect(x, y, w, h, INPUT_BG, 6, INPUT_BORDER)
            col = FG
        else:
            self.rect(x, y, w, h, PRIM, 6)
            col = PRIMFG
        cx = x + pad
        if ic:
            self.icon(ic, cx, y + h / 2 - 8, 16, col)
            cx += 24
        self.t(cx, y + h / 2 + 5, label, 14, col, 500)
        return w

    def icon_btn(self, x, y, name, size=36, ghost=True, outline=False):
        if outline:
            self.rect(x, y, size, size, INPUT_BG, 6, INPUT_BORDER)
        self.icon(name, x + size / 2 - 8, y + size / 2 - 8, 16, FG)

    # --- form controls ------------------------------------------
    def field(self, x, y, w, value=None, placeholder=None, h=36, icon_right=None, prefix=None):
        self.rect(x, y, w, h, INPUT_BG, 6, INPUT_BORDER)
        tx = x + 12
        if prefix:
            self.t(tx, y + h / 2 + 5, prefix, 14, MFG)
            tx += 20 if prefix == "%" else 32
        if value:
            self.t(tx, y + h / 2 + 5, value, 14, FG)
        elif placeholder:
            self.t(tx, y + h / 2 + 5, placeholder, 14, MFG)
        if icon_right:
            self.icon(icon_right, x + w - 28, y + h / 2 - 8, 16, MFG)

    def select(self, x, y, w, value=None, placeholder=None, h=36, dot=None):
        self.rect(x, y, w, h, INPUT_BG, 6, INPUT_BORDER)
        tx = x + 12
        if dot:
            self.circle(tx + 4, y + h / 2, 4, dot)
            tx += 16
        if value:
            self.t(tx, y + h / 2 + 5, value, 14, FG)
        else:
            self.t(tx, y + h / 2 + 5, placeholder or "", 14, MFG)
        self.icon("chevron-down", x + w - 28, y + h / 2 - 8, 16, "#6e6e6e")

    def switch(self, x, y, on=False):
        # h-[1.15rem] w-8  (18.4 x 32)
        self.rect(x, y, 32, 18.4, "#e5e5e5" if on else "#3a3a3a", 9.2)
        cx = x + (32 - 9 - 1) if on else x + 9.2
        self.circle(cx, y + 9.2, 8, "#171717" if on else FG)

    def label(self, x, y, s, req=False):
        self.t(x, y, s, 14, FG, 500)

    def dot_menu(self, x, y):
        self.icon("ellipsis-vertical", x + 10, y + 10, 16, FG)

    # --- page pieces ---------------------------------------------
    def page_header(self, x, y, title, subtitle):
        self.t(x, y + 18, title, 20, FG, 600)
        self.t(x, y + 42, subtitle, 14, MFG)

    def metric(self, x, y, w, label, value, unit=None, h=84):
        self.rect(x, y, w, h, BG, 6, BORDER)
        self.t(x + 20, y + 30, label, 14, MFG)
        self.t(x + 20, y + 62, value, 20, FG, 700)
        if unit:
            self.t(x + 20 + tw(value, 20, 700) + 8, y + 62, unit, 13, MFG)

    def pill(self, x, y, label, fill, ic=None, h=24):
        w = int(16 + tw(label, 14, 600) + (18 if ic else 0))
        self.rect(x, y, w, h, fill, h / 2)
        cx = x + 8
        if ic:
            self.icon(ic, cx, y + h / 2 - 7, 14, "#fff")
            cx += 18
        self.t(cx, y + h / 2 + 5, label, 14, "#fff", 600)
        return w

    def sort_tri(self, x, y):
        # two stacked dim triangles (SortIcon), ~ 8 wide
        c = "#4a4a4a"
        self.parts.append(f'<path d="M{x},{y-1} l4,-5 l4,5 z" fill="{c}"/>')
        self.parts.append(f'<path d="M{x},{y+1} l4,5 l4,-5 z" fill="{c}"/>')

    def table_frame(self, x, y, w, h):
        self.rect(x, y, w, h, BG, 6, BORDER)

    def row_line(self, x, y, w):
        self.line(x, y, x + w, y, BORDER)

    def dialog(self, x, y, w, h):
        self.rect(x, y, w, h, BG, 8, BORDER_CARD)

    def dialog_close(self, x, y):
        self.icon("x", x, y, 16, MFG)

    def overlay(self, w, h):
        self.parts.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#000" fill-opacity="0.5"/>')

    def drop(self, x, y, w, items, hl=None):
        """DropdownMenuContent with icon items. items=[(icon,label)]"""
        h = 8 + len(items) * 32
        self.rect(x, y, w, h, CARD, 6, BORDER_CARD)
        for i, (ic, lab) in enumerate(items):
            yy = y + 4 + i * 32
            if hl == i:
                self.rect(x + 4, yy, w - 8, 32, MUTED, 4)
            self.icon(ic, x + 12, yy + 8, 16, MFG)
            self.t(x + 36, yy + 21, lab, 14, FG)
        return h

    def save(self, path):
        super().save(path)
