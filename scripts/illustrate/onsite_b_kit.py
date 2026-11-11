"""Drawing kit for Group E onsite illustrations (dark theme tokens from packages/ui globals.css).

Colours are the real `.dark` tokens converted from oklch:
  background #0a0a0a, card/popover #171717, muted/secondary/accent #262626,
  muted-foreground #a1a1a1, foreground #fafafa, primary #e5e5e5,
  btn-primary (CTA) #c696ff with text-primary-foreground #171717,
  border = white 10%, input = white 15%.
"""
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(__file__))
from ui import Canvas, FONT, ORANGE  # noqa: E402,F401

try:
    from PIL import ImageFont
    _F = {400: ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100, index=0),
          700: ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100, index=1)}
except Exception:  # pragma: no cover
    _F = None


def tw(s, size=14, weight=400):
    """Approximate rendered width of s."""
    if _F is None:
        return len(s) * size * 0.56
    f = _F[700 if weight >= 600 else 400]
    return f.getlength(s) * size / 100 * 1.03


def blend(fg, bg, a):
    f = [int(fg[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(bg[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(f[i] * a + b[i] * (1 - a)) for i in range(3))


BG, CARD, MUTED = "#0a0a0a", "#171717", "#262626"
FG, MFG = "#fafafa", "#a1a1a1"
PRIMARY = "#e5e5e5"
CTA, CTA_FG = "#c696ff", "#171717"
BORDER = blend("#ffffff", BG, 0.10)
BORDER_C = blend("#ffffff", CARD, 0.10)
INPUT_B = blend("#ffffff", BG, 0.15)
INPUT_BC = blend("#ffffff", CARD, 0.15)
INPUT_BG = blend("#ffffff", BG, 0.15 * 0.30)
INPUT_BGC = blend("#ffffff", CARD, 0.15 * 0.30)
DESTR = "#ff6467"
EMERALD, AMBER, RED, VIOLET = "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"

TONES = {  # border, bg, text  (dark variants from pills.tsx)
    "neutral": (BORDER, MUTED, FG),
    "good": ("#065f46", "#022c22", "#d1fae5"),
    "warn": ("#92400e", "#451a03", "#fef3c7"),
    "bad": ("#991b1b", "#450a0a", "#fee2e2"),
    "info": ("#5b21b6", "#2e1065", "#ede9fe"),
}
CALLOUT = {  # dark:border-*-900 dark:bg-*-950/40 dark:text-*-100
    "bad": ("#7f1d1d", blend("#450a0a", BG, 0.4), "#fee2e2"),
    "warn": ("#78350f", blend("#451a03", BG, 0.4), "#fef3c7"),
    "info": ("#1e3a8a", blend("#172554", BG, 0.4), "#dbeafe"),
}

ICONS = {
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "circle-x": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/>',
    "circle-dot": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="1" fill="currentColor"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "copy": '<rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "pencil": '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>',
    "plus": '<path d="M5 12h14M12 5v14"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5M12 15V3"/>',
    "file-up": '<path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8l6 6v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5M12 12v6m3-3-3-3-3 3"/>',
    "arrow-up-from-line": '<path d="m18 9-6-6-6 6M12 3v14M5 21h14"/>',
    "alert-circle": '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "ban": '<circle cx="12" cy="12" r="10"/><path d="m4.9 4.9 14.2 14.2"/>',
    "minus-circle": '<circle cx="12" cy="12" r="10"/><path d="M8 12h8"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
}


def icon(c, x, y, name, size=16, color=FG, sw=2):
    """Lucide-style icon with its top-left at (x, y)."""
    s = size / 24
    c.parts.append(
        f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{color}" color="{color}" '
        f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def T(c, x, y, s, size=14, fill=FG, weight=400, anchor="start", extra=""):
    c.parts.append(
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def mono(c, x, y, s, size=14, fill=FG):
    T(c, x, y, s, size, fill, extra='font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"')


def R(c, x, y, w, h, fill="none", r=6, stroke=None, sw=1, dash=None):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    c.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st}{d}/>')


def line(c, x1, y1, x2, y2, color=BORDER_C, sw=1):
    c.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>')


def wrap(s, width, size=14, weight=400):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if tw(t, size, weight) <= width or not cur:
            cur = t
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def para(c, x, y, s, width, size=13, fill=MFG, weight=400, lh=None):
    """Wrapped paragraph; returns y after the last line."""
    lh = lh or round(size * 1.45)
    for ln in wrap(s, width, size, weight):
        T(c, x, y, ln, size, fill, weight)
        y += lh
    return y


def pill(c, x, y, label, tone="neutral", size=13, lock=False, h=22):
    """Pill with top-left at (x, y). Returns its width."""
    bd, bg, fg = TONES[tone]
    w = tw(label, size, 500) + 16 + (15 if lock else 0)
    R(c, x, y, w, h, bg, 6, bd)
    tx = x + 8
    if lock:
        icon(c, tx, y + (h - 12) / 2, "lock", 12, fg)
        tx += 15
    T(c, tx, y + h / 2 + size * 0.35, label, size, fg, 500)
    return w


def pill_w(label, size=13, lock=False):
    return tw(label, size, 500) + 16 + (15 if lock else 0)


def btn_w(label, ic=False, size=14, pad=16):
    return tw(label, size, 500) + pad * 2 + (20 if ic else 0) - (4 if ic else 0)


def button(c, x, y, label, kind="cta", h=36, w=None, ic=None, size=14, disabled=False, pad=16):
    """kind: cta | cta-outline | default | outline | ghost | destructive. Returns width."""
    w = w or btn_w(label, bool(ic), size, pad)
    iw = 20 if ic else 0
    c.parts.append('<g opacity="0.5">' if disabled else "<g>")
    if kind == "cta":
        R(c, x, y, w, h, CTA, 6); fg = CTA_FG
    elif kind == "cta-outline":
        R(c, x, y, w, h, INPUT_BG, 6, CTA); fg = CTA
    elif kind == "default":
        R(c, x, y, w, h, PRIMARY, 6); fg = "#262626"
    elif kind == "destructive":
        R(c, x, y, w, h, blend(DESTR, BG, 0.6), 6); fg = "#fff"
    elif kind == "ghost":
        fg = FG
    else:
        R(c, x, y, w, h, INPUT_BG, 6, INPUT_B); fg = FG
    cx = x + (w - tw(label, size, 500) - iw) / 2
    if ic:
        icon(c, cx, y + h / 2 - 8, ic, 16, fg)
        cx += 22
    T(c, cx, y + h / 2 + size * 0.36, label, size, fg, 500)
    c.parts.append("</g>")
    return w


def input_box(c, x, y, w, text="", placeholder="", h=36, size=14, on_card=False, icon_left=None, mono_font=False):
    R(c, x, y, w, h, INPUT_BGC if on_card else INPUT_BG, 6, INPUT_BC if on_card else INPUT_B)
    tx = x + 12
    if icon_left:
        icon(c, x + 12, y + h / 2 - 8, icon_left, 16, MFG)
        tx = x + 36
    if text:
        (mono if mono_font else T)(c, tx, y + h / 2 + size * 0.36, text, size, FG)
    elif placeholder:
        T(c, tx, y + h / 2 + size * 0.36, placeholder, size, MFG)


def select(c, x, y, w, text, placeholder=False, h=36, size=14, on_card=False, dot=None):
    R(c, x, y, w, h, INPUT_BGC if on_card else INPUT_BG, 6, INPUT_BC if on_card else INPUT_B)
    tx = x + 12
    if dot:
        c.parts.append(f'<circle cx="{x + 18}" cy="{y + h / 2}" r="4" fill="{dot}"/>')
        tx = x + 30
    T(c, tx, y + h / 2 + size * 0.36, text, size, MFG if placeholder else FG)
    c.parts.append('<g opacity="0.55">')
    icon(c, x + w - 26, y + h / 2 - 8, "chevron-down", 16, FG)
    c.parts.append("</g>")


def panel(c, x, y, w, h, title=None, hint=None, footer=None):
    """Panel (rounded-lg border bg-card). Returns y where content starts."""
    R(c, x, y, w, h, CARD, 8, BORDER_C)
    cy = y + 16
    if title is not None or hint is not None:
        T(c, x + 16, y + 29, title or "", 15, FG, 600)
        if hint:
            T(c, x + w - 16, y + 29, hint, 13, MFG, anchor="end")
        line(c, x, y + 46, x + w, y + 46)
        cy = y + 46 + 16
    if footer:
        line(c, x, y + h - 36, x + w, y + h - 36)
        T(c, x + 16, y + h - 13, footer, 13, MFG)
    return cy


def th_band(c, x, y, w, h=34):
    c.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{blend(MUTED, CARD, 0.4)}"/>')


def callout(c, x, y, w, tone, title, body, size=13):
    bd, bg, fg = CALLOUT[tone]
    lines = wrap(body, w - 32, size) if body else []
    h = 16 + 20 + (4 + len(lines) * 19 if lines else 0) + 14
    R(c, x, y, w, h, bg, 8, bd)
    T(c, x + 16, y + 28, title, 14, fg, 600)
    yy = y + 50
    for ln in lines:
        T(c, x + 16, yy, ln, size, fg)
        yy += 19
    return h


def stripe(c, x, y, h, tone):
    col = {"bad": RED, "warn": AMBER, "good": EMERALD, "info": VIOLET}[tone]
    c.parts.append(f'<rect x="{x}" y="{y}" width="4" height="{h}" fill="{col}"/>')


def row_bg(c, x, y, w, h, tone):
    col = {"bad": "#450a0a", "warn": "#451a03", "info": "#2e1065"}.get(tone)
    if col:
        c.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{blend(col, CARD, 0.2)}"/>')


def tabs(c, x, y, labels, active, h=36, w=None):
    """Tabs list (bg-muted rounded-lg p-[3px]). Returns width."""
    ws = [tw(l, 14, 500) + 22 for l in labels]
    total = sum(ws) + 6 if w is None else w
    R(c, x, y, total, h, MUTED, 8)
    cx = x + 3
    if w is not None:
        ws = [(w - 6) / len(labels)] * len(labels)
    for i, (l, wi) in enumerate(zip(labels, ws)):
        if i == active:
            R(c, cx, y + 3, wi, h - 6, blend("#ffffff", BG, 0.045), 6, INPUT_B)
        T(c, cx + wi / 2, y + h / 2 + 5, l, 14, FG if i == active else MFG, 500, "middle")
        cx += wi
    return total


def checkbox(c, x, y, checked=False, size=16):
    R(c, x, y, size, size, INPUT_BG, 4, INPUT_B)
    if checked:
        icon(c, x + 2, y + 2, "check", size - 4, FG, 3)


def stat_card(c, x, y, w, h, label, value, foot, tone=None, vsize=26):
    R(c, x, y, w, h, CARD, 8, BORDER_C)
    T(c, x + 16, y + 26, label, 13, MFG, 500)
    col = {"good": "#6ee7b7", "warn": "#fcd34d", "bad": "#fca5a5"}.get(tone, FG)
    T(c, x + 16, y + 58, value, vsize, col, 700)
    if foot:
        yy = y + 80
        for ln in wrap(foot, w - 32, 13):
            T(c, x + 16, yy, ln, 13, MFG)
            yy += 17


def recommended_box(c, x, y, w, h):
    """border-2 border-btn-primary bg-btn-primary/5."""
    R(c, x, y, w, h, blend(CTA, CARD, 0.05), 8, CTA, 2)


def ring(c, x, y, w, h, r=8):
    c.ring(x, y, w, h, r)


def num(c, x, y, n):
    c.callout(x, y, n)


def new(w, h):
    return Canvas(w, h, bg=BG)
