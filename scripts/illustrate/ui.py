"""Tiny SVG kit for drawing Business Portal UI (dark theme, vector so always crisp)."""
from xml.sax.saxutils import escape

BG, CARD, BORDER = "#0a0a0a", "#171717", "#2a2a2a"
FG, MUTED = "#fafafa", "#a3a3a3"
PRIMARY, ORANGE = "#721BFD", "#FF7A1A"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


class Canvas:
    def __init__(self, w, h, bg=BG):
        self.w, self.h, self.parts = w, h, []
        self.rect(0, 0, w, h, bg, r=0)

    def rect(self, x, y, w, h, fill=CARD, r=10, stroke=None):
        s = f' stroke="{stroke}"' if stroke else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}/>')

    def text(self, x, y, s, size=14, fill=FG, weight=400, anchor="start"):
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}">{escape(s)}</text>')

    def card(self, x, y, w, h):
        self.rect(x, y, w, h, CARD, 12, BORDER)

    def input(self, x, y, w, placeholder, value=None, h=40):
        self.rect(x, y, w, h, BG, 8, BORDER)
        self.text(x + 12, y + h / 2 + 5, value or placeholder, 14, FG if value else MUTED)

    def button(self, x, y, w, label, h=40, fill=PRIMARY, fg="#fff", stroke=None):
        self.rect(x, y, w, h, fill, 8, stroke)
        self.text(x + w / 2, y + h / 2 + 5, label, 14, fg, 600, "middle")

    def callout(self, x, y, n):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="12" fill="{ORANGE}"/>')
        self.text(x, y + 5, str(n), 14, "#fff", 700, "middle")

    def ring(self, x, y, w, h, r=10):
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>')

    def save(self, path):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'font-family="{FONT}">' + "".join(self.parts) + "</svg>")
        open(path, "w").write(svg)
