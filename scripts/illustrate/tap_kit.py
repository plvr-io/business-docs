"""SVG kit for PLVR Tap illustrations. Tokens come from packages/ui globals.css (.dark),
converted from oklch. Components mirror packages/ui + business-portal markup."""
from xml.sax.saxutils import escape

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
BG, CARD, MUTEDBG = "#0a0a0a", "#171717", "#262626"
FG, MFG = "#fafafa", "#a1a1a1"
BORDER, INPUT_B, INPUT_F = "#232323", "#2f2f2f", "#151515"
BTN, BTN_FG = "#c696ff", "#171717"        # --btn-primary / --primary-foreground (dark)
DEST = "#ff6467"
GREEN, GRAY = "#22c55e", "#6b7280"        # tailwind green-500 / gray-500
EMERALD7 = "#047857"
ORANGE = "#FF7A1A"

ICONS = {
    "plus": ["M5 12h14", "M12 5v14"],
    "pencil": ["M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z", "m15 5 4 4"],
    "chevron-down": ["m6 9 6 6 6-6"],
    "chevron-right": ["m9 18 6-6-6-6"],
    "chevron-left": ["m15 18-6-6 6-6"],
    "chevrons-up-down": ["m7 15 5 5 5-5", "m7 9 5-5 5 5"],
    "search": ["m21 21-4.3-4.3", "C"],
    "x": ["M18 6 6 18", "m6 6 12 12"],
    "check": ["M20 6 9 17l-5-5"],
    "download": ["M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4", "m7 10 5 5 5-5", "M12 15V3"],
    "upload": ["M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4", "m17 8-5-5-5 5", "M12 3v12"],
    "arrow-up-from-line": ["m18 9-6-6-6 6", "M12 3v14", "M5 21h14"],
    "arrow-right": ["M5 12h14", "m12 5 7 7-7 7"],
    "info": ["O", "M12 16v-4", "M12 8h.01"],
    "copy": ["R8", "M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"],
    "external-link": ["M15 3h6v6", "M10 14 21 3", "M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"],
    "banknote": ["B", "M6 12h.01", "M18 12h.01"],
    "credit-card": ["K", "M2 10h20"],
    "qr-code": ["Q1", "Q2", "Q3", "M21 16h-3a2 2 0 0 0-2 2v3", "M21 21v.01", "M12 7v3a2 2 0 0 1-2 2H7", "M3 12h.01", "M12 3h.01", "M12 16v.01", "M16 12h1", "M21 12v.01", "M12 21v-1"],
    "landmark": ["M10 18v-7", "M11.12 2.198a2 2 0 0 1 1.76.006l7.866 3.847c.476.233.31.949-.22.949H3.474c-.53 0-.695-.716-.22-.949z", "M14 18v-7", "M18 18v-7", "M3 22h18", "M6 18v-7"],
    "more-horizontal": ["D12,12", "D19,12", "D5,12"],
    "image": ["I", "D9,9", "m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"],
    "grip-vertical": ["D9,12", "D9,5", "D9,19", "D15,12", "D15,5", "D15,19"],
    "venus-and-mars": ["M10 20h4", "M12 16v6", "M17 2h4v4", "m21 2-5.46 5.46", "M12 12a5 5 0 1 0 0-.01"],
    "globe": ["O", "M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20", "M2 12h20"],
    "phone": ["M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"],
    "cake": ["M20 21v-8a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8", "M4 16s.5-1 2-1 2.5 2 4 2 2.5-2 4-2 2.5 2 4 2 2-1 2-1", "M2 21h20", "M7 8v3", "M12 8v3", "M17 8v3", "M7 4h.01", "M12 4h.01", "M17 4h.01"],
    "id-card": ["M16 10h2", "M16 14h2", "M6.17 15a3 3 0 0 1 5.66 0", "D9,11", "R2"],
    # sidebar
    "chart-line": ["M3 3v16a2 2 0 0 0 2 2h16", "m19 9-5 5-4-4-3 3"],
    "pencil-line": ["M12 20h9", "M16.376 3.622a1 1 0 0 1 3.002 3.002L7.368 18.635a2 2 0 0 1-.855.506l-2.872.838a.5.5 0 0 1-.62-.62l.838-2.872a2 2 0 0 1 .506-.854z", "m15 5 3 3"],
    "ticket": ["M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z", "M13 5v2", "M13 17v2", "M13 11v2"],
    "nfc": ["M6 8.32a7.43 7.43 0 0 1 0 7.36", "M9.46 6.21a11.76 11.76 0 0 1 0 11.58", "M12.91 4.1a15.91 15.91 0 0 1 .01 15.8", "M16.37 2a20.16 20.16 0 0 1 0 20"],
    "headset": ["M3 11h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5Zm0 0a9 9 0 1 1 18 0m0 0v5a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3Z", "M21 16v2a4 4 0 0 1-4 4h-5"],
    "user-cog": ["M10 15H6a4 4 0 0 0-4 4v2", "D18,18", "U10,7", "m21.7 16.4-.9-.3", "m15.2 19.9-.9-.3", "m16.6 21.7.3-.9", "m19.1 15.2.3-.9", "m19.6 21.7-.4-1", "m16.8 15.3-.4-1", "m14.3 16.6 1-.4", "m20.7 17.8 1-.4"],
    "tag": ["M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z", "D7.5,7.5"],
    "fingerprint": ["M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4", "M14 13.12c0 2.38 0 6.38-1 8.88", "M17.29 21.02c.12-.6.43-2.3.5-3.02", "M2 12a10 10 0 0 1 18-6", "M2 16h.01", "M21.8 16c.2-2 .131-5.354 0-6", "M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2", "M8.65 22c.21-.66.45-1.32.57-2", "M9 6.8a6 6 0 0 1 9 5.2v2"],
}


