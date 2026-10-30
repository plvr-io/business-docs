"""Illustrations for tickets/*.mdx and other/payment-links.mdx (GROUP A).

Every label is the en.json string from apps/business-portal/messages/en.json.
All data is made up (events Neon Nights / Harbor Lights Festival, Alex Chen ...).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from tickets_kit import *

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "images")
TK = os.path.join(ROOT, "tickets")
OT = os.path.join(ROOT, "other")
os.makedirs(TK, exist_ok=True)
os.makedirs(OT, exist_ok=True)

AMBER6 = "#d97706"  # text-amber-600 (tier warning tone)
DOT = {"Active": GREEN5, "Inactive": GRAY5, "Ended": GRAY5, "Sold out": NEUT4}


# ---------------------------------------------------------------- ticket table
def ticket_table(c, x, y, w, rows, cols=None, name_header="Ticket Type", currency="USD", grip=True, fit=False):
    """Ticket Management table. Returns (height, geometry dict)."""
    cols = cols or dict(total=48, name=108, price=270, sold=370, avail=440, status=540)
    c.surface(x, y, w, 10)  # placeholder, replaced below
    c.parts.pop()
    hh = 40
    heights = []
    for r in rows:
        left = 20 + (22 if r.get("chips") else 0)
        right = 36 + (20 if r.get("hint") else 0)
        heights.append(16 + max(left, right))
    total = hh + sum(heights)
    c.surface(x, y, w, total)
    gx = x
    c.line(x, y + hh, x + w, y + hh)
    for key, label in [("total", "Total"), ("name", name_header), ("price", f"Price ({currency})"),
                       ("sold", "Sold"), ("avail", "Available"), ("status", "Status")]:
        c.th(x + cols[key], y + 25, label)
    yy = y + hh
    geo = {"rows": []}
    for r, rh in zip(rows, heights):
        cy = yy + rh / 2
        if grip:
            c.icon("grip", x + 12, cy - 8, 16, MFG)
        c.t(x + cols["total"], cy + 5, str(r["total"]))
        ny = yy + 8 + 15 if r.get("chips") else cy + 5
        c.t(x + cols["name"], ny, r["name"])
        cx = x + cols["name"]
        for ch in r.get("chips", []):
            cx += c.chip(cx, yy + 8 + 22, ch) + 6
        c.t(x + cols["price"], cy + 5, r["price"])
        c.t(x + cols["sold"], cy + 5, str(r["sold"]))
        c.t(x + cols["avail"], cy + 5, str(r["avail"]))
        sy = yy + 8
        sw = int(12 + 16 + est(r["status"]) + 8 + 16 + 14) if fit else 180
        c.select(x + cols["status"], sy, sw, r["status"], dot=DOT[r["status"]], disabled=r["status"] == "Ended")
        if r.get("hint"):
            txt, col = r["hint"]
            c.t(x + cols["status"], sy + 36 + 15, txt, 13, col)
        c.icon("pencil", x + w - 32, cy - 8, 16, FG)
        geo["rows"].append(dict(y=yy, h=rh, sel=(x + cols["status"], sy, sw, 36), pencil=(x + w - 32, cy - 8, 16, 16)))
        c.line(x, yy + rh, x + w, yy + rh) if r is not rows[-1] else None
        yy += rh
    geo["h"] = total
    geo["hh"] = hh
    geo["cols"] = cols
    return total, geo


# ---------------------------------------------------------------- release chains
def tier_row(c, x, y, w, tier, thr=98):
    """One tier li: grip, '1. Name', status, progress, state line, remove X. Height 52."""
    h = 52
    c.box(x, y, w, h, BG, "#fff", 8, BORDER_OP)
    c.icon("grip", x + 8, y + 9, 16, MFG)
    px = x + 32
    base = y + 6 + 15
    nm = f'{tier["pos"]}. {tier["name"]}'
    c.t(px, base, nm)
    px += est(nm) + 12
    c.dot(px + 4, base - 5, 4, GREEN5 if tier["status"] == "Active" else NEUT4)
    c.t(px + 14, base, tier["status"])
    px += 14 + est(tier["status"]) + 12
    c.progress(px, base - 8, tier["pct"], tier["status"] == "Active", tick=thr)
    c.t(px + 112 + 8, base, f'{tier["pct"]}% sold', 14, MFG)
    col = {"neutral": MFG, "warning": AMBER6, "muted": MFG}[tier.get("tone", "neutral")]
    c.t(x + 32, y + 6 + 20 + 2 + 12, tier["line"], 13, col, op=0.7 if tier.get("tone") == "muted" else None)
    c.icon("x", x + w - 26, y + 9, 16, MFG)
    return h


def chain_panel(c, x, y, w, tiers, summary, open_=True, threshold=98, copy_to=True, add_select=True,
                badge=3, name="GA", enabled=True, new_chain=True):
    """Release Chains panel. Returns (height, geometry)."""
    geo = {}
    hdr = 48
    # content heights
    card_h = 12 + 32 + 8 + len(tiers) * 52 + (len(tiers) - 1) * 6 + 8 + (36 if add_select else 20) + 12
    total = hdr + ((1 + 8 + 20 + 8 + card_h + 12) if open_ else 0) + 0
    c.surface(x, y, w, total)
    c.icon("chevron-down" if open_ else "chevron-right", x + 12, y + 16, 16, MFG)
    c.t(x + 36, y + 29, "Release Chains", 14, FG, 500)
    c.t(x + 36 + est("Release Chains", 14, True) + 8, y + 29, summary, 14, MFG)
    # right buttons
    bx = x + w - 12
    nw = 112
    if new_chain:
        c.button(bx - nw, y + 8, nw, "New chain", "outline", icon="plus", h=32)
        geo["new"] = (bx - nw, y + 8, nw, 32)
        bx -= nw + 4
    c.icon("history", bx - 32 + 8, y + 16, 16, FG)
    geo["log"] = (bx - 32, y + 8, 32, 32)
    if badge:
        c.dot(bx - 2, y + 11, 8, "#e5e5e5")
        c.t(bx - 2, y + 15, str(badge), 11, BTN_FG, 600, "middle")
    if open_:
        c.line(x, y + hdr, x + w, y + hdr)
        yy = y + hdr + 1 + 8
        c.t(x + 12, yy + 15, f"The next tier opens when {threshold}% of the current tier is sold.", 14, MFG)
        yy += 20 + 8
        cx, cw = x + 12, w - 24
        c.box(cx, yy, cw, card_h, BG, "#fff", 8, BORDER_OP)
        c.t(cx + 12, yy + 12 + 21, name, 14, FG, 500)
        # right controls
        rx = cx + cw - 12
        c.icon("trash", rx - 24 + 4, yy + 12 + 8, 16, FG)
        geo["trash"] = (rx - 32, yy + 12, 32, 32)
        rx -= 36
        if copy_to:
            cw2 = 118
            c.button(rx - cw2, yy + 12, cw2, "Copy to…", "ghost", icon="copy", h=32)
            geo["copy"] = (rx - cw2, yy + 12, cw2, 32)
            rx -= cw2 + 12
        c.switch(rx - 32, yy + 12 + 7, enabled, GREEN6)
        geo["switch"] = (rx - 32, yy + 12 + 7, 32, 18)
        c.t(rx - 32 - 6, yy + 12 + 21, "Auto-release", 14, FG, anchor="end")
        geo["switch_label"] = (rx - 32 - 6 - est("Auto-release"), yy + 12 + 5, est("Auto-release") + 6 + 32 + 6, 22)
        ty = yy + 12 + 32 + 8
        geo["tiers"] = []
        for t in tiers:
            tier_row(c, cx + 12, ty, cw - 24, t, threshold)
            geo["tiers"].append((cx + 12, ty, cw - 24, 52))
            ty += 52 + 6
        ty += 2
        if add_select:
            c.select(cx + 12, ty, 384, placeholder="+ Add existing ticket")
        else:
            c.t(cx + 12, ty + 15, "No more tickets available to add.", 14, MFG)
        geo["card"] = (cx, yy, cw, card_h)
    geo["h"] = total
    return total, geo


TIERS3 = [
    dict(pos=1, name="Early Bird", status="Active", pct=40, line="On sale"),
    dict(pos=2, name="General Admission", status="Inactive", pct=0,
         line="Activates automatically when 'Early Bird' sells out"),
    dict(pos=3, name="Final Release", status="Inactive", pct=0,
         line="Activates automatically when 'General Admission' sells out"),
]


# ================================================================ concepts
def concepts_ticket_table():
    W = 800
    c = K(W, 270)
    rows = [
        dict(total=300, name="General Admission", price="30.00", sold=120, avail=180, status="Active"),
        dict(total=50, name="VIP", price="80.00", sold=0, avail=50, status="Inactive"),
        dict(total=100, name="Early Bird", price="20.00", sold=100, avail=0, status="Ended"),
    ]
    h, g = ticket_table(c, 20, 44, 760, rows)
    c.canvas_h = 44 + h + 24
    r0 = g["rows"][0]["sel"]
    c.ring(r0[0] - 4, r0[1] - 4, r0[2] + 8, r0[3] + 8, 10)
    c.callout(r0[0] - 4, r0[1] - 8, 1)
    cols = g["cols"]
    rx = 20 + cols["total"] - 10
    c.ring(rx, 44 + 4, cols["avail"] + 90 - cols["total"], h - 8, 10)
    c.callout(rx, 44 - 2, 2)
    c.h = 44 + h + 24
    finish(c, f"{TK}/concepts-ticket-table.svg")


def finish(c, path):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {c.w} {c.h}" font-family="{FONT_STACK}">'
           + "".join(c.parts) + "</svg>")
    # background rect was drawn with the initial height; fix it
    svg = svg.replace(f'height="{c.initial_h}"', f'height="{c.h}"', 1)
    open(path, "w").write(svg)


FONT_STACK = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
_orig_init = K.__init__


def _init(self, w, h):
    _orig_init(self, w, h)
    self.initial_h = h


K.__init__ = _init


def concepts_release_chain():
    c = K(800, 400)
    tiers = [
        dict(pos=1, name="Early Bird", status="Active", pct=40, line="On sale"),
        dict(pos=2, name="General Admission", status="Inactive", pct=0,
             line="Activates automatically when 'Early Bird' sells out"),
        dict(pos=3, name="Final Release", status="Inactive", pct=0,
             line="Activates automatically when 'General Admission' sells out"),
    ]
    h, g = chain_panel(c, 20, 20, 760, tiers, "1 chain · 1 auto-releasing", copy_to=False, add_select=False, badge=0)
    c.h = 20 + h + 20
    finish(c, f"{TK}/concepts-release-chain-panel.svg")


def fees_drawers(c, x, y, show_summary=True):
    pass


def concepts_how_fees():
    c = K(880, 464)
    # left: Edit Ticket drawer fragment (w 384)
    lx, ly, lw = 20, 20, 384
    c.box(lx, ly, lw, 214, BG, "#fff", 0, BORDER_OP)
    c.label(lx + 20, ly + 36, "Price*")
    c.field(lx + 20, ly + 46, lw - 40, "30", prefix="USD")
    c.t(lx + 20, ly + 112, "Buyer pays: 32.50, You receive: 30.00", 14, MFG)
    c.t(lx + 20, ly + 136, "How fees work", 13, BTN)
    # right: How Fees Work drawer (w 384)
    rx, ry, rw, rh = 440, 20, 384, 424
    c.box(rx, ry, rw, rh, BG, "#fff", 0, BORDER_OP)
    c.icon("chevron-left", rx + 28, ry + 28, 16, FG)
    c.t(rx + rw / 2, ry + 37, "How Fees Work", 18, FG, 600, "middle")
    sections = [("Cost to buyer", [("Ticket Price", "USD 30.00"), ("Service Fee", "USD 2.50"), ("VAT", "USD 0.00"), ("Buyer Pays", "USD 32.50")]),
                ("Your Revenue", [("Ticket Price", "USD 30.00"), ("Absorbed Fee", "USD 0.00"), ("VAT", "USD 0.00"), ("You Receive", "USD 30.00")])]
    yy = ry + 76
    for title, rows in sections:
        c.t(rx + 20, yy + 14, title, 14, FG, 600)
        c.card(rx + 20, yy + 24, rw - 40, 134, 14)
        ry2 = yy + 24 + 30
        for i, (k, v) in enumerate(rows):
            last = i == len(rows) - 1
            if last:
                ry2 += 6
                c.line(rx + 44, ry2 - 18, rx + rw - 44, ry2 - 18)
                ry2 += 4
            c.kv_row(rx + 44, ry2, rw - 88, k, v, bold=last)
            ry2 += 24
        yy += 170
    c.h = 464
    finish(c, f"{TK}/concepts-how-fees-work.svg")




def rn(c, b, n, px=4, py=0):
    """Orange ring around box b with its numbered callout on the top-left corner."""
    c.ring(b[0] - px, b[1] - py, b[2] + 2 * px, b[3] + 2 * py, 8)
    c.callout(b[0] - px, b[1] - py, n)


# ================================================================ shared form helpers
def fi(c, x, y, w, label, desc=None):
    """FormItem header: label (+ optional description). Returns y of the control."""
    c.label(x, y + 11, label)
    if desc:
        c.desc(x, y + 37, desc)
        return y + 50
    return y + 22


def drawer(c, x, y, w, h, title=None, top_cut=False):
    c.box(x, y, w, h, BG, "#fff", 0, BORDER_OP)
    if title:
        c.t(x + 16, y + 34, title, 16, FG, 600)


def footer(c, x, y, w, border=False):
    if border:
        c.line(x, y, x + w, y)
    c.button(x + 20, y + 20, 84, "Cancel", "outline")
    c.button(x + 116, y + 20, 74, "Save", "default")


# ================================================================ ticket management
def tm_overview():
    c = K(800, 560)
    x, w = 20, 760
    y = 20
    tw = c.tabs(x, y, ["Tickets", "Add-ons"], 0, w=200)
    c.ring(x - 4, y - 4, tw + 8, 44, 12)
    c.callout(x - 4, y - 2, 1)
    # filters
    fy = 76
    c.label(x, fy + 11, "Ticket Status")
    c.select(x, fy + 22, 160, placeholder="All")
    c.label(x + 180, fy + 11, "Session")
    c.select(x + 180, fy + 22, 160, placeholder="All")
    c.label(x + 360, fy + 11, "Search")
    c.field(x + 360, fy + 22, 320, placeholder="Ticket Name / Bundle Name", icon="search")
    c.ring(x - 12, fy - 10, 708, 76, 10)
    c.callout(x - 12, fy - 10, 2)
    # session 1 (open)
    sy = 176
    c.box(x, sy, w, 56, MUTED, None, 8)
    c.t(x + 16, sy + 26, "Friday Night", 16, FG, 600)
    c.t(x + 16, sy + 44, "Nov 13, 9:00 PM - Nov 14, 3:00 AM", 13, MFG)
    c.icon("chevron-down", x + w - 32, sy + 20, 16, FG)
    py = sy + 56 + 8
    ph, pg = chain_panel(c, x, py, w, [], "No chains yet", open_=False, badge=0)
    ty = py + ph + 8
    rows = [
        dict(total=100, name="VIP Early Access", price="60.00", sold=0, avail=100, status="Active",
             hint=("Sales starts in 12 days", MFG)),
        dict(total=300, name="General Admission", price="30.00", sold=120, avail=180, status="Active"),
    ]
    th, g = ticket_table(c, x, ty, w, rows)
    s0 = g["rows"][0]["sel"]
    c.ring(s0[0] - 4, s0[1] - 4, s0[2] + 8, s0[3] + 8, 10)
    c.callout(s0[0] - 4, s0[1] - 6, 3)
    p0 = g["rows"][0]["pencil"]
    c.ring(p0[0] - 8, p0[1] - 8, 32, 32, 8)
    c.callout(p0[0] - 8, p0[1] - 8, 4)
    # session 2 (collapsed)
    s2 = ty + th + 12
    c.t(x + 16, s2 + 26, "Saturday Night", 16, FG, 600)
    c.t(x + 16, s2 + 44, "Nov 14, 9:00 PM - Nov 15, 3:00 AM", 13, MFG)
    c.icon("chevron-right", x + w - 32, s2 + 20, 16, FG)
    c.h = s2 + 56 + 20
    finish(c, f"{TK}/ticket-management-overview.svg")


def date_row(c, x, y, w, label, date, hh, mm):
    """SelectDate row: label + date button on the left, Hour:Minute on the right."""
    c.label(x, y + 11, label)
    c.box(x, y + 22, 190, 36, "#fff", "#fff", 8, INPUT_OP, op=0.045)
    c.t(x + 12, y + 22 + 23, date, 14, FG)
    c.icon("calendar", x + 190 - 28, y + 22 + 10, 16, MFG, op=0.7)
    hx = x + w - 114
    c.label(hx, y + 11, "Hour*")
    c.box(hx, y + 22, 55, 36, "#fff", "#fff", 8, INPUT_OP, op=0.045)
    c.t(hx + 27, y + 22 + 23, hh, 14, FG, anchor="middle")
    c.t(hx + 55 + 2, y + 22 + 22, ":", 14, FG, anchor="middle")
    c.label(hx + 59, y + 11, "Minute*")
    c.box(hx + 59, y + 22, 55, 36, "#fff", "#fff", 8, INPUT_OP, op=0.045)
    c.t(hx + 59 + 27, y + 22 + 23, mm, 14, FG, anchor="middle")
    return y + 58


def tm_edit_panel():
    H = 488
    c = K(840, H + 40)
    pw = 384
    lx, rx, ty = 20, 436, 20
    # left drawer
    drawer(c, lx, ty, pw, H, "Edit Ticket")
    px = lx + 20
    iw = pw - 40
    y = ty + 72
    ctrl = fi(c, px, y, iw, "Name*")
    c.field(px, ctrl, iw, "General Admission", disabled=True)
    c.t(px, ctrl + 36 + 17, "Name cannot be modified after tickets have been", 13, AMBER5)
    c.t(px, ctrl + 36 + 33, "sold (40 sold)", 13, AMBER5)
    name_box = (px - 6, y - 6, iw + 12, 22 + 36 + 38 + 6)
    y += 22 + 36 + 38 + 24
    ctrl = fi(c, px, y, iw, "Total Quantity*")
    c.field(px, ctrl, iw, "300")
    qty_box = (px - 6, y - 6, iw + 12, 22 + 36 + 12)
    y += 22 + 36 + 24
    ctrl = fi(c, px, y, iw, "Price*")
    c.field(px, ctrl, iw, "30", prefix="USD", disabled=True)
    c.t(px, ctrl + 36 + 17, "Price cannot be modified after tickets have been", 13, AMBER5)
    c.t(px, ctrl + 36 + 33, "sold (40 sold)", 13, AMBER5)
    price_box = (px - 6, y - 6, iw + 12, 22 + 36 + 38 + 6)
    fy = ctrl + 36 + 33 + 14
    c.t(px, fy + 14, "Buyer pays: 32.50, You receive: 30.00", 14, MFG)
    c.t(px, fy + 34, "How fees work", 13, BTN)
    fees_box = (px - 6, fy - 2, iw + 12, 44)
    rn(c, name_box, 1)
    rn(c, price_box, 1)
    rn(c, qty_box, 2)
    rn(c, fees_box, 5)
    # right drawer (the same form, scrolled down)
    drawer(c, rx, ty, pw, H)
    px = rx + 20
    y = ty + 20
    y0 = y
    y = date_row(c, px, y, iw, "Sales Start Date *", "Nov 1, 2026", "10", "00")
    y += 24
    y = date_row(c, px, y, iw, "Sales End Date *", "Nov 13, 2026", "20", "00")
    dates_box = (px - 6, y0 - 6, iw + 12, y - y0 + 12)
    y += 24
    y1 = y
    ctrl = fi(c, px, y, iw, "Limit Qty per Order")
    c.field(px, ctrl, iw, "4")
    y += 58 + 24
    ctrl = fi(c, px, y, iw, "Limit Qty per User")
    c.field(px, ctrl, iw, "8")
    limits_box = (px - 6, y1 - 6, iw + 12, y + 58 - y1 + 12)
    rn(c, dates_box, 3)
    rn(c, limits_box, 4)
    footer(c, rx, ty + H - 76, pw, border=False)
    c.h = ty + H + 20
    finish(c, f"{TK}/ticket-management-edit-panel.svg")


def tm_release_panel():
    c = K(800, 560)
    tiers = [
        dict(pos=1, name="Early Bird", status="Sold out", pct=100, line="Sold out — next tier opened"),
        dict(pos=2, name="General Admission", status="Active", pct=62, line="On sale"),
        dict(pos=3, name="Final Release", status="Inactive", pct=0,
             line="Activates automatically when 'General Admission' sells out"),
    ]
    h, g = chain_panel(c, 20, 56, 760, tiers, "1 chain · 1 auto-releasing", copy_to=True, add_select=True, badge=3)
    n = g["new"]
    c.ring(n[0] - 3, n[1] - 3, n[2] + 6, n[3] + 6, 10); c.callout(n[0] + n[2] / 2, n[1] + n[3] + 26, 1)
    s = g["switch"]; sl = g["switch_label"]
    c.ring(sl[0] - 4, sl[1] - 3, sl[2] + 6, sl[3] + 6, 8); c.callout(sl[0] + 30, sl[1] - 20, 2)
    t2 = g["tiers"][1]
    # progress bar of tier 2: reconstruct its position
    nm = "2. General Admission"
    px = t2[0] + 32 + est(nm) + 12 + 14 + est("Active") + 12
    c.ring(px - 4, t2[1] + 6 + 7 - 5, 112 + 8, 16, 6)
    c.callout(px + 56, t2[1] + 6 + 7 - 22, 3)
    lg = g["log"]
    c.ring(lg[0] - 1, lg[1] - 1, lg[2] + 2, lg[3] + 2, 8); c.callout(lg[0] + 16, lg[1] + lg[3] + 26, 4)
    cp = g["copy"]
    c.ring(cp[0] - 3, cp[1] - 3, cp[2] + 6, cp[3] + 6, 8); c.callout(cp[0] + cp[2] / 2, cp[1] - 20, 5)
    tr = g["trash"]
    c.ring(tr[0] - 2, tr[1] - 2, tr[2] + 4, tr[3] + 4, 8); c.callout(tr[0] + 16, tr[1] - 20, 6)
    c.h = 56 + h + 20
    finish(c, f"{TK}/ticket-management-release-chains-panel.svg")


def tm_tier_messages():
    c = K(960, 600)
    tiers = [
        dict(pos=1, name="Early Bird", status="Sold out", pct=100, line="Sold out — next tier opened"),
        dict(pos=2, name="General Admission", status="Active", pct=62, line="On sale"),
        dict(pos=3, name="Final Release", status="Inactive", pct=0,
             line="Activates automatically when 'General Admission' sells out"),
    ]
    h, g = chain_panel(c, 20, 20, 920, tiers, "1 chain · 1 auto-releasing", copy_to=True, add_select=False, badge=0)
    rows = [
        dict(total=300, name="General Admission", price="30.00", sold=120, avail=180, status="Active",
             chips=["GA · 2/3"], hint=("Auto-activated when 'Early Bird' sold out.", MFG)),
        dict(total=100, name="Final Release", price="40.00", sold=0, avail=100, status="Inactive",
             chips=["GA · 3/3"], hint=("Activates automatically when 'General Admission' sells out", MFG)),
    ]
    cols = dict(total=44, name=96, price=250, sold=346, avail=404, status=488)
    th, g2 = ticket_table(c, 20, 20 + h + 12, 920, rows, cols)
    c.h = 20 + h + 12 + th + 20
    finish(c, f"{TK}/ticket-management-chain-tier-messages.svg")


def tm_create_addon():
    c = K(520, 600)
    pw, x = 480, 20
    top = 0
    drawer(c, x, top, pw, 580)
    px, iw = x + 20, pw - 40
    y = top + 30
    ctrl = fi(c, px, y, iw, "Linked to*")
    c.box(px, ctrl, iw, 36, "#fff", "#fff", 8, INPUT_OP, op=0.045)
    c.t(px + 16, ctrl + 23, "General Admission + 1 more", 14, FG, 500)
    c.icon("chevrons-up-down", px + iw - 28, ctrl + 10, 16, MFG, op=0.5)
    b1 = (px - 6, y - 6, iw + 12, 22 + 36 + 12)
    y += 22 + 36 + 24
    ctrl = fi(c, px, y, iw, "Inventory Source*")
    c.select(px, ctrl, iw, "Sync from ticket", hint="(Use another ticket type's inventory)")
    b2 = (px - 6, y - 6, iw + 12, 22 + 36 + 12)
    y += 22 + 36 + 24
    ctrl = fi(c, px, y, iw, "Source Ticket Type*", "Sales of this add-on will reduce selected ticket's inventory")
    c.select(px, ctrl, iw, "General Admission")
    b3 = (px - 6, y - 6, iw + 12, 50 + 36 + 12)
    y += 50 + 36 + 24
    ctrl = fi(c, px, y, iw, "Add-on Sales Limit*", "Limit add-on sales while using the source ticket inventory")
    c.field(px, ctrl, iw, "50")
    b4 = (px - 6, y - 6, iw + 12, 50 + 36 + 12)
    y += 50 + 36 + 24
    ctrl = fi(c, px, y, iw, "Face Value*")
    c.field(px, ctrl, iw, "15", prefix="USD")
    c.t(px, ctrl + 36 + 22, "Buyer pays: 16.20, You receive: 15.00", 14, MFG)
    c.t(px, ctrl + 36 + 42, "How fees work", 13, BTN)
    b5 = (px - 6, y - 6, iw + 12, 22 + 36 + 48 + 12)
    for n, b in enumerate([b1, b2, b3, b4, b5], 1):
        rn(c, b, n)
    c.h = max(b5[1] + b5[3] + 20, 0)
    c.parts[1:1] = []
    # panel height matches content
    c.parts[1] = c.parts[1]  # no-op, keeps order explicit
    finish(c, f"{TK}/ticket-management-create-addon.svg")


def tm_addons_table():
    c = K(800, 360)
    x, w = 20, 760
    c.tabs(x, 20, ["Tickets", "Add-ons"], 1, w=200)
    c.button(x + w - 160, 20, 160, "Create Add-on", "default", icon="plus")
    fy = 76
    c.label(x, fy + 11, "Add-on Status")
    c.select(x, fy + 22, 160, placeholder="All")
    c.label(x + 180, fy + 11, "Search")
    c.field(x + 180, fy + 22, 320, placeholder="Add-on Name", icon="search")
    rows = [
        dict(total=100, name="Parking Pass", price="15.00", sold=22, avail=78, status="Active"),
        dict(total=50, name="VIP Lounge Access", price="25.00", sold=10, avail=40, status="Active"),
        dict(total=120, name="Festival T-Shirt", price="20.00", sold=45, avail=75, status="Inactive"),
    ]
    cols = dict(total=12, name=84, price=300, sold=410, avail=480, status=584)
    ty = fy + 70 + 20
    th, g = ticket_table(c, x, ty, w, rows, cols, name_header="Add-on Name", grip=False, fit=True)
    # status column header positions are fine; ring edit icon of row 1
    c.h = ty + th + 20
    finish(c, f"{TK}/ticket-management-addons-table.svg")




# ================================================================ comp tickets
def metric_card(c, x, y, w, label, big, small=None, info=False, h=88, unit_sep=True):
    """MetricsCard: border rounded-md p-5, label text-sm muted, value text-xl bold."""
    c.surface(x, y, w, h)
    c.t(x + 20, y + 20 + 14, label, 14, MFG)
    if info:
        c.icon("info", x + 20 + est(label) + 8, y + 20 + 1, 14, MFG)
    vy = y + 20 + 14 + 8 + 20
    c.t(x + 20, vy, big, 20, FG, 700)
    if small:
        sx = x + 20 + est(big, 20, True) + 6
        if unit_sep:
            c.t(sx, vy, "/", 13, MFG)
            sx += 12
        c.t(sx, vy, small, 13, MFG)


def sort_head(c, x, y, s):
    """SortButton: link variant (btn-primary text) with stacked up/down chevrons."""
    c.t(x, y, s, 14, BTN, 500)
    sx = x + est(s, 14, True) + 10
    c.icon("sort-up", sx - 4, y - 18, 16, MFG, 2)
    c.icon("sort-down", sx - 4, y - 10, 16, MFG, 2)


def comp_list():
    c = K(800, 560)
    x, w = 20, 760
    y = 20
    cw = (w - 32) / 2
    metric_card(c, x, y, cw, "Total Recipients", "4")
    metric_card(c, x + cw + 32, y, cw, "Total Tickets", "7")
    c.ring(x - 6, y - 6, w + 12, 100, 10); c.callout(x - 6, y - 6, 1)
    y += 88 + 24
    bw = 262
    c.button(x + w - bw, y, bw, "Create Complimentary Tickets", "default", icon="plus")
    c.ring(x + w - bw - 4, y - 4, bw + 8, 44, 10); c.callout(x + w - bw - 4, y - 4, 3)
    y += 36 + 20
    c.field(x, y, w, placeholder="Search by name or email")
    c.ring(x - 4, y - 4, w + 8, 44, 10); c.callout(x - 4, y - 4, 2)
    y += 36 + 20
    # table
    cols = [14, 210, 366, 450, 612]
    hh, rh = 40, 56
    rows = [
        ("Alex Chen", "alex@example.com", "General Admission", "2", "Oct 28, 2026, 14:05", "Press", "dl"),
        ("Maya Patel", "maya@example.com", "VIP", "1", "Oct 28, 2026, 14:02", "Sponsor", "dl"),
        ("Sam Rivera", "sam@example.com", "General Admission", "3", "Oct 27, 2026, 10:30", "Guest list", "dl"),
        ("Jordan Lee", "jordan@example.com", "VIP", "1", "Oct 30, 2026, 09:12", "Staff", "gen"),
    ]
    th = hh + rh * len(rows)
    c.surface(x, y, w, th)
    c.line(x, y + hh, x + w, y + hh)
    for cx, name in zip(cols, ["Name", "Ticket Type", "Quantity", "Sent Date", "Remarks"]):
        sort_head(c, x + cx, y + 25, name)
    yy = y + hh
    for i, (nm, em, tk, q, dt, rm, st) in enumerate(rows):
        cy = yy + rh / 2
        c.t(x + cols[0], cy - 3, nm, 14)
        c.t(x + cols[0], cy + 17, em, 14, MFG)
        c.t(x + cols[1], cy + 5, tk, 14)
        c.t(x + cols[2], cy + 5, q, 14)
        c.t(x + cols[3], cy + 5, dt, 14)
        c.t(x + cols[4], cy + 5, rm, 14)
        if st == "dl":
            c.icon("download", x + w - 36, cy - 8, 16, FG)
            if i == 0:
                c.ring(x + w - 46, cy - 18, 36, 36, 8)
                c.callout(x + w - 46, cy - 18, 4)
        else:
            c.t(x + w - 12, cy + 5, "Generating...", 14, MFG, anchor="end")
        yy += rh
        if i < len(rows) - 1:
            c.line(x, yy, x + w, yy)
    c.h = y + th + 20
    finish(c, f"{TK}/comp-tickets-list.svg")


def comp_drawer_head(c, x, y, w, h):
    c.box(x, y, w, h, BG, "#fff", 0, BORDER_OP)
    c.t(x + 16, y + 34, "Create Complimentary Tickets", 16, FG, 600)


def comp_single():
    c = K(840, 560)
    x, y, w = 20, 20, 500
    comp_drawer_head(c, x, y, w, 520)
    px, iw = x + 20, w - 40
    ty = y + 56 + 16
    c.tabs(px, ty, ["Single Creation", "Bulk Creation"], 0, w=iw)
    yy = ty + 36 + 24
    c.switch(px, yy + 3, True)
    c.t(px + 40, yy + 16, "Email ticket to recipient", 14, FG, 500)
    sw_box = (px - 2, yy - 2, 40 + est("Email ticket to recipient", 14, True) + 6, 26)
    yy += 24 + 24
    ctrl = fi(c, px, yy, iw, "Name*"); c.field(px, ctrl, iw, "Alex Chen")
    yy += 58 + 24
    ctrl = fi(c, px, yy, iw, "Email*"); c.field(px, ctrl, iw, "alex@example.com")
    yy += 58 + 24
    ctrl = fi(c, px, yy, iw, "Ticket Type*"); c.select(px, ctrl, iw, "General Admission")
    tt = (px, yy, iw, 58)
    sel_y = ctrl
    yy += 58 + 24
    ctrl = fi(c, px, yy, iw, "Quantity*"); c.field(px, ctrl, iw, "2")
    qb = (px, yy, iw, 58)
    rn(c, sw_box, 1, 4, 2)
    rn(c, tt, 2, 8, 6)
    rn(c, qb, 3, 8, 6)
    # the opened Ticket Type list (popover), shown beside the form
    ppx, ppy, pw = x + w + 28, sel_y + 40, 280
    c.box(ppx, ppy, pw, 76, CARD, "#fff", 8, BORDER_OP)
    c.t(ppx + 12, ppy + 4 + 22, "General Admission", 14, FG)
    c.icon("check", ppx + pw - 26, ppy + 4 + 8, 16, FG)
    c.t(ppx + 12, ppy + 4 + 32 + 22, "VIP Table", 14, FG, op=0.5)
    c.box(ppx + pw - 12 - 70, ppy + 4 + 32 + 7, 70, 20, MUTED, None, 2, op=0.5)
    c.t(ppx + pw - 12 - 35, ppy + 4 + 32 + 22, "Sold out", 13, FG, anchor="middle", op=0.5)
    c.h = y + 520 + 20
    finish(c, f"{TK}/comp-tickets-single-form.svg")


def recipients_table(c, x, y, w, rows, add=True):
    """Bulk recipients: border rounded-lg; header grid-cols-12 gap-4 p-3."""
    unit = (w - 24 - 11 * 16) / 12
    cx = [12, 12 + 4 * unit + 4 * 16, 12 + 8 * unit + 8 * 16, 12 + 11 * unit + 11 * 16]
    spans = [4 * unit + 3 * 16, 4 * unit + 3 * 16, 3 * unit + 2 * 16]
    hh = 40
    th = hh + 60 * len(rows) + (60 if add else 0)
    c.box(x, y, w, th, BG, "#fff", 10, BORDER_OP)
    c.box(x + 1, y + 1, w - 2, hh - 1, MUTED, None, 9, op=0.5)
    for dx, s in zip(cx, ["Name", "Email", "Qty (Max 10)"]):
        c.t(x + dx, y + 25, s, 13, MFG, 500)
    yy = y + hh
    for nm, em, q in rows:
        c.line(x, yy, x + w, yy)
        c.field(x + cx[0], yy + 12, spans[0], nm)
        c.field(x + cx[1], yy + 12, spans[1], em)
        c.field(x + cx[2], yy + 12, spans[2], q)
        c.icon("trash", x + cx[3] + 2, yy + 20, 16, "#ef4444")
        yy += 60
    if add:
        c.line(x, yy, x + w, yy)
        c.button(x + 12, yy + 12, w - 24, "Add Recipient", "outline", icon="plus")
    return th, cx, spans


RECIP = [("Alex Chen", "alex@demo.com", "2"), ("Maya Patel", "maya@demo.com", "2"), ("Sam Rivera", "sam@demo.com", "1")]


def comp_bulk():
    c = K(560, 520)
    x, y, w = 20, 0, 500
    c.box(x, y - 2, w, 464, BG, "#fff", 0, BORDER_OP)
    px, iw = x + 20, w - 40
    yy = y + 28
    c.label(px, yy + 11, "Recipients *")
    c.t(px + iw, yy + 12, "3/50", 14, MFG, anchor="end")
    cnt = (px + iw - est("3/50") - 6, yy - 2, est("3/50") + 12, 22)
    yy += 24
    c.t(px, yy + 14, "Total Tickets: 5 | Remaining: 200", 14, MFG)
    tot = (px - 6, yy - 2, est("Total Tickets: 5 | Remaining: 200") + 12, 22)
    yy += 28
    th, cx, spans = recipients_table(c, px, yy, iw, RECIP)
    q = (px + cx[2] - 8, yy + 6, spans[2] + 16, 28)
    yy += th + 20
    # footer (fixed bottom of the drawer)
    fy = yy + 4
    c.line(x, fy, x + w, fy)
    c.button(px, fy + 20, 84, "Cancel", "outline")
    c.button(px + 96, fy + 20, 74, "Save", "default")
    rn(c, cnt, 1, 4, 2)
    rn(c, q, 2, 2, 2)
    rn(c, tot, 3, 4, 2)
    rn(c, (px + 92, fy + 16, 82, 44), 4, 2, 0)
    c.h = fy + 76 + 2
    finish(c, f"{TK}/comp-tickets-bulk-form.svg")


def comp_csv():
    c = K(560, 600)
    x, y, w = 20, 0, 500
    px, iw = x + 20, w - 40
    yy = y + 28
    c.label(px, yy + 21, "Import from CSV")
    bw1, bw2 = 168, 120
    b2x = px + iw - bw2
    b1x = b2x - 8 - bw1
    c.button(b1x, yy + 6, bw1, "Download Template", "outline", icon="download", h=32, size=14)
    c.button(b2x, yy + 6, bw2, "Upload CSV", "outline", icon="upload", h=32, size=14)
    rn(c, (b1x, yy + 6, bw1, 32), 2, 2, 3)
    rn(c, (b2x, yy + 6, bw2, 32), 1, 2, 3)
    yy += 44 + 12
    c.t(px, yy + 14, "Paste CSV data below (Name, Email, Qty) or upload a CSV file", 14, MFG)
    yy += 20 + 12 + 8
    c.textarea(px, yy, iw, 100, placeholder="", lines=["John Doe,john@example.com,6", "Jane Smith,jane@example.com,8"])
    rn(c, (px, yy, iw, 100), 3, 4, 4)
    yy += 100 + 16
    c.button(px, yy, iw, "Parse & Preview", "outline", icon="file-spreadsheet")
    yy += 36 + 24
    c.label(px, yy + 11, "Recipients *")
    c.t(px + iw, yy + 12, "3/50", 14, MFG, anchor="end")
    yy += 24 + 4
    th, cx, spans = recipients_table(c, px, yy, iw, RECIP, add=False)
    rn(c, (px, yy, iw, th), 4, 4, 4)
    c.h = yy + th + 24
    finish(c, f"{TK}/comp-tickets-csv-import.svg")



# ================================================================ ticket report
def report_cards():
    c = K(960, 140)
    x, y = 20, 20
    gap = 24
    cw = (920 - 3 * gap) / 4
    metric_card(c, x, y, cw, "Total Revenue", "12,480.00", "USD")
    metric_card(c, x + (cw + gap), y, cw, "Tickets Sold", "412", "500", info=True)
    metric_card(c, x + 2 * (cw + gap), y, cw, "Personalization Progress", "180", "412")
    metric_card(c, x + 3 * (cw + gap), y, cw, "Add-ons Sold", "36", "100", info=True)
    c.h = y + 88 + 20
    finish(c, f"{TK}/ticket-report-summary-cards.svg")


def report_filters():
    c = K(960, 130)
    y = 30
    # Date: two joined 120px buttons
    c.label(20, y + 11, "Date")
    c.box(20, y + 22, 252, 36, None, "#fff", 8, INPUT_OP)
    for i, bx in enumerate([20, 152]):
        c.box(bx + 1, y + 23, 119, 34, "#fff", None, 7, op=0.045)
        c.t(bx + 12, y + 22 + 23, "Start" if i == 0 else "End", 14, MFG)
        c.icon("calendar", bx + 120 - 28, y + 22 + 10, 16, MFG, op=0.6)
    c.line(132, y + 40, 138, y + 40, NEUT4, 1, 1)
    c.label(292, y + 11, "Session")
    c.select(292, y + 22, 150, "Friday Night", clear=True)
    c.label(462, y + 11, "Item")
    c.select(462, y + 22, 170, "Early Bird", clear=True)
    c.label(652, y + 11, "Search")
    c.field(652, y + 22, 180, placeholder="Search by email", icon="search")
    c.button(850, y + 22, 92, "Export", "default", icon="arrow-up-from-line")
    items = [(20, 252, 1), (292, 150, 2), (462, 170, 3), (652, 180, 4), (850, 92, 5)]
    for x0, w0, n in items:
        c.ring(x0 - 4, y - 6, w0 + 8, 70, 8)
        c.callout(x0 - 4, y - 6, n)
    c.h = y + 58 + 28
    finish(c, f"{TK}/ticket-report-filters.svg")


def report_table():
    c = K(1000, 600)
    x, w = 20, 960
    cols = [12, 160, 322, 466, 576, 700, 832]
    heads = ["Date & Time", "User", "Item", "Promo Code", "Revenue (USD)", "Affiliate Code", "Payment Method"]
    rows = [
        dict(dt="Oct 28, 2026, 19:45", nm="Alex Chen", fl="SG", em="alex@example.com", item="General Admission", promo="EARLY10", rev="27.00", aff="", pm="Card"),
        dict(dt="Oct 28, 2026, 19:12", nm="Maya Patel", fl="DE", em="maya@example.com", item="General Admission", promo="", rev="30.00", aff="JORDAN", pm="Card"),
        dict(dt="Oct 28, 2026, 18:50", nm="Sam Rivera", fl="JP", em="sam@example.com", item="Parking Pass", sub="Add-on", promo="", rev="15.00", aff="", pm="Card"),
        dict(dt="Oct 28, 2026, 18:21", nm="Jordan Lee", fl="FR", em="jlee@example.com", item="General Admission", sub="Group of 4", promo="", rev="30.00", aff="", pm="Card"),
        dict(dt="Oct 28, 2026, 17:05", nm="Taylor Kim", em="tkim@example.com", item="VIP Pass", ic="triangle-alert", promo="", rev="80.00", aff="", pm="Card"),
        dict(dt="Oct 28, 2026, 16:40", nm="Alex Chen", em="alex@example.com", item="VIP Pass", ic="circle-check", promo="", rev="80.00", aff="", pm="Card"),
    ]
    y = 20
    hh, rh = 40, 56
    th = hh + rh * len(rows)
    c.surface(x, y, w, th)
    c.line(x, y + hh, x + w, y + hh)
    for cx, s in zip(cols, heads):
        c.t(x + cx, y + 25, s, 14, FG, 500)
    yy = y + hh
    geo = {}
    for i, r in enumerate(rows):
        cy = yy + rh / 2
        c.t(x + cols[0], cy + 5, r["dt"], 14)
        c.t(x + cols[1], cy - 3, r["nm"], 14)
        if r.get("fl"):
            c.flag(x + cols[1] + est(r["nm"]) + 8, cy - 15, r["fl"])
        c.t(x + cols[1], cy + 17, r["em"], 14, MFG)
        c.t(x + cols[2], cy - 3 if r.get("sub") else cy + 5, r["item"], 14)
        if r.get("sub"):
            c.t(x + cols[2], cy + 17, r["sub"], 14, MFG)
            if r["sub"] == "Group of 4":
                geo["bundle"] = (x + cols[2] - 6, cy + 1, est(r["sub"]) + 12, 24)
        if r.get("ic"):
            ix = x + cols[2] + est(r["item"]) + 8
            c.icon(r["ic"], ix, cy - 8, 16, YELLOW5 if r["ic"] == "triangle-alert" else GREEN6)
            if r["ic"] == "triangle-alert":
                geo["pers"] = (ix - 4, cy - 12, 24, 24)
        c.t(x + cols[3], cy + 5, r["promo"], 14)
        c.t(x + cols[4], cy + 5, r["rev"], 14)
        c.t(x + cols[5], cy + 5, r["aff"], 14)
        c.t(x + cols[6], cy + 5, r["pm"], 14)
        if r["promo"] and "promo" not in geo:
            geo["promo"] = (x + cols[3] - 8, y + 4, 100, th - 8)
        if r["aff"] and "aff" not in geo:
            geo["aff"] = (x + cols[5] - 8, y + 4, 120, th - 8)
        yy += rh
        if i < len(rows) - 1:
            c.line(x, yy, x + w, yy)
    # pagination bar
    py = y + th + 16
    c.t(x + 20, py + 25, "Total", 14, MFG)
    c.t(x + 20 + 40, py + 25, "6", 14, "#e5e5e5", 600)
    c.t(x + 20 + 40 + 14, py + 25, "items", 14, MFG)
    rx = x + w - 20
    # chevron buttons
    for i, ic in enumerate(["chevrons-right", "chevron-right", "chevron-left", "chevrons-left"]):
        c.icon(ic, rx - 16 - i * 40, py + 17, 16, "#e5e5e5", op=0.4)
    # page of
    pg = "Page 1 of 1"
    px = rx - 4 * 40 - 24 - est(pg)
    c.t(px, py + 25, "Page ", 14, MFG)
    c.t(px + est("Page "), py + 25, "1", 14, "#e5e5e5", 600)
    c.t(px + est("Page ") + 14, py + 25, " of 1", 14, MFG)
    # rows per page
    sx = px - 40 - 70
    c.t(sx - 8 - est("Rows per page"), py + 25, "Rows per page", 14, MFG)
    c.box(sx, py + 8, 70, 32, "#fff", "#fff", 8, INPUT_OP, op=0.045)
    c.t(sx + 12, py + 29, "10", 14, "#e5e5e5")
    c.icon("chevron-down", sx + 70 - 24, py + 16, 16, MFG, op=0.5)
    rp = (sx - 12 - est("Rows per page"), py + 6, 12 + est("Rows per page") + 70, 36)
    for k, n in [("promo", 1), ("aff", 2), ("bundle", 3), ("pers", 4)]:
        b = geo[k]
        c.ring(*b, 8)
        if k in ("promo", "aff"):
            c.callout(b[0] + b[2] / 2, b[1] - 8, n)
        elif k == "bundle":
            c.callout(b[0] - 12, b[1] + b[3] / 2, n)
        else:
            c.callout(b[0] + b[2], b[1], n)
    c.ring(rp[0] - 8, rp[1], rp[2] + 16, rp[3], 8)
    c.callout(rp[0] - 8, rp[1], 5)
    c.h = py + 56
    finish(c, f"{TK}/ticket-report-table.svg")


# ================================================================ payment links
def pl_table_head(c, x, y, w, cols, heads):
    c.surface(x, y, w, 10)  # replaced by caller via box
    c.parts.pop()
    for cx, s in zip(cols, heads):
        c.t(x + cx, y + 25, s, 14, FG, 500)


STATUS_STYLE = {"Pending": (ORANGE5, "circle-dashed"), "Paid": (GREEN5, "check"),
                "Expired": (GRAY5, "info"), "Closed": (RED5, "circle-slash")}
PL_COLS = [12, 170, 294, 400, 510, 640, 766, 856]
PL_HEADS = ["Buyer", "Item", "Price (USD)", "Status", "Revenue (USD)", "Payment Method", "Remarks", ""]
PL_ROWS = [
    ("Alex Chen", "alex@example.com", "VIP Table", "500.00", "Pending", "0.00", "", "Table 4"),
    ("Maya Patel", "maya@example.com", "Parking Pass", "40.00", "Paid", "40.00", "Card", "Rooftop"),
    ("Sam Rivera", "sam@example.com", "Merch Bundle", "85.00", "Expired", "0.00", "", ""),
    ("Jordan Lee", "jlee@example.com", "Lounge Access", "120.00", "Closed", "0.00", "", "Guest"),
]


def pl_row_actions(c, x, cy):
    c.icon("more-vertical", x + 10, cy - 8, 16, FG)
    c.icon("rotate-ccw", x + 50, cy - 8, 16, FG)


def pl_list():
    c = K(980, 520)
    x, w = 20, 940
    y = 20
    cw = (w - 32) / 2
    metric_card(c, x, y, cw, "Revenue", "40.00", "USD", unit_sep=False)
    metric_card(c, x + cw + 32, y, cw, "Successful Payments", "1", "4")
    c.ring(x - 6, y - 6, w + 12, 100, 10); c.callout(x - 6, y - 6, 1)
    y += 88 + 24
    c.field(x, y, 320, placeholder="Search by email or item")
    cl = 148
    c.button(x + w - cl, y, cl, "Create Link", "default", icon="plus")
    ex = 140
    c.button(x + w - cl - 8 - ex, y, ex, "Export CSV", "outline", icon="arrow-up-from-line")
    c.ring(x + w - cl - 4, y - 4, cl + 8, 44, 10); c.callout(x + w - cl - 4, y - 4, 2)
    c.ring(x + w - cl - 8 - ex - 4, y - 4, ex + 8, 44, 10); c.callout(x + w - cl - 8 - ex - 4, y - 4, 3)
    y += 36 + 20
    hh, rh = 40, 56
    th = hh + rh * 4
    c.surface(x, y, w, th)
    c.line(x, y + hh, x + w, y + hh)
    for cx, s in zip(PL_COLS, PL_HEADS):
        c.t(x + cx, y + 25, s, 14, FG, 500)
    yy = y + hh
    for i, (nm, em, item, price, st, rev, pm, rm) in enumerate(PL_ROWS):
        cy = yy + rh / 2
        c.t(x + PL_COLS[0], cy - 3, nm, 14)
        c.t(x + PL_COLS[0], cy + 17, em, 14, MFG)
        c.t(x + PL_COLS[1], cy + 5, item, 14)
        c.t(x + PL_COLS[2], cy + 5, price, 14)
        fill, ic = STATUS_STYLE[st]
        c.badge_pill(x + PL_COLS[3], cy - 12, st, fill, 14, icon=ic, h=24)
        c.t(x + PL_COLS[4], cy + 5, rev, 14)
        c.t(x + PL_COLS[5], cy + 5, pm, 14)
        c.t(x + PL_COLS[6], cy + 5, rm, 14)
        pl_row_actions(c, x + PL_COLS[7] - 4, cy)
        yy += rh
        if i < 3:
            c.line(x, yy, x + w, yy)
    c.ring(x + PL_COLS[3] - 8, y + 4, 110, th - 8, 10); c.callout(x + PL_COLS[3] - 8, y + 4, 4)
    c.ring(x + PL_COLS[7] - 10, y + hh + 6, 86, rh - 12, 10); c.callout(x + PL_COLS[7] - 10, y + hh + 6, 5)
    c.h = y + th + 20
    finish(c, f"{OT}/payment-links-list.svg")


def pl_create():
    c = K(840, 480)
    pw, H = 384, 440
    lx, rx, ty = 20, 436, 20
    # left
    drawer(c, lx, ty, pw, H, "Create Link")
    px, iw = lx + 20, pw - 40
    y = ty + 72
    ctrl = fi(c, px, y, iw, "Item*", "Shown on payment page and receipt")
    c.field(px, ctrl, iw, "VIP Table")
    y += 50 + 36 + 24
    ctrl = fi(c, px, y, iw, "Item Price*")
    c.field(px, ctrl, iw, "500", prefix="USD")
    c.t(px, ctrl + 36 + 20, "You Receive:", 14, MFG)
    c.t(px + 96, ctrl + 36 + 20, "482.50", 14, MFG)
    c.t(px + 96 + 48, ctrl + 36 + 20, "USD", 14, MFG)
    y += 58 + 24 + 24
    ctrl = fi(c, px, y, iw, "Buyer Name*", "Shown on receipt")
    c.field(px, ctrl, iw, "Alex Chen")
    # right
    drawer(c, rx, ty, pw, H)
    px = rx + 20
    y = ty + 20
    c.label(px, y + 11, "Buyer Email*")
    c.desc(px, y + 37, "Send receipt to buyer")
    c.checkbox(px + iw - 14 - est("Use my email") - 8 - 16 + 14, y + 27, True)
    c.t(px + iw, y + 38, "Use my email", 14, FG, 500, "end")
    c.field(px, y + 50, iw, "alex@example.com")
    y += 50 + 36 + 24
    ctrl = fi(c, px, y, iw, "Remarks", "Internal use only, not shown to buyer")
    c.field(px, ctrl, iw, "Table 4")
    y += 50 + 36 + 24
    c.t(px, y + 14, "Notes:", 14, MFG)
    for i, ln in enumerate(["Each link can only be paid once", "The links will expire 24 hours after creation"]):
        c.dot(px + 14, y + 14 + 20 * (i + 1) - 5, 2.5, MFG)
        c.t(px + 24, y + 14 + 20 * (i + 1), ln, 14, MFG)
    footer(c, rx, ty + H - 76, pw)
    c.h = ty + H + 20
    finish(c, f"{OT}/payment-links-create-panel.svg")


def pl_menu():
    c = K(980, 270)
    x, w = 20, 940
    y = 20
    hh, rh = 40, 56
    c.surface(x, y, w, hh + rh)
    c.line(x, y + hh, x + w, y + hh)
    for cx, s in zip(PL_COLS, PL_HEADS):
        c.t(x + cx, y + 25, s, 14, FG, 500)
    nm, em, item, price, st, rev, pm, rm = PL_ROWS[0]
    cy = y + hh + rh / 2
    c.t(x + PL_COLS[0], cy - 3, nm, 14)
    c.t(x + PL_COLS[0], cy + 17, em, 14, MFG)
    c.t(x + PL_COLS[1], cy + 5, item, 14)
    c.t(x + PL_COLS[2], cy + 5, price, 14)
    fill, ic = STATUS_STYLE[st]
    c.badge_pill(x + PL_COLS[3], cy - 12, st, fill, 14, icon=ic, h=24)
    c.t(x + PL_COLS[4], cy + 5, rev, 14)
    c.t(x + PL_COLS[6], cy + 5, rm, 14)
    pl_row_actions(c, x + PL_COLS[7] - 4, cy)
    # ghost button hover on the open trigger
    bx = x + PL_COLS[7] - 4
    c.box(bx - 2, cy - 18, 36, 36, MUTED, None, 8, op=0.5)
    c.icon("more-vertical", bx + 10, cy - 8, 16, FG)
    # DropdownMenuContent align=end
    mw, mh = 168, 104
    mx, my = bx + 34 - mw, cy + 18 + 4
    c.box(mx, my, mw, mh, CARD, "#fff", 8, BORDER_OP)
    for i, (lab, col) in enumerate([("Copy URL", FG), ("Create QR Code", FG), ("Close Link", RED5)]):
        if i == 0:
            c.box(mx + 4, my + 4, mw - 8, 32, MUTED, None, 4)
        c.t(mx + 12, my + 4 + 21 + 32 * i, lab, 14, col)
    c.h = my + mh + 20
    finish(c, f"{OT}/payment-links-row-menu-and-qr.svg")


def pl_qr():
    c = K(560, 700)
    c.box(0, 0, 560, 700, "#000", None, 0, op=0.5)
    dw, x, y = 512, 24, 24
    dh = 624
    c.box(x, y, dw, dh, BG, "#fff", 10, BORDER_OP)
    ix = x + 24
    iw = dw - 48
    c.t(ix, y + 24 + 24, "Payment Link Details", 24, FG, 700)
    c.icon("x", x + dw - 16 - 16, y + 16, 16, FG, op=0.7)
    yy = y + 24 + 30 + 16
    c.box(ix, yy, iw, 76, MUTED, "#a1a1a1", 10, 0.05)
    c.t(ix + iw / 2, yy + 12 + 15, "VIP Table", 14, FG, 500, "middle")
    c.t(ix + iw / 2, yy + 12 + 20 + 4 + 21, "512.50 USD", 18, FG, 700, "middle")
    yy += 76 + 16
    qh = 12 + 20 + 12 + 200 + 8 + 36 + 12
    c.box(ix, yy, iw, qh, MUTED, "#a1a1a1", 10, 0.05)
    c.t(ix + iw / 2, yy + 12 + 15, "QR Code for payment", 14, FG, 500, "middle")
    qx = ix + (iw - 200) / 2
    c.qr(qx, yy + 12 + 20 + 12, 200)
    c.button(qx, yy + 12 + 20 + 12 + 200 + 8, 200, "Download QR Code", "outline")
    yy += qh + 16
    c.line(ix, yy + 10, ix + (iw - 120) / 2 - 40, yy + 10, "#fff", 0.1)
    c.t(ix + iw / 2, yy + 15, "Payment URL", 14, FG, 500, "middle")
    c.line(ix + (iw + 120) / 2 + 40, yy + 10, ix + iw, yy + 10, "#fff", 0.1)
    yy += 20 + 16
    c.field(ix, yy, iw - 44, "https://pay.example.com/l/8f3k2q", disabled=True)
    c.button(ix + iw - 36, yy, 36, "", "secondary", icon="copy", h=36)
    yy += 36 + 16
    c.button(ix + iw / 4, yy, iw / 2, "Close", "secondary")
    c.h = y + dh + 24
    c.parts[1] = c.parts[1]
    finish(c, f"{OT}/payment-links-row-menu-and-qr-qr.svg")



if __name__ == "__main__":
    concepts_ticket_table()
    concepts_release_chain()
    concepts_how_fees()
    tm_overview()
    tm_edit_panel()
    tm_release_panel()
    tm_tier_messages()
    tm_create_addon()
    tm_addons_table()
    comp_list()
    comp_single()
    comp_bulk()
    comp_csv()
    report_cards()
    report_filters()
    report_table()
    pl_list()
    pl_create()
    pl_menu()
    pl_qr()
