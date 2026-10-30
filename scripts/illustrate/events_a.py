import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from ui import Canvas, ORANGE, FONT
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "events")


def oklch(L, C, h):
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = [4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
           -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
           -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_]
    out = ""
    for v in rgb:
        v = max(0, min(1, v))
        v = 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
        out += "%02x" % round(v * 255)
    return "#" + out

# dark theme tokens (packages/ui globals.css .dark)
BG = oklch(.145, 0, 0)
CARD = oklch(.205, 0, 0)
MUTED = oklch(.269, 0, 0)
MFG = oklch(.708, 0, 0)
FG = oklch(.985, 0, 0)
BORDER = "#242424"      # white @10% over background
INPUT = "#2f2f2f"       # white @15%
BTN = oklch(.8223, .2836, 289)   # btn-primary (dark)
BTN_FG = "#2a1050"
GREEN = "#22c55e"
RED = "#ef4444"


def P(c, s):
    c.parts.append(s)

def T(c, x, y, s, size=14, fill=FG, w=400, a="start"):
    c.text(x, y, s, size, fill, w, a)

def R(c, x, y, w, h, fill, r=8, stroke=None, sw=1, dash=None, op=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    if dash: s += f' stroke-dasharray="{dash}"'
    if op: s += f' opacity="{op}"'
    P(c, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}/>')

def line(c, x1, y1, x2, y2, col=BORDER, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    P(c, f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}"{d}/>')

def path(c, d, col=FG, sw=1.8, fill="none", op=1):
    P(c, f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')

def circ(c, x, y, r, fill="none", stroke=None, sw=1.5):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    P(c, f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{s}/>')

# ---- icons (centered on x,y; ~16px) ----
def ic_pencil(c, x, y, col=FG):
    path(c, f"M{x-5},{y+6} l1,-4 l7,-7 l3,3 l-7,7 z M{x+1},{y-4} l3,3", col, 1.4)
def ic_x(c, x, y, col=FG, s=4.5, sw=1.8):
    path(c, f"M{x-s},{y-s} L{x+s},{y+s} M{x+s},{y-s} L{x-s},{y+s}", col, sw)
def ic_check(c, x, y, col=FG):
    path(c, f"M{x-6},{y} l4,4 l8,-8", col, 1.8)
def ic_plus(c, x, y, col=FG, s=5):
    path(c, f"M{x-s},{y} H{x+s} M{x},{y-s} V{y+s}", col, 1.8)
def ic_chev(c, x, y, col=MFG):
    path(c, f"M{x-4},{y-2} l4,4 l4,-4", col, 1.6)
def ic_info(c, x, y, col=MFG):
    circ(c, x, y, 8, stroke=col, sw=1.4); path(c, f"M{x},{y} V{y+4}", col, 1.5); circ(c, x, y-4, .9, col)
def ic_globe(c, x, y, col=FG, r=8):
    circ(c, x, y, r, stroke=col, sw=1.4)
    P(c, f'<ellipse cx="{x}" cy="{y}" rx="{r*.42}" ry="{r}" fill="none" stroke="{col}" stroke-width="1.3"/>')
    path(c, f"M{x-r},{y} H{x+r}", col, 1.3)
def ic_monitor(c, x, y, col=FG):
    R(c, x-8, y-6, 16, 10, "none", 2, col, 1.5); path(c, f"M{x-3},{y+8} H{x+3} M{x},{y+4} V{y+8}", col, 1.5)
def ic_phone(c, x, y, col=MFG):
    R(c, x-5, y-8, 10, 16, "none", 2.5, col, 1.5); path(c, f"M{x-1},{y+5} h2", col, 1.5)
def ic_shield(c, x, y, col=FG):
    path(c, f"M{x},{y-8} l7,2.5 v5 c0,4 -3,6.5 -7,8.5 c-4,-2 -7,-4.5 -7,-8.5 v-5 z M{x-3},{y} l2.5,2.5 l4,-4.5", col, 1.4)
def ic_mega(c, x, y, col=FG):
    path(c, f"M{x-8},{y-3} h5 l8,-5 v16 l-8,-5 h-5 z M{x-5},{y+3} l1.5,6 h3 l-1,-6", col, 1.4)
def ic_lock(c, x, y, col=MFG):
    R(c, x-6, y-2, 12, 9, "none", 2, col, 1.4); path(c, f"M{x-3.5},{y-2} v-3 a3.5,3.5 0 0 1 7,0 v3", col, 1.4)
def ic_bold(c, x, y, col=FG):
    path(c, f"M{x-4},{y-6} h5 a3,3 0 0 1 0,6 h-5 M{x-4},{y} h6 a3,3 0 0 1 0,6 h-6 z", col, 1.8)
def ic_link(c, x, y, col=FG):
    path(c, f"M{x-1},{y-4} h-3 a4,4 0 0 0 0,8 h3 M{x+1},{y-4} h3 a4,4 0 0 1 0,8 h-3 M{x-3},{y} h6", col, 1.6)
def ic_grip(c, x, y, col=MFG):
    for dx in (-3, 3):
        for dy in (-6, 0, 6):
            circ(c, x+dx, y+dy, 1.4, col)

# ---- components ----
def pill(c, x, y, label, w, h=28, fill=MUTED, fg=FG, size=13, weight=400, stroke=None):
    R(c, x, y, w, h, fill, h/2, stroke)
    T(c, x+w/2, y+h/2+4.5, label, size, fg, weight, "middle")

def edit_btn(c, x, y):   # "Edit" pill with pencil
    R(c, x, y, 76, 32, MUTED, 16, INPUT)
    ic_pencil(c, x+20, y+16, FG); T(c, x+34, y+21, "Edit", 13, FG)

def toggle(c, x, y, on, dim=False):
    op = ' opacity=".55"' if dim else ""
    P(c, f'<g{op}>')
    R(c, x, y, 40, 22, BTN if on else MUTED, 11)
    circ(c, x+29 if on else x+11, y+11, 8, BG if on else FG)
    P(c, '</g>')

def btn(c, x, y, w, label, h=36, fill=BTN, fg=BTN_FG, dim=False, stroke=None, wt=500):
    R(c, x, y, w, h, fill, 8, stroke, op=.5 if dim else None)
    T(c, x+w/2, y+h/2+5, label, 14, fg, wt, "middle")

def status(c, x, y, w=110, dim=False):
    op = ' opacity=".5"' if dim else ""
    P(c, f'<g{op}>')
    R(c, x, y, w, 40, BG, 8, INPUT)
    circ(c, x+16, y+20, 4, GREEN); T(c, x+28, y+25, "Active", 14, FG)
    ic_chev(c, x+w-18, y+20); P(c, '</g>')

def textbox(c, x, y, w, h, lines, ph=False, focus=False):
    R(c, x, y, w, h, BG, 10, FG if focus else INPUT, 2 if focus else 1)

def label_req(c, x, y, s, size=14):
    T(c, x, y, s, size, FG, 500)


# =================== 1. editor full page ===================
def editor_full():
    W, H = 900, 520
    c = Canvas(W, H, BG)
    # top bar
    line(c, 0, 52, W, 52)
    T(c, 24, 32, "Event info", 14, FG, 500); R(c, 24, 50, 66, 2, FG, 0)
    T(c, 118, 32, "Checkout", 14, MFG, 500)
    T(c, 640, 32, "Preview layout", 13, MFG, 400, "end")
    R(c, 652, 10, 78, 34, CARD, 8, BORDER)
    R(c, 656, 14, 34, 26, MUTED, 6); ic_monitor(c, 673, 27, FG); ic_phone(c, 711, 27, MFG)
    R(c, 752, 9, 124, 36, BTN, 8, op=.55)
    T(c, 814, 32, "Save Event", 14, BTN_FG, 500, "middle")
    # main image (square) + gallery
    R(c, 100, 82, 232, 232, CARD, 14, BORDER)
    R(c, 112, 94, 208, 208, "#2a1560", 8)
    P(c, '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a1590"/><stop offset=".55" stop-color="#8a2be2"/><stop offset="1" stop-color="#ff4fa3"/></linearGradient></defs>')
    R(c, 112, 94, 208, 208, "url(#g)", 8)
    circ(c, 216, 168, 34, "#fff", op=None) if False else None
    R(c, 132, 190, 80, 80, "#ff4fa3", 6, op=.85); R(c, 190, 130, 110, 60, "#22d3ee", 6, op=.8); circ(c, 250, 250, 36, "#fde047")
    T(c, 100, 340, "Gallery", 14, MFG, 400); T(c, 332, 340, "1/15", 13, MFG, 400, "end")
    R(c, 100, 352, 66, 66, "#6a2bc9", 8)
    circ(c, 154, 364, 9, "#ef4444cc"); ic_x(c, 154, 364, "#fff", 3.5, 1.6)
    R(c, 178, 352, 66, 66, "none", 8, INPUT, 1.5, "5 4")
    ic_plus(c, 211, 376, MFG, 6); T(c, 211, 404, "Add", 13, MFG, 400, "middle")
    # right column
    T(c, 368, 120, "Neon Nights", 36, FG, 700)
    edit_btn(c, 800, 88)
    T(c, 368, 160, "Fri, Nov 6, 9:00 PM", 17, "#a78bfa", 500)
    T(c, 368, 192, "Demo Hall, Bangkok, Thailand", 15, FG)
    edit_btn(c, 800, 218)
    R(c, 368, 262, 508, 74, CARD, 14)
    T(c, 392, 306, "From", 15, MFG); T(c, 436, 308, "$45.00", 24, FG, 600)
    R(c, 744, 276, 116, 46, "#721BFD", 23); T(c, 802, 305, "Buy now", 15, "#fff", 600, "middle")
    line(c, 368, 358, 876, 358)
    ic_info(c, 376, 384); T(c, 396, 389, "This is an 18+ event.", 14, FG)
    ic_info(c, 376, 414); T(c, 396, 419, "Photo ID required for entry.", 14, FG)
    line(c, 368, 442, 876, 442)
    T(c, 368, 480, "About", 20, FG, 600); T(c, 428, 477, "*", 20, RED, 600)
    edit_btn(c, 800, 460)
    T(c, 368, 508, "Neon Nights returns for one night only.", 14, FG)
    # callouts + rings
    c.ring(94, 76, 244, 244, 12); c.callout(88, 78, 1)
    c.ring(92, 330, 258, 98, 10); c.callout(86, 336, 2)
    c.ring(362, 88, 270, 46, 8); c.callout(358, 90, 3)
    c.ring(362, 142, 220, 28, 8); c.callout(358, 150, 4)
    c.ring(796, 214, 84, 40, 20); c.callout(790, 214, 5)
    c.save(f"{OUT}/editor-full-page.svg")


# =================== 2. time picker ===================
def time_picker():
    W, H = 760, 220
    c = Canvas(W, H, BG)
    T(c, 24, 38, "Time", 20, FG, 600); T(c, 70, 36, "*", 20, RED, 600)
    ic_check(c, 696, 30); ic_x(c, 730, 30, FG, 5, 1.6)
    R(c, 24, 58, 566, 140, MUTED, 14)
    circ(c, 48, 98, 5, MFG); circ(c, 48, 158, 5, "none", MFG, 1.5); line(c, 48, 105, 48, 151, MFG, 1.3, "2 3")
    T(c, 72, 104, "Start time", 17, FG); T(c, 72, 164, "End time", 17, FG)
    for y, d, t in ((78, "Fri, Nov 6", "9:00 PM"), (138, "Sat, Nov 7", "2:00 AM")):
        R(c, 340, y, 232, 44, CARD, 8, None)
        line(c, 462, y, 462, y+44, BG, 2)
        T(c, 401, y+27, d, 14, FG, 400, "middle"); T(c, 517, y+27, t, 14, FG, 400, "middle")
    R(c, 604, 58, 134, 140, MUTED, 14)
    ic_globe(c, 628, 92, FG, 9)
    T(c, 622, 150, "GMT+07:00", 15, FG, 700); T(c, 622, 174, "Bangkok", 14, MFG)
    c.save(f"{OUT}/editor-time-picker.svg")


# =================== 3. price label / button text ===================
def price_btn():
    W, H = 760, 330
    c = Canvas(W, H, BG)
    for cx in (690, 730):
        circ(c, cx, 28, 17, BG, INPUT, 1.5)
    ic_check(c, 690, 28); ic_x(c, 730, 28, FG, 5, 1.6)
    R(c, 20, 56, 720, 258, CARD, 14)
    # left input
    R(c, 40, 76, 380, 62, BG, 12, INPUT)
    T(c, 58, 116, "From", 20, FG, 600)
    R(c, 114, 92, 130, 30, MUTED, 8); T(c, 126, 112, "Lowest price", 13, FG, 600); ic_x(c, 230, 107, MFG, 3.5, 1.5)
    ic_x(c, 396, 107, MFG, 5, 1.6)
    T(c, 420, 158, "21/28", 13, MFG, 400, "end")
    for i, s in enumerate(["Shown instead of the ticket price. Leave blank to keep",
                           "the default. Use the button below to include the",
                           "current lowest price."]):
        T(c, 40, 184 + i * 20, s, 13, MFG)
    R(c, 40, 254, 184, 38, CARD, 8, INPUT); T(c, 132, 278, "Insert lowest price", 14, MFG, 400, "middle")
    # right button
    R(c, 460, 76, 262, 62, BTN, 31, "#7c3aed", 1.5)
    T(c, 560, 113, "Join", 17, BTN_FG, 700, "middle")
    ic_x(c, 700, 107, BTN_FG, 5, 1.6)
    T(c, 722, 158, "4/8", 13, MFG, 400, "end")
    for i, s in enumerate(["The purchase button's wording.", "Leave blank to keep the default", "“Buy now”."]):
        T(c, 464, 184 + i * 20, s, 13, MFG)
    c.save(f"{OUT}/editor-price-label-button-text.svg")


# =================== 4. checkout consent ===================
def consent():
    W, H = 640, 640
    c = Canvas(W, H, BG)
    T(c, 24, 36, "Checkout consent", 18, FG, 600)
    T(c, 24, 62, "The checkboxes buyers tick when they buy a ticket or RSVP. Each one saves on its own.", 13, MFG)
    # required
    ic_shield(c, 32, 98, FG); T(c, 50, 104, "Required Consent", 15, FG, 500); ic_info(c, 198, 98)
    pill(c, 366, 85, "Always shown · can't be turned off", 250, 26, MUTED, FG, 13, 500)
    R(c, 24, 122, 592, 196, BG, 10, BORDER)
    ic_bold(c, 52, 148); ic_link(c, 92, 148)
    line(c, 24, 174, 616, 174); line(c, 24, 208, 616, 208)
    ic_lock(c, 42, 191); T(c, 58, 196, "By proceeding, you accept our", 14, MFG)
    T(c, 264, 196, "Terms of Use", 14, FG, 600); line(c, 264, 200, 352, 200, FG)
    T(c, 358, 196, "and", 14, MFG)
    T(c, 390, 196, "Privacy Policy", 14, FG, 600); line(c, 390, 200, 486, 200, FG)
    T(c, 488, 196, ".", 14, MFG)
    T(c, 600, 196, "Locked", 13, MFG, 400, "end")
    T(c, 40, 238, "Add your own terms after the platform sentence, e.g. My RSVP details", 14, MFG)
    T(c, 40, 260, "will be shared with **Neon Nights** to run this event.", 14, MFG)
    for x, w, s in ((24, 100, "House rules"), (134, 126, "Age restriction"), (270, 106, "Photography")):
        R(c, x, 330, w, 34, BG, 8, INPUT); T(c, x+w/2, 352, s, 13, FG, 500, "middle")
    T(c, 616, 352, "0/500 bytes", 13, MFG, 400, "end")
    T(c, 24, 400, "Wording last changed Sep 23, 2026, 08:16", 13, MFG)
    btn(c, 552, 382, 64, "Save", 34, BTN, BTN_FG, dim=True)
    # marketing
    ic_mega(c, 32, 452, FG); T(c, 50, 458, "Marketing Consent", 15, FG, 500); ic_info(c, 216, 452)
    pill(c, 340, 439, "Optional · starts unticked", 206, 26, MUTED, FG, 13, 500)
    toggle(c, 576, 441, True)
    R(c, 24, 478, 592, 112, BG, 10, FG, 2)
    ic_bold(c, 52, 504); ic_link(c, 92, 504)
    line(c, 25, 530, 615, 530)
    T(c, 40, 562, "Get news and updates from **Neon Nights** by email. Unsubscribe anytime.", 14, FG)
    T(c, 616, 614, "73/500 bytes", 13, MFG, 400, "end")
    T(c, 24, 655, "Not saved yet", 13, MFG)
    c.h = 676
    btn(c, 552, 626, 64, "Save", 34, BTN, BTN_FG)
    c.w, c.h = W, 676
    c.parts[0] = f'<rect x="0" y="0" width="{W}" height="676" rx="0" fill="{BG}"/>'
    c.save(f"{OUT}/editor-checkout-consent.svg")


# =================== 5. registration form ===================
def q_row(c, y, name, req, dim=False, stat=True):
    ic_grip(c, 40, y+23)
    T(c, 88, y+28, name, 15, FG, 500)
    toggle(c, 360, y+12, req, dim)
    status(c, 560, y+4, 112, dim)
    line(c, 24, y+46, 736, y+46)

def regform():
    W, H = 760, 560
    c = Canvas(W, H, BG)
    T(c, 24, 34, "Booking questions", 18, FG, 600)
    T(c, 24, 58, "The questions buyers answer at checkout. Changes save as you make them.", 13, MFG)
    T(c, 24, 100, "Quick add", 14, MFG)
    x = 104
    for lab, w, ic in (("Gender", 100, "g"), ("Nationality", 126, "n"), ("Date of Birth", 140, "b"), ("Identity Document", 172, "i")):
        R(c, x, 80, w, 36, BG, 8, INPUT)
        ix = x + 20
        if ic == "n": ic_globe(c, ix, 98, FG, 7)
        elif ic == "g": circ(c, ix-1, 100, 4.5, stroke=FG, sw=1.4); path(c, f"M{ix+2},{97} l5,-5 M{ix+3},{92} h4 v4 M{ix-1},{105} v5 M{ix-3},{108} h4", FG, 1.3)
        elif ic == "b": R(c, ix-7, 99, 14, 7, "none", 1, FG, 1.3); path(c, f"M{ix},{92} v6", FG, 1.3)
        else: R(c, ix-8, 92, 16, 12, "none", 2, FG, 1.3); path(c, f"M{ix-4},{97} h3 M{ix-4},{100} h5", FG, 1.2)
        T(c, x+36, 103, lab, 13, FG, 500)
        x += w + 12
    c.ring(14, 72, 722, 52, 10); c.callout(14, 74, 1)
    T(c, 24, 160, "Preset Questions", 14, FG, 600)
    for hx, s in ((88, "Question"), (360, "Required"), (560, "Status")):
        T(c, hx, 192, s, 13, FG, 500)
    line(c, 24, 204, 736, 204)
    q_row(c, 204, "Full Name", True, True)
    q_row(c, 250, "Email Address", True, True)
    q_row(c, 296, "Phone Number", True)
    T(c, 24, 388, "Custom Questions", 14, FG, 600)
    R(c, 548, 366, 188, 40, BTN, 8); ic_plus(c, 580, 386, BTN_FG, 5)
    T(c, 598, 391, "Custom question", 14, BTN_FG, 500)
    for hx, s in ((88, "Question"), (360, "Required"), (560, "Status")):
        T(c, hx, 436, s, 13, FG, 500)
    line(c, 24, 448, 736, 448)
    q_row(c, 448, "Dietary requirements", False)
    q_row(c, 494, "Arrival day", False)
    c.ring(26, 304, 28, 38, 8); c.callout(24, 304, 5)
    c.ring(354, 304, 52, 36, 18); c.callout(354, 304, 3)
    c.ring(554, 304, 124, 48, 10); c.callout(554, 304, 4)
    c.ring(544, 362, 196, 48, 10); c.callout(544, 362, 2)
    c.save(f"{OUT}/regform-page.svg")


# =================== 6. create custom question panel ===================
def panel():
    W, H = 460, 600
    c = Canvas(W, H, BG)
    T(c, 24, 36, "Create Custom Question", 18, FG, 600)
    T(c, 24, 70, "Question*", 14, FG, 500)
    R(c, 24, 80, 412, 40, BG, 8, INPUT); T(c, 38, 105, "Which day will you arrive?", 14, FG)
    T(c, 24, 148, "Description", 14, FG, 500)
    R(c, 24, 158, 412, 58, BG, 8, INPUT); T(c, 38, 182, "Enter description", 14, MFG)
    T(c, 24, 244, "Answer Type*", 14, FG, 500)
    R(c, 24, 254, 412, 40, BG, 8, INPUT); T(c, 38, 279, "Multiple choice", 14, FG); ic_chev(c, 412, 274)
    T(c, 24, 322, "Options*", 14, FG, 500)
    for i, s in enumerate(("Friday", "Saturday", "Sunday")):
        y = 332 + i * 44
        R(c, 24, y, 340, 38, BG, 8, INPUT); T(c, 38, y+24, s, 14, FG); ic_x(c, 392, y+19, FG, 5, 1.6)
    R(c, 24, 464, 412, 38, BG, 8, INPUT); ic_plus(c, 198, 483, FG, 5); T(c, 214, 488, "Add Option", 14, FG, 500)
    T(c, 24, 530, "Required", 14, FG, 500); toggle(c, 98, 518, True)
    btn(c, 24, 552, 80, "Cancel", 36, BG, FG, stroke=INPUT)
    btn(c, 114, 552, 68, "Save", 36, BTN, BTN_FG)
    c.w, c.h = W, 600
    c.save(f"{OUT}/regform-create-custom-question-panel.svg")


for f in (editor_full, time_picker, price_btn, consent, regform, panel):
    f()