def _icon_svg(name):
    out = []
    for p in ICONS[name]:
        if p == "O":
            out.append('<circle cx="12" cy="12" r="10"/>')
        elif p == "C":
            out.append('<circle cx="11" cy="11" r="8"/>')
        elif p == "R8":
            out.append('<rect x="8" y="8" width="14" height="14" rx="2"/>')
        elif p == "R2":
            out.append('<rect x="2" y="4" width="20" height="16" rx="2"/>')
        elif p == "B":
            out.append('<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2"/>')
        elif p == "K":
            out.append('<rect x="2" y="5" width="20" height="14" rx="2"/>')
        elif p == "I":
            out.append('<rect x="3" y="3" width="18" height="18" rx="2"/>')
        elif p == "Q1":
            out.append('<rect x="3" y="3" width="5" height="5" rx="1"/>')
        elif p == "Q2":
            out.append('<rect x="16" y="3" width="5" height="5" rx="1"/>')
        elif p == "Q3":
            out.append('<rect x="3" y="16" width="5" height="5" rx="1"/>')
        elif p == "U10,7":
            out.append('<circle cx="10" cy="7" r="4"/>')
        elif p.startswith("D"):
            cx, cy = p[1:].split(",")
            r = 3 if name == "user-cog" else 1
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>')
        else:
            out.append(f'<path d="{p}"/>')
    return "".join(out)


def tw(s, size=14, weight=400):
    """Rough text width estimate for the system sans stack."""
    narrow, wide = set("ijlt.,:;'|!()/ I"), set("mwMW")
    n = 0.0
    for ch in s:
        if ch in narrow:
            n += 0.33
        elif ch in wide:
            n += 0.85
        elif ch.isupper():
            n += 0.68
        elif ch.isdigit():
            n += 0.56
        else:
            n += 0.565
    k = 1.05 if weight >= 600 else (1.02 if weight >= 500 else 1.0)
    return n * size * k


class T:
    def __init__(self, w, h, bg=BG):
        self.w, self.h, self.bg = w, h, bg
        self.parts, self.defs, self._id = [], [], 0
        self.rect(0, 0, w, h, bg, r=0)

    # ---- primitives
    def rect(self, x, y, w, h, fill=CARD, r=6, stroke=None, op=None, sw=1):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{o}{s}/>')

    def line(self, x1, y1, x2, y2, color=BORDER, sw=1):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>')

    def circle(self, cx, cy, r, fill, stroke=None):
        s = f' stroke="{stroke}"' if stroke else ""
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{s}/>')

    def text(self, x, cy, s, size=14, fill=FG, weight=400, anchor="start", mono=False, clip=None):
        fam = f' font-family="{MONO}"' if mono else ""
        c = f' clip-path="url(#{clip})"' if clip else ""
        self.parts.append(
            f'<text x="{x}" y="{cy}" dy=".35em" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{fam}{c}>{escape(s)}</text>')

    def clip(self, x, y, w, h):
        self._id += 1
        i = f"c{self._id}"
        self.defs.append(f'<clipPath id="{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')
        return i

    def icon(self, name, x, y, size=16, color=FG, sw=2, op=None):
        o = f' opacity="{op}"' if op else ""
        self.parts.append(
            f'<g transform="translate({x} {y}) scale({size / 24})" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{o}>{_icon_svg(name)}</g>')

    # ---- controls
    def btn(self, x, y, label, kind="outline", icon=None, h=36, w=None, fg=None):
        """kind: cta (blocks/Button), outline (components/Button), ghost."""
        pad = 16 if not icon else 12
        content = tw(label, 14, 500) + (24 if icon else 0)
        bw = w or content + pad * 2
        if kind == "cta":
            self.rect(x, y, bw, h, BTN, 6)
            col = BTN_FG
        elif kind == "outline":
            self.rect(x + .5, y + .5, bw - 1, h - 1, "#ffffff", 6, INPUT_B, op=0.045)
            col = fg or FG
        else:
            col = fg or FG
        if kind == "ghost" and w:
            pass
        sx = x + (bw - content) / 2
        cy = y + h / 2
        if icon:
            self.icon(icon, sx, cy - 8, 16, col)
            self.text(sx + 24, cy, label, 14, col, 500)
        else:
            self.text(sx, cy, label, 14, col, 500)
        return bw

    def icon_btn(self, x, y, name, size=36, isz=16, color=FG):
        self.icon(name, x + (size - isz) / 2, y + (size - isz) / 2, isz, color)

    def select(self, x, y, w, value, dot=None, h=36, color=FG, disabled=False):
        self.rect(x + .5, y + .5, w - 1, h - 1, "#ffffff", 6, INPUT_B, op=0.045)
        tx = x + 12
        if dot:
            self.circle(tx + 4, y + h / 2, 4, dot)
            tx += 16
        self.text(tx, y + h / 2, value, 14, color)
        self.icon("chevron-down", x + w - 28, y + h / 2 - 8, 16, MFG, op=0.7)

    def input(self, x, y, w, value=None, placeholder=None, h=36, icon=None, removable=False, disabled=False, mono=False):
        self.rect(x + .5, y + .5, w - 1, h - 1, "#ffffff", 6, INPUT_B, op=0.045)
        tx = x + 12
        if icon:
            self.icon(icon, x + 10, y + h / 2 - 8, 16, MFG)
            tx = x + 32
        cid = self.clip(tx, y, w - (tx - x) - 28 if removable else w - (tx - x) - 8, h)
        if value is not None:
            self.text(tx, y + h / 2, value, 14, FG if not disabled else MFG, mono=mono, clip=cid)
        elif placeholder:
            self.text(tx, y + h / 2, placeholder, 14, MFG, clip=cid)
        if removable and value:
            self.icon("x", x + w - 26, y + h / 2 - 8, 16, MFG)

    def textarea(self, x, y, w, h, value=None, placeholder=None, lines=None):
        self.rect(x + .5, y + .5, w - 1, h - 1, "#ffffff", 6, INPUT_B, op=0.045)
        if lines:
            for i, ln in enumerate(lines):
                self.text(x + 12, y + 18 + i * 20, ln, 14, FG)
        elif value is not None:
            self.text(x + 12, y + 18, value, 14, FG)
        elif placeholder:
            self.text(x + 12, y + 18, placeholder, 14, MFG)

    def label(self, x, cy, s, optional=None, right=None):
        self.text(x, cy, s, 14, FG, 500)
        if optional and right:
            self.text(right, cy, optional, 14, MFG, anchor="end")

    def switch(self, x, y, on):
        w, h = 32, 18.4
        self.rect(x, y, w, h, BTN if on else "#ffffff", h / 2, op=None if on else 0.12)
        cx = x + w - 9.2 if on else x + 9.2
        self.circle(cx, y + h / 2, 8, "#171717" if on else FG)

    def checkbox(self, x, y, checked=False):
        if checked:
            self.rect(x, y, 16, 16, "#e5e5e5", 4)
            self.icon("check", x + 1.5, y + 1.5, 13, "#171717", 3)
        else:
            self.rect(x + .5, y + .5, 15, 15, "#ffffff", 4, INPUT_B, op=0.045)

    def badge(self, x, cy, label, kind="secondary"):
        w = tw(label, 13, 500) + 18
        h = 22
        y = cy - h / 2
        if kind == "default":
            self.rect(x, y, w, h, "#e5e5e5", 6); col = "#171717"
        elif kind == "secondary":
            self.rect(x, y, w, h, MUTEDBG, 6); col = FG
        elif kind == "pending":
            self.rect(x + .5, y + .5, w - 1, h - 1, BTN, 6, BTN, op=0.1); col = BTN
            self.parts.append(f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="6" fill="none" stroke="{BTN}" stroke-opacity="0.4"/>')
        elif kind == "approved":
            self.rect(x + .5, y + .5, w - 1, h - 1, "#059669", 6, "#059669", op=0.1); col = "#34d399"
        else:
            self.rect(x + .5, y + .5, w - 1, h - 1, MUTEDBG, 6, BORDER); col = MFG
        self.text(x + w / 2, cy, label, 13, col, 500, "middle")
        return w

    def tabs(self, x, y, labels, active, h=36):
        wi = max(tw(l, 14, 500) for l in labels) + 16
        total = wi * len(labels) + 6
        self.rect(x, y, total, h, MUTEDBG, 8)
        pos = []
        for i, l in enumerate(labels):
            tx = x + 3 + i * wi
            if i == active:
                self.rect(tx + .5, y + 3.5, wi - 1, h - 7, "#ffffff", 6, INPUT_B, op=0.045)
            self.text(tx + wi / 2, y + h / 2, l, 14, FG if i == active else MFG, 500, "middle")
            pos.append((tx, wi))
        return pos, total

    def table(self, x, y, w, colw, headers, row_hs, boxed=True, header_h=40, extra=0):
        """colw entries may be None (flex). headers entries: str | (str, 'info') | (str, 'info', 'right').
        Returns (col_x list, col_w list, row_y list, total_h)."""
        fixed = sum(c for c in colw if c)
        flex = [i for i, c in enumerate(colw) if c is None]
        cw = [c if c else (w - fixed) / len(flex) for c in colw]
        cx = [x]
        for c in cw[:-1]:
            cx.append(cx[-1] + c)
        total = header_h + sum(row_hs)
        if boxed:
            self.rect(x + .5, y + .5, w - 1, total + extra - 1, BG, 6, BORDER)
        yy = y + header_h
        for i, hd in enumerate(headers):
            if not hd:
                continue
            if isinstance(hd, str):
                s, info, al = hd, False, "left"
            else:
                s, info, al = hd[0], "info" in hd, ("right" if "right" in hd else "left")
            if al == "right":
                ex = cx[i] + cw[i] - 8
                self.text(ex, y + header_h / 2, s, 14, FG, 500, "end")
            else:
                self.text(cx[i] + 8, y + header_h / 2, s, 14, FG, 500)
                if info:
                    self.icon("info", cx[i] + 8 + tw(s, 14, 500) + 10, y + header_h / 2 - 7, 14, MFG)
        self.line(x + 1, yy, x + w - 1, yy)
        ry = []
        for i, rh in enumerate(row_hs):
            ry.append(yy)
            yy += rh
            if i < len(row_hs) - 1:
                self.line(x + 1, yy, x + w - 1, yy)
        return cx, cw, ry, total

    def avatar(self, x, y, initial, size=32):
        self.rect(x, y, size, size, "#3b0764", 6)
        self.text(x + size / 2, y + size / 2, initial, 14, "#d8b4fe", 500, "middle")

    def thumb(self, x, y, size, seed=0):
        """Abstract placeholder picture (stands in for an uploaded image)."""
        cols = [("#7c3aed", "#f472b6"), ("#0ea5e9", "#22c55e"), ("#f59e0b", "#ef4444")][seed % 3]
        self._id += 1
        g = f"g{self._id}"
        self.defs.append(f'<linearGradient id="{g}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{cols[0]}"/><stop offset="1" stop-color="{cols[1]}"/></linearGradient>')
        self.rect(x, y, size, size, f"url(#{g})", 6)
        self.circle(x + size * .7, y + size * .3, size * .1, "#ffffff")
        self.parts.append(f'<path d="M{x} {y+size*.85} L{x+size*.35} {y+size*.5} L{x+size*.6} {y+size*.75} L{x+size*.8} {y+size*.6} L{x+size} {y+size*.8} L{x+size} {y+size} L{x} {y+size} Z" fill="#ffffff" fill-opacity=".35"/>')

    # ---- overlays / annotations
    def dropdown(self, x, y, w, items, selected=0):
        h = len(items) * 32 + 8
        self.rect(x + .5, y + .5, w - 1, h - 1, CARD, 6, "#2b2b2b")
        for i, it in enumerate(items):
            iy = y + 4 + i * 32
            if i == 1:
                pass
            self.text(x + 12, iy + 16, it, 14, FG)
            if i == selected:
                self.icon("check", x + w - 26, iy + 8, 16, FG)
        return h

    def callout(self, x, y, n):
        self.circle(x, y, 13, ORANGE)
        self.text(x, y, str(n), 14, "#fff", 700, "middle")

    def ring(self, x, y, w, h, r=8):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>')

    def drawer_panel(self, x, y, w, h, title, footer=None):
        """Right drawer: bg-background, border-l, header p-4 with semibold title. Footer buttons pinned bottom."""
        self.rect(x, y, w, h, BG, 0)
        self.line(x + .5, y, x + .5, y + h)
        self.text(x + 16, y + 28, title, 16, FG, 600)

    def drawer_footer(self, x, y, w, h, cancel, primary, border=True):
        self.rect(x, y + h - 72, w, 72, BG, 0)
        if border:
            self.line(x, y + h - 72, x + w, y + h - 72)
        cw = self.btn(x + 20, y + h - 54, cancel, "outline")
        self.btn(x + 20 + cw + 12, y + h - 54, primary, "cta")

    def dim(self, x, y, w, h):
        self.rect(x, y, w, h, "#000000", 0, op=0.5)

    def save(self, path):
        self.parts[0] = f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="{self.bg}"/>'
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" font-family="{FONT}" overflow="hidden">'
               f'<defs>{"".join(self.defs)}</defs>' + "".join(self.parts) + "</svg>")
        open(path, "w").write(svg)
