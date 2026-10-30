"""Onsite Operations illustrations, group D: command center, cashless, cases, guests.

Every label is the en.json string (onsiteConsole / onsiteGuests / onsiteCases / onsiteCashless /
onsiteOps); server-built sentences come from plvr/internal/business/services/onsite_ops_*.go.
All names, amounts and references are made up.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from onsite_kit import *  # noqa: F401,F403,E402
from onsite_kit import K, tw, wrap, MFG, FG, BTN, DARK, CARD, BG, BORDER_CARD, MUTED, INPUT_BG, INPUT_BORDER  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "onsite")
M = 28
RED, AMBER = "#ef4444", "#f59e0b"


def out(name):
    os.makedirs(OUT, exist_ok=True)
    return os.path.join(OUT, name + ".svg")


def marks(k, items):
    for x, y, n in items:
        k.callout(x, y, n)


def ring(k, x, y, w, h, r=12):
    k.ring(x - 4, y - 4, w + 8, h + 8, r)


# ---------------------------------------------------------------- shared pieces
def queue_row(k, x, y, w, title, desc, pills, wait, wrap_desc=None, h=None):
    """One attention-queue row. pills: list of (label, tone, upper)."""
    rx = x + w - 12
    k.icon("arrow-right", rx - 16, y + (h or 64) / 2 - 8, 16, MFG)
    rx -= 28
    k.t(rx, y + (h or 64) / 2 + 5, wait, 13, MFG, 400, "end")
    rx -= 64 + 6
    for label, tone, upper in reversed(pills):
        pw = k.pill(rx, y + (h or 64) / 2 - 12, label, tone, upper, anchor="end")
        rx -= pw + 6
    return rx


def attention_rows(k, x, y, w, rows, desc_w):
    for title, desc, pills, wait in rows:
        dl = wrap(desc, desc_w, 13)
        h = 16 + 20 + len(dl) * 17 + 2
        k.box(x, y, w, h, CARD, BORDER_CARD, 8)
        k.t(x + 12, y + 28, title, 14, FG, 500)
        k.lines(x + 12, y + 47, dl, 13, MFG, lh=17)
        queue_row(k, x, y, w, title, desc, pills, wait, h=h)
        y += h + 8
    return y


# ---------------------------------------------------------------- command center
def command_center_overview():
    W, H = 916, 576
    k = K(W, H)
    cw = 860
    y = k.header(M, M, cw, "Onsite Operations", "Neon Nights · Oct 30, 2026 · Tap event", action="+ New service case")
    # search
    sy = 108
    k.box(M, sy, cw, 56, BG, "#7b5e9d", 10, sw=2)
    k.icon("search", M + 16, sy + 18, 20, BTN)
    k.t(M + 48, sy + 34, "Search Ticket ID, email, wristband, order number, payment or top-up reference…", 15, MFG)
    k.button(M + cw - 12, sy + 12, "Search", "default", h=32, disabled=True, anchor="end", size=14)
    k.t(M, sy + 80, "One box, any identifier — the type is detected for you. Three characters minimum.", 13, MFG)
    # stat cards
    cy = 208
    gap = 16
    cwid = (cw - 3 * gap) / 4
    cards = [
        ("Open service cases", "3", ["1 waiting on review"], "warn"),
        ("Blocked from entry", "12", ["8 cases closed · 75%", "settled at the desk"], "bad"),
        ("Unresolved top-ups", "2", ["1 expired — re-check", "with the provider"], "bad"),
        ("Average time to close", "4m 30s", ["Across 8 closed cases.", "Mean, not median."], "neutral"),
    ]
    for i, (lab, val, foot, tone) in enumerate(cards):
        k.stat(M + i * (cwid + gap), cy, cwid, 112, lab, val, foot, tone)
    # panels
    py = 336
    lw, rw = 560, 284
    k.panel(M, py, lw, 260, "Attention queue", "3 of 3 open cases", "View all")
    attention_rows(k, M + 16, py + 62, lw - 32, [
        ("Topup not credited", "Waiting on review (payment_review) for 18 min.",
         [("Payment review", "neutral", False), ("High", "bad", True)], "18 min"),
        ("Ticket not found", 'Nobody identified yet — raised 9 min ago against "NN-4821".',
         [("Unmatched", "warn", False), ("Medium", "warn", True)], "9 min"),
    ], 215)
    rx = M + lw + 16
    k.panel(rx, py, rw, 260, "Workspaces")
    items = [("ticket", "Tickets & Entry", "Blocked tickets, grouped by reason"),
             ("radio", "Wristbands", "Bindings, freezes and ownership"),
             ("wallet", "Cashless", "Money collected, credited and spent")]
    yy = py + 60
    for ic, lab, det in items:
        k.icon(ic, rx + 20, yy + 4, 16, MFG)
        k.t(rx + 48, yy + 15, lab, 14, FG, 500)
        dl = wrap(det, 175, 13)
        k.lines(rx + 48, yy + 33, dl, 13, MFG, lh=17)
        k.icon("arrow-right", rx + rw - 36, yy + 4, 16, MFG)
        yy += 36 + len(dl) * 17 + 6
    k.fade(H - 60, 60)
    ring(k, M, sy, cw, 56)
    ring(k, M, cy, cw, 112)
    ring(k, M, py, lw, 240)
    ring(k, rx, py, rw, 240)
    marks(k, [(M - 4, sy - 4, 1), (M - 4, cy - 4, 2), (M - 4, py - 4, 3), (rx - 4, py - 4, 4)])
    k.save(out("onsite-command-center-overview"))


def command_center_queue():
    W, H = 816, 436
    k = K(W, H)
    pw = 760
    k.panel(M, M, pw, 380, "Attention queue", "4 of 4 open cases", "View all",
            footer="Risk is separate from case state. Ordered by risk, then by how long someone has been waiting.")
    attention_rows(k, M + 16, M + 62, pw - 32, [
        ("Entry dispute", "Waiting on review (identity_dispute) for 1h 5m.",
         [("Identity dispute", "neutral", False), ("High", "bad", True)], "1h 5m"),
        ("Topup not credited", "Waiting on review (payment_review) for 18 min.",
         [("Payment review", "neutral", False), ("High", "bad", True)], "18 min"),
        ("Ticket not found", 'Nobody identified yet — raised 9 min ago against "NN-4821".',
         [("Unmatched", "warn", False), ("Medium", "warn", True)], "9 min"),
        ("Wristband lost or stolen", "Open for 4 min.", [("Normal", "neutral", True)], "4 min"),
    ], 330)
    k.save(out("onsite-command-center-attention-queue"))


def command_center_alerts():
    W, H = 616, 330
    k = K(W, H)
    pw = 560
    k.note(M, M, pw, "warn", "Operational health: Degraded",
              ["1 station or method is producing repeat failures."], h=76)
    y = M + 92
    k.panel(M, y, pw, 180, "Floor alerts", "Clustered failures, not individual cases")
    by = y + 48 + 20
    k.vline(M + 17, by - 4, by + 94, AMBER, 2)
    k.t(M + 30, by + 12, "3 unresolved top-ups at Gate A Top-up (Card terminal)", 14, FG, 500)
    det = wrap("3 top-ups unresolved at Gate A Top-up using Card terminal. Several at once points at a fault there "
               "rather than 3 separate participant problems — stop using that method and handle these together.",
               510, 13)
    yy = k.lines(M + 30, by + 32, det, 13, MFG, lh=17)
    k.t(M + 30, yy + 4, "Stop using that method at that station and handle these together.", 13, FG, 500)
    k.save(out("onsite-command-center-floor-alerts"))


# ---------------------------------------------------------------- guests
def guests_list():
    W, H = 916, 330
    k = K(W, H)
    cw = 860
    # search row
    y = M
    sw = cw - 130 - 180 - 16
    k.box(M, y, sw, 36, INPUT_BG, INPUT_BORDER, 8)
    k.icon("search", M + 12, y + 10, 16, MFG)
    k.t(M + 36, y + 23, "Name or email", 14, MFG)
    k.button(M + sw + 8, y, "Search", "outline", w=76)
    k.button(M + cw, y, "Add an approved guest", "cta", anchor="end")
    # table
    ty = y + 56
    cols = [16, 300, 560, 720]
    k.box(M, ty, cw, 42 + 52 + 52 + 104, BG, BORDER_CARD, 8)
    k.box(M + 1, ty + 1, cw - 2, 40, "#141414", None, 7)
    k.t(M + 16, ty + 26, "Name", 14, FG, 500)
    k.t(M + 300, ty + 26, "Email", 14, FG, 500)
    k.t(M + 560, ty + 26, "Entry", 14, FG, 500)
    rows = [("Alex Chen", "alex@example.com", "Checked in", "Undo check-in", None),
            ("Sam Rivera", "sam@example.com", "Not checked in", "Check in", None),
            ("Jordan Lee", "—", "Not checked in", "Check in",
             "More than one guest has this name. Confirm with an email or the company they came with before admitting anyone.")]
    ry = ty + 42
    rh = [52, 52, 104]
    for (name, mail, entry, btn, warn), h in zip(rows, rh):
        k.hline(M, M + cw, ry)
        k.t(M + 16, ry + 28, name, 14, FG, 500)
        if warn:
            k.icon("alert", M + 16, ry + 38, 13, "#fbbf24")
            wl = wrap(warn, 225, 13)
            k.lines(M + 34, ry + 50, wl, 13, "#fbbf24", lh=16)
        k.t(M + 300, ry + 28, mail, 14, FG)
        k.t(M + 560, ry + 28, entry, 14, FG)
        k.button(M + 720, ry + 8, btn, "outline", h=32, size=14)
        ry += h
    k.t(M, ry + 28, "1–3 of 3", 14, MFG)
    k.button(M + cw - 66, ry + 10, "Previous", "outline", h=32, w=80, disabled=True, anchor="end")
    k.button(M + cw, ry + 10, "Next", "outline", h=32, w=58, disabled=True, anchor="end")
    # callouts
    ring(k, M, y, sw, 36, 10)
    marks(k, [(M - 4, y - 4, 1)])
    wy = ty + 42 + 52 + 52 + 34
    ring(k, M + 12, wy, 270, 4 * 16 + 6, 8)
    marks(k, [(M + 12 + 270 + 4, wy + 4 * 16 + 10, 2)])
    for i, lab in enumerate(["Undo check-in", "Check in"]):
        bw = tw(lab, 14, 600) + 32
        ring(k, M + 720, ty + 42 + 52 * i + 8, bw, 32, 10)
    marks(k, [(M + 720 + tw("Undo check-in", 14, 600) + 36, ty + 42 + 4, 3)])
    k.h = ry + 60
    k.parts[0] = k.parts[0].replace(f'height="{H}"', f'height="{k.h}"')
    k.save(out("onsite-guests-list"))


def drawer(k, x, y, w, h, title, footer_buttons):
    k.box(x, y, w, h, BG, "#2a2a2a", 0)
    k.t(x + 20, y + 36, title, 18, FG, 600)
    # footer
    k.hline(x, x + w, y + h - 76, "#262626")
    bw = (w - 40 - 12) / 2
    k.button(x + 20, y + h - 56, footer_buttons[0][0], "outline", w=bw, disabled=footer_buttons[0][1])
    k.button(x + 20 + bw + 12, y + h - 56, footer_buttons[1][0], "cta", w=bw, disabled=footer_buttons[1][1])


def field(k, x, y, w, label, kind="input", value="", placeholder="", hint=None, rows=0, req=True, lines_val=()):
    k.label(x, y + 14, label, req)
    fy = y + 26
    if kind == "input":
        k.input(x, fy, w, value, placeholder)
        h = 36
    elif kind == "select":
        k.select(x, fy, w, value, placeholder)
        h = 36
    else:
        h = rows
        k.textarea(x, fy, w, h, lines_val, wrap(placeholder, w - 24, 14) if placeholder else ())
    yy = fy + h
    if hint:
        hl = wrap(hint, w, 13)
        yy = k.lines(x, yy + 18, hl, 13, MFG, lh=17) - 5
    return yy


def guests_add_form():
    W, H = 556, 520
    k = K(W, H, bg="#050505")
    dx, dw = M, 500
    k.h = H
    drawer(k, dx, 20, dw, 480, "Add an approved guest", [("Cancel", False), ("Add guest", False)])
    x, w = dx + 20, dw - 40
    y = 20 + 56 + 16
    y = field(k, x, y, w, "Full name", "input", "Taylor Kim", "As they'll give it at the door") + 20
    y = field(k, x, y, w, "Ticket type ID", "input", "1042", "Which ticket type this guest counts as",
              hint="From Ticket Management. A guest still counts against a ticket type.") + 20
    field(k, x, y, w, "Who approved this?", "input", "Approved by the promoter by phone, 20:15", "",
          hint="Stored with this action. Without it, nobody can tell afterwards whether this was authorised.")
    k.save(out("onsite-guests-add-approved-form"))


# ---------------------------------------------------------------- cashless
def attention_bar(k, x, y, w, count, noun, detail_lines, action):
    h = 24 + max(1, len(detail_lines)) * 20 + 8 if detail_lines else 56
    h = max(h, 64)
    k.box(x, y, w, h, "#1c0a0a", "#7f1d1d", 10)
    k.t(x + 16, y + h / 2 + 8, str(count), 24, "#fca5a5", 700)
    k.t(x + 16 + 22, y + h / 2 + 7, noun, 14, "#fecaca", 500)
    dx = x + 16 + 22 + tw(noun, 14, 500) + 24
    top = y + h / 2 - len(detail_lines) * 10 + 5
    for i, ln in enumerate(detail_lines):
        k.t(dx, top + i * 20 + 5, ln, 14, "#fca5a5")
    k.button(x + w - 16, y + h / 2 - 17, action, "danger", h=34, anchor="end")
    return h


def totals_strip(k, x, y, w, items):
    h = 82
    k.box(x, y, w, h, CARD, BORDER_CARD, 10)
    cw = w / 3
    for i, (lab, val, foot) in enumerate(items):
        cx = x + i * cw
        if i:
            k.vline(cx, y, y + h)
        k.t(cx + 12, y + 23, lab, 13, MFG)
        k.t(cx + 12, y + 47, val, 18, FG, 600)
        k.t(cx + 12, y + 66, foot, 13, MFG)
    return h


def money_pill(k, x, y, status, anchor="start"):
    lab = {"succeeded": "Completed", "pending": "Pending", "expired": "Expired", "failed": "Failed",
           "cancelled": "Cancelled"}.get(status, status)
    tone = {"succeeded": "good", "pending": "warn", "expired": "bad", "failed": "bad"}.get(status, "neutral")
    return k.pill(x, y, lab, tone, anchor=anchor)


def cashless_overview():
    W, H = 916, 566
    k = K(W, H)
    cw = 860
    k.header(M, M, cw, "Cashless", "Neon Nights · Oct 30, 2026", action="+ New service case")
    by = 108
    detail = ["The payment record says these were paid and the credit never landed. This is money",
              "owed — work these first, and credit each one only against the payment evidence."]
    dl = wrap("The payment record says these were paid and the credit never landed. This is money owed — work these "
              "first, and credit each one only against the payment evidence.", 470, 14)
    bh = max(64, 24 + len(dl) * 20)
    k.box(M, by, cw, bh, "#1c0a0a", "#7f1d1d", 10)
    k.t(M + 16, by + bh / 2 + 8, "2", 24, "#fca5a5", 700)
    k.t(M + 40, by + bh / 2 - 2, "top-ups", 14, "#fecaca", 500)
    k.t(M + 40, by + bh / 2 + 16, "unresolved", 14, "#fecaca", 500)
    k.lines(M + 160, by + bh / 2 - len(dl) * 10 + 15, dl, 14, "#fca5a5", lh=20)
    k.button(M + cw - 16, by + bh / 2 - 17, "Show 2", "danger", h=34, anchor="end")
    ty = by + bh + 14
    th = totals_strip(k, M, ty, cw, [
        ("Top-ups collected", "$12,480.00", "Online $9,230.00 · Onsite $3,250.00"),
        ("Still on wallets", "$4,120.00", "Across 86 wallets"),
        ("Vendor spend", "$8,360.00", "Onsite $2,940.00")])
    gy = ty + th + 16
    lw, rw = 560, 284
    k.panel(M, gy, lw, H - gy + 40, "Money ledger", "Every row keeps its own amount and the balance it left")
    # table header (columns condensed to fit the crop)
    hy = gy + 48
    k.box(M + 1, hy, lw - 2, 34, "#141414", None, 0)
    for x, lab, a in [(16, "Who", "start"), (150, "What", "start"), (250, "Status", "start"),
                      (440, "Amount", "end"), (516, "Balance", "end")]:
        k.t(M + x, hy + 22, lab, 13, MFG, 500, a)
    rx = M + lw + 16
    yy = k.panel(rx, gy, rw, H - gy + 40, "Needs attention · 2", "Grouped by meaning, not by status") + 18
    groups = [(RED, "1", "Paid, but the balance never went up",
               "The payment record says these were paid and the credit never landed. This is money owed — "
               "work these first, and credit each one only against the payment evidence."),
              (AMBER, "1", "Still waiting on confirmation",
               "Not yet settled either way. Don't credit a balance on the strength of one of these.")]
    for col, n, lab, det in groups:
        ll = wrap(lab, 205, 14, 500)
        dl = wrap(det, 205, 13)
        gh = len(ll) * 18 + 4 + len(dl) * 17
        k.vline(rx + 17, yy - 3, yy + gh + 2, col, 2)
        k.t(rx + 30, yy + 18, n, 20, FG, 700)
        e = k.lines(rx + 52, yy + 14, ll, 14, FG, 500, lh=18)
        k.lines(rx + 52, e + 1, dl, 13, MFG, lh=17)
        yy += gh + 24
    k.fade(H - 70, 70)
    ring(k, M, by, cw, bh)
    ring(k, rx, gy, rw, H - gy - 4)
    ring(k, M, ty, cw, th)
    marks(k, [(M - 4, by - 4, 1), (rx - 4, gy - 4, 2), (M - 4, ty - 4, 3)])
    k.save(out("onsite-cashless-overview"))


def ledger_row(k, x, y, w, h, who, mail, what, where, ref, status, link, amount, bal, when, since, stripe):
    cols = [174, 174, 116, 132, 124, 104, 36]
    if stripe:
        bg = {"bad": "#1d1010", "warn": "#1c1509"}[stripe]
        k.box(x, y, w, h, bg, None, 0)
        k.box(x, y, 4, h, {"bad": RED, "warn": AMBER}[stripe], None, 0)
    k.hline(x, x + w, y)
    cx = [x]
    for c in cols:
        cx.append(cx[-1] + c)
    k.t(cx[0] + 16, y + 26, who, 14, BTN, 500)
    k.t(cx[0] + 16, y + 44, mail, 13, MFG)
    k.t(cx[1] + 16, y + 26, what, 14, FG, 500)
    k.t(cx[1] + 16, y + 44, where, 13, MFG)
    if ref:
        k.t(cx[1] + 16, y + 62, ref, 12, FG, 400, mono=True)
        k.icon("copy", cx[1] + 16 + len(ref) * 7.2 + 6, y + 51, 13, MFG)
    money_pill(k, cx[2] + 16, y + 12, status)
    if link:
        k.t(cx[2] + 16, y + 52, "Investigate", 13, BTN)
    k.t(cx[4] - 16, y + 31, amount, 15, FG, 600, "end")
    k.t(cx[5] - 16, y + 31, bal, 14, MFG, 400, "end")
    k.t(cx[5] + 16, y + 26, when, 14, FG)
    k.t(cx[5] + 16, y + 44, since, 13, MFG)
    k.icon("chevron-right", cx[6] + 8, y + 17, 16, MFG)


def cashless_ledger():
    W, H = 916, 556
    k = K(W, H)
    cw = 860
    y = M
    # search + channel
    k.box(M, y, 384, 36, INPUT_BG, INPUT_BORDER, 8)
    k.t(M + 12, y + 23, "Email, name, reference, station or stall", 14, MFG)
    k.t(M, y + 54, "Takes whatever they can give you — you don't need the right kind of reference.", 13, MFG)
    gx = M + 384 + 12 + 4
    k.t(gx, y + 23, "Channel", 13, MFG, 500)
    bx = gx + 56
    for lab, sel in [("All", True), ("Online", False), ("Onsite", False)]:
        w = tw(lab, 14, 600) + 24
        k.button(bx, y + 2, lab, "default" if sel else "outline", h=32, w=w)
        bx += w + 6
    # type + unresolved
    y2 = y + 78
    k.t(M, y2 + 22, "Type", 13, MFG, 500)
    bx = M + 36
    for lab, sel in [("All", True), ("Top-up", False), ("Spend", False), ("Refund", False), ("Adjustment", False)]:
        w = tw(lab, 14, 600) + 24
        k.button(bx, y2 + 2, lab, "default" if sel else "outline", h=32, w=w)
        bx += w + 6
    k.button(bx + 12, y2 + 2, "Unresolved only", "outline", h=32)
    ring(k, M, y - 0, 384, 36, 10)
    fx0, fy0 = M, y
    k.ring(M - 6, y - 6, cw + 12, 78 + 40 + 12, 14)
    # ledger panel
    py = y2 + 52
    ph = 48 + 34 + 70 + 56 + 70 + 56 + 4
    k.box(M, py, cw, ph, CARD, BORDER_CARD, 10)
    k.t(M + 16, py + 30, "Money ledger", 16, FG, 600)
    k.t(M + cw - 16, py + 29, "Every row keeps its own amount and the balance it left", 13, MFG, 400, "end")
    k.hline(M, M + cw, py + 48)
    hy = py + 49
    k.box(M + 1, hy, cw - 2, 34, "#141414", None, 0)
    cols = [174, 174, 116, 132, 124, 104]
    cx = M
    for c, lab in zip(cols, ["Who", "What", "Status", "Amount", "Balance", "When"]):
        if lab in ("Amount", "Balance"):
            k.t(cx + c - 16, hy + 22, lab, 13, MFG, 500, "end")
        else:
            k.t(cx + 16, hy + 22, lab, 13, MFG, 500)
        cx += c
    ry = hy + 34
    ledger_row(k, M, ry, cw, 70, "Maya Patel", "maya@example.com", "Top-up", "PayCo · at Gate A Top-up",
               "pay_8F2K91", "expired", True, "+$30.00", "$0.00", "21:05", "12 min ago", "bad")
    ry += 70
    ledger_row(k, M, ry, cw, 56, "Sam Rivera", "sam@example.com", "Purchase", "at Neon Bar", None,
               "succeeded", False, "−$12.00", "$38.00", "21:11", "6 min ago", None)
    ry += 56
    ledger_row(k, M, ry, cw, 70, "Taylor Kim", "taylor@example.com", "Top-up", "PayCo",
               "pay_3D7Q42", "pending", True, "+$20.00", "$0.00", "21:14", "3 min ago", "warn")
    ry += 70
    ledger_row(k, M, ry, cw, 56, "Alex Chen", "alex@example.com", "Top-up", "at Gate B Top-up", None,
               "succeeded", False, "+$50.00", "$50.00", "21:15", "2 min ago", None)
    k.h = ry + 28
    k.parts[0] = k.parts[0].replace(f'height="{H}"', f'height="{k.h}"')
    # callout 2 (Investigate link on Expired row)
    marks(k, [(M - 4, y - 8, 1)])
    iy = hy + 34 + 42
    k.ring(M + 174 + 174 + 12, iy - 4, 100, 24, 8)
    k.callout(M + 174 + 174 + 12 + 112, iy + 8, 2)
    k.save(out("onsite-cashless-ledger"))


def layer_cards(k, x, y, w, cards):
    gap = 16
    cwid = (w - 2 * gap) / 3
    hmax = 0
    for i, (lab, val, foot, tone) in enumerate(cards):
        n = len(foot)
        hmax = max(hmax, 82 + n * 17 + 12)
    for i, (lab, val, foot, tone) in enumerate(cards):
        k.stat(x + i * (cwid + gap), y, cwid, hmax, lab, val, foot, tone)
    return hmax


def topup_investigation():
    W, H = 916, 790
    k = K(W, H)
    cw = 860
    hb = k.header(M, M, cw, "Top-up not reflected", "Online top-up · Oct 30, 9:05 PM", live=False)
    # right actions: Online pill + Add note
    bw = k.button(M + cw, M, "Add note", "cta-outline", anchor="end")
    k.pill(M + cw - bw - 8, M + 6, "Online", "neutral", anchor="end")
    y = hb + 14
    cwid = (cw - 32) / 3
    pay = wrap("Our payment record for pay_3D7Q42 says unpaid, last updated 2026-10-30T21:07:00Z. That is what we "
               "recorded, not a fresh answer from the provider — if the participant has a statement line showing a "
               "charge, treat their evidence as the stronger one.", cwid - 32, 13)
    ent = wrap("Still unconfirmed. Do not add balance again while this is unresolved — that double-credits.",
               cwid - 32, 13)
    bal = wrap("No balance was added for this top-up.", cwid - 32, 13)
    hmax = 82 + max(len(pay), len(ent), len(bal)) * 17 + 8
    cards = [("1 · Stripe", "unpaid", pay, "neutral"), ("2 · Top-up entry", "Pending", ent, "warn"),
             ("3 · Wallet balance", "$0.00", bal, "neutral")]
    for i, (lab, val, foot, tone) in enumerate(cards):
        k.stat(M + i * (cwid + 16), y, cwid, hmax, lab, val, foot, tone)
    ring(k, M, y, cw, hmax, 12)
    k.callout(M - 4, y - 4, 1)
    py = y + hmax + 20
    # reconciliation panel
    ph = 48 + 34 + 3 * 74 + 110 - 10
    k.box(M, py, cw, ph, CARD, BORDER_CARD, 10)
    k.t(M + 16, py + 30, "Reconciliation", 16, FG, 600)
    k.t(M + cw - 16, py + 29, "Three layers must agree", 13, MFG, 400, "end")
    k.hline(M, M + cw, py + 48)
    hy = py + 49
    k.box(M + 1, hy, cw - 2, 34, "#141414", None, 0)
    c1, c2 = M + 16, M + 200
    c3 = M + 330
    k.t(c1, hy + 22, "Layer", 13, MFG, 500)
    k.t(c2, hy + 22, "State", 13, MFG, 500)
    k.t(c3, hy + 22, "What it is based on", 13, MFG, 500)
    ry = hy + 34
    rows = [("Payment provider", ("unpaid", "neutral"), pay_detail := wrap(
        "Our payment record for pay_3D7Q42 says unpaid, last updated 2026-10-30T21:07:00Z. That is what we recorded, "
        "not a fresh answer from the provider — if the participant has a statement line showing a charge, treat "
        "their evidence as the stronger one.", cw - 330 - 16 + 16, 14)),
            ("Top-up entry", ("Pending", "warn"), wrap(
                "Still unconfirmed. Do not add balance again while this is unresolved — that double-credits.",
                cw - 330 - 16 + 16, 14)),
            ("Wallet balance", ("not_credited", "neutral"), wrap("No balance was added for this top-up.",
                                                                  cw - 330 - 16 + 16, 14))]
    for name, (st, tone), det in rows:
        h = max(24 + 20 * len(det), 52)
        k.hline(M, M + cw, ry)
        k.t(c1, ry + 28, name, 14, FG, 500)
        k.pill(c2, ry + 12, st, tone)
        k.lines(c3, ry + 28, det, 14, MFG, lh=20)
        ry += h
    k.hline(M + 16, M + cw - 16, ry + 8)
    k.t(M + 16, ry + 36, "Where it broke", 14, FG, 600)
    dg = wrap("Money may have been taken but the balance was not credited. Do not add balance again until the payment "
              "is confirmed.", cw - 32, 14)
    ye = k.lines(M + 16, ry + 58, dg, 14, MFG, lh=20)
    ph_real = ye - py + 12
    # patch panel height
    k.parts[[i for i, p in enumerate(k.parts) if f'y="{py}"' in p and 'width="860"' in p][0]] = (
        f'<rect x="{M}" y="{py}" width="{cw}" height="{ph_real}" rx="10" fill="{CARD}" stroke="{BORDER_CARD}" stroke-width="1"/>')
    ring(k, M, py, cw, ph_real, 12)
    k.callout(M - 4, py - 4, 2)
    ring(k, M + 8, ry + 14, cw - 16, ye - ry - 6, 8)
    k.callout(M + 4, ry + 12, 3)
    k.h = int(py + ph_real + 28)
    k.parts[0] = k.parts[0].replace(f'height="{H}"', f'height="{k.h}"')
    k.save(out("onsite-cashless-topup-investigation"))


def transaction_detail():
    W, H = 916, 560
    k = K(W, H)
    cw = 860
    y = M
    bh = 168
    k.box(M, y, cw, bh, CARD, BORDER_CARD, 10)
    pw_ = money_pill(k, M + 16, y + 14, "succeeded")
    k.t(M + 16 + pw_ + 10, y + 31, "Purchase · at Neon Bar", 14, MFG)
    k.t(M + 16, y + 70, "−$25.00", 30, FG, 700)
    k.t(M + 16, y + 94, "Oct 30, 9:41 PM · 22 min ago", 14, MFG)
    cx = M + 400
    for lab, val, x in [("Balance after", "$25.00", cx), ("Balance now", "$33.00", cx + 130)]:
        k.t(x, y + 40, lab, 13, MFG)
        k.t(x, y + 62, val, 18, FG, 600)
    px = cx + 270
    k.t(px, y + 40, "Participant", 13, MFG)
    k.t(px, y + 62, "Alex Chen", 14, BTN, 500)
    k.t(px, y + 82, "alex@example.com", 12, FG, 400, mono=True)
    k.icon("copy", px + 16 * 7.2 + 8, y + 71, 13, MFG)
    k.hline(M + 16, M + cw - 16, y + 108)
    sl = wrap("A purchase, part or all of which has already been refunded. Check the refunded quantity on each line "
              "before agreeing to refund anything again.", cw - 32, 14)
    k.lines(M + 16, y + 132, sl, 14, FG, lh=20)
    ring(k, M, y, cw, bh)
    k.callout(M - 4, y - 4, 1)
    # left: What was bought
    py = y + bh + 16
    lw = 560
    k.box(M, py, lw, 330, CARD, BORDER_CARD, 10)
    left_box = len(k.parts) - 1
    k.t(M + 16, py + 30, "What was bought", 16, FG, 600)
    k.t(M + lw - 16, py + 29, "at Neon Bar · order status: completed", 13, MFG, 400, "end")
    k.hline(M, M + lw, py + 48)
    cy = py + 64
    body = wrap("$8.00 of this order has already been refunded. Check the refunded column before agreeing to "
                "anything further.", lw - 32 - 32, 14)
    ch = 22 + 22 + len(body) * 20
    k.note(M + 16, cy, lw - 32, "warn", "Partly refunded already", body, h=ch)
    ty = cy + ch + 12
    k.box(M + 1, ty, lw - 2, 34, "#141414", None, 0)
    xs = {"Item": M + 16, "Qty": M + 270, "Unit": M + 350, "Line total": M + 450, "Refunded": M + lw - 16}
    for lab, x in xs.items():
        k.t(x, ty + 22, lab, 13, MFG, 500, "start" if lab == "Item" else "end")
    ry = ty + 34
    for item, q, u, lt, rf in [("Draft beer", "2", "$8.00", "$16.00", "1 of 2"), ("Nachos", "1", "$9.00", "$9.00", "—")]:
        k.hline(M, M + lw, ry)
        k.t(M + 16, ry + 26, item, 14, FG, 500)
        k.t(M + 270, ry + 26, q, 14, FG, 400, "end")
        k.t(M + 350, ry + 26, u, 14, FG, 400, "end")
        k.t(M + 450, ry + 26, lt, 14, FG, 500, "end")
        k.t(M + lw - 16, ry + 26, rf, 14, FG if rf != "—" else MFG, 500, "end")
        ry += 40
    k.box(M, ry, lw, 40, "#1b1b1b", None, 0)
    k.hline(M, M + lw, ry)
    k.t(M + 16, ry + 26, "Order total", 14, FG, 500)
    k.t(M + 450, ry + 26, "$25.00", 14, FG, 500, "end")
    k.t(M + lw - 16, ry + 26, "$8.00", 14, MFG, 500, "end")
    k.parts[left_box] = (f'<rect x="{M}" y="{py}" width="{lw}" height="{ry + 40 + 14 - py}" rx="10" fill="{CARD}" '
                         f'stroke="{BORDER_CARD}" stroke-width="1"/>')
    k.h = int(ry + 40 + 14 + 28)
    k.parts[0] = k.parts[0].replace(f'height="{H}"', f'height="{k.h}"')
    ring(k, M + lw - 100, ty, 96, 34 + 80 + 40, 6)
    k.callout(M + lw - 98, ty - 6, 2)
    # right: Record + What you can do
    rx = M + lw + 16
    rw = cw - lw - 16
    k.box(rx, py, rw, 118, CARD, BORDER_CARD, 10)
    k.t(rx + 16, py + 30, "Record", 16, FG, 600)
    k.hline(rx, rx + rw, py + 48)
    k.t(rx + 16, py + 76, "Provider", 14, MFG)
    k.t(rx + rw - 16, py + 76, "Not recorded", 14, FG, 400, "end")
    k.hline(rx, rx + rw, py + 86)
    k.t(rx + 16, py + 109, "Reference", 14, MFG)
    k.t(rx + rw - 16 - 24, py + 109, "ent_7Q2M41", 12, FG, 400, "end", mono=True)
    k.icon("copy", rx + rw - 16 - 14, py + 98, 13, MFG)
    wy = py + 134
    k.box(rx, wy, rw, 330, CARD, BORDER_CARD, 10)
    k.t(rx + 16, wy + 30, "What you can do", 16, FG, 600)
    k.hline(rx, rx + rw, wy + 48)
    sy = wy + 48
    steps = [("Go through the items with them",
              "Each line shows what was charged and how much of it has already been refunded, so a disagreement is "
              "about one item rather than the whole order."),
             ("Confirm with Neon Bar",
              "The stall can be quoted the order reference or the transaction id. A refund for goods not received is "
              "the vendor's call and cannot be made from this console.")]
    for lab, det in steps:
        k.hline(rx, rx + rw, sy)
        k.t(rx + 16, sy + 26, lab, 14, FG, 500)
        dl = wrap(det, rw - 32, 13)
        yy = k.lines(rx + 16, sy + 45, dl, 13, MFG, lh=17)
        sy = yy + 8
    ring(k, rx, wy, rw, 280, 12)
    k.callout(rx - 4, wy - 4, 3)
    k.fade(k.h - 60, 60, rw + 20, rx - 4)
    k.save(out("onsite-cashless-transaction-detail"))


# ---------------------------------------------------------------- cases
def cases_list():
    W, H = 916, 470
    k = K(W, H)
    cw = 860
    y = k.header(M, M, cw, "Service cases", "Neon Nights · Oct 30, 2026",
                 "Every problem raised at the desk, and whether it reached a conclusion.")
    fy = y + 14
    x = M
    for lab, sel in [("Still open", False), ("Resolved", False), ("Product gaps", False), ("Everything", True),
                     ("Nobody identified yet", False)]:
        w = tw(lab, 14, 600) + 24
        k.button(x, fy, lab, "default" if sel else "outline", h=32, w=w)
        x += w + 8
    fw = x - 8 - M
    k.button(M + cw, fy, "Record a case", "cta", anchor="end")
    ring(k, M, fy, fw, 32, 10)
    k.callout(M - 4, fy - 4, 1)
    ty = fy + 52
    cols = [0, 200, 380, 520, 670]
    rows = [("Topup not credited", "Alex Chen", None, "Open", None, "—", "Oct 30, 2026, 9:05 PM"),
            ("Entry dispute", "Maya Patel", None, "Sent for review", None, "Identity dispute", "Oct 30, 2026, 8:40 PM"),
            ("Ticket not found", None, "“NN-4821”", "Open", None, "—", "Oct 30, 2026, 8:56 PM"),
            ("Vendor not delivered", "Sam Rivera", None, "Sent for review", "Needs the payment provider",
             "Payment review", "Oct 30, 2026, 8:15 PM"),
            ("Duplicate payment", "Jordan Lee", None, "Resolved", None, "—", "Oct 30, 2026, 7:30 PM")]
    hts = [50, 50, 66, 66, 50]
    th = 40 + sum(hts)
    k.box(M, ty, cw, th, BG, BORDER_CARD, 8)
    k.box(M + 1, ty + 1, cw - 2, 38, "#141414", None, 7)
    for c, lab in zip(cols, ["Problem", "Who", "Status", "Review", "Raised"]):
        k.t(M + c + 16, ty + 26, lab, 14, FG, 500)
    ry = ty + 40
    for (prob, who, ident, st, sub, rev, when), h in zip(rows, hts):
        k.hline(M, M + cw, ry)
        k.t(M + 16, ry + 29, prob, 14, BTN, 500)
        if who:
            k.t(M + cols[1] + 16, ry + 29, who, 14, BTN)
        else:
            k.t(M + cols[1] + 16, ry + 29, "Nobody identified", 14, MFG)
            k.t(M + cols[1] + 16, ry + 47, ident, 12, FG, 400, mono=True)
        k.t(M + cols[2] + 16, ry + 29, st, 14, FG)
        if sub:
            k.t(M + cols[2] + 16, ry + 47, sub, 13, MFG)
        k.t(M + cols[3] + 16, ry + 29, rev, 14, FG)
        k.t(M + cols[4] + 16, ry + 29, when, 14, FG)
        ry += h
    ring(k, M, ty, cw, th, 12)
    k.callout(M - 4, ty - 4, 2)
    k.h = ry + 56
    k.t(M, ry + 28, "1–5 of 5", 14, MFG)
    k.button(M + cw - 66, ry + 10, "Previous", "outline", h=32, w=80, disabled=True, anchor="end")
    k.button(M + cw, ry + 10, "Next", "outline", h=32, w=58, disabled=True, anchor="end")
    k.parts[0] = k.parts[0].replace(f'height="{H}"', f'height="{k.h}"')
    k.save(out("onsite-cases-list"))


def cases_record_form():
    W, H = 556, 800
    k = K(W, H, bg="#050505")
    dx, dw = M, 500
    drawer(k, dx, 20, dw, H - 40, "Record a service case", [("Cancel", False), ("Record case", False)])
    x, w = dx + 20, dw - 40
    y = 20 + 56 + 14
    il = wrap("A case records what happened and how it was concluded. Nothing is assigned or timed — it just makes "
              "sure this problem ends with an answer.", w, 14)
    y = k.lines(x, y + 12, il, 14, MFG, lh=20) + 14
    y = field(k, x, y, w, "What kind of problem?", "select", "Topped up but balance didn't go up", "",
              hint="If this needs escalating, it will go to Payment review.") + 18
    y = field(k, x, y, w, "What did they show you?", "input", "NN-4821", "",
              hint="Copy it exactly — don’t correct the spelling or capitalisation. What they actually presented is the record.") + 18
    y = field(k, x, y, w, "What did they say?", "area", "", "In their words, as far as you can.", rows=70, req=False,
              lines_val=("“I paid twice and nothing showed up.”",)) + 18
    field(k, x, y, w, "What happened at the desk?", "area", "", "What you checked, what you found, and what you couldn’t do.",
          rows=96, lines_val=("Checked the ledger for alex@example.com. The top-up",
                              "shows as pending and the balance is unchanged.",
                              "Could not credit it from the desk."))
    k.save(out("onsite-cases-record-form"))


def case_detail():
    W, H = 916, 700
    k = K(W, H)
    cw = 860
    y = M
    # header excerpt: title row
    k.t(M, y + 30, "Topup not credited", 30, FG, 700)
    k.t(M, y + 56, "Alex Chen · Oct 30, 2026, 9:05 PM", 14, MFG)
    k.t(M, y + 77, "The desk could not safely act, so it has gone to a reviewer with a stated conclusion type.", 14, MFG)
    bw = k.button(M + cw, y, "Add evidence", "outline", anchor="end")
    k.pill(M + cw - bw - 8, y + 6, "Sent for review", "warn", anchor="end")
    # flow
    fy = y + 98
    fh = 240
    k.box(M, fy, cw, fh, CARD, BORDER_CARD, 10)
    k.t(M + 16, fy + 30, "Case state flow", 16, FG, 600)
    k.t(M + cw - 16, fy + 29, "Five states · three mutually exclusive end states", 13, MFG, 400, "end")
    k.hline(M, M + cw, fy + 48)
    ny = fy + 76
    # node: open (done)
    n1x, n2x = M + 80, M + 80 + 40 + 56 + 110
    k.dot(n1x, ny, 14, BTN)
    k.icon("check", n1x - 8, ny - 8, 16, "#fff", 2.5)
    k.vline(0, 0, 0)
    k.parts.append(f'<rect x="{n1x + 14 + 6}" y="{ny - 1}" width="{n2x - n1x - 40}" height="2" fill="{BTN}"/>')
    k.parts.append(f'<circle cx="{n2x}" cy="{ny}" r="13" fill="none" stroke="{BTN}" stroke-width="2"/>')
    k.dot(n2x, ny, 5, BTN)
    k.t(n1x, ny + 32, "Open", 14, FG, 400, "middle")
    k.lines(n1x, ny + 49, ["Recorded at the", "service desk"], 12, MFG, lh=14)
    k.t(n2x, ny + 32, "Sent for review", 14, FG, 400, "middle")
    k.lines(n2x, ny + 49, ["Escalated · awaiting", "a business", "conclusion"], 12, MFG, lh=14)
    # end states
    ex = M + 480
    k.vline(ex - 24, fy + 62, fy + fh - 52)
    ey = fy + 62
    for lab, mean in [("Resolved", "The participant received a result."),
                      ("Could not be resolved", "Reason recorded, and logged as a product gap."),
                      ("Cancelled", "Withdrawn or a duplicate.")]:
        k.dot(ex, ey + 12, 5, "#3a3a3a")
        k.t(ex + 16, ey + 12, lab, 14, FG)
        k.t(ex + 16, ey + 30, mean, 13, MFG)
        ey += 44
    k.hline(M, M + cw, fy + fh - 38)
    k.t(M + 16, fy + fh - 14, "These five states are the complete set. A case never leaves this diagram.", 13, MFG)
    ring(k, M, fy, cw, fh, 12)
    k.callout(M - 4, fy - 4, 1)
    # break
    by = fy + fh + 12
    for i in range(3):
        k.dot(M + cw / 2 - 12 + i * 12, by + 6, 2, "#555")
    # evidence
    ey0 = by + 34
    k.t(M, ey0 + 18, "Evidence", 16, FG, 600)
    k.button(M + cw, ey0, "Add evidence", "outline", h=32, anchor="end")
    iy = ey0 + 42
    k.box(M, iy, cw, 84, BG, BORDER_CARD, 8)
    k.t(M + 12, iy + 22, "REFERENCE NUMBER", 12, MFG, 500)
    k.t(M + 12, iy + 44, "pay_3D7Q42", 14, FG, 400, mono=True)
    k.t(M + 12, iy + 68, "Oct 30, 2026, 9:12 PM", 12, MFG)
    k.ring(M - 10, ey0 - 10, cw + 20, 42 + 84 + 14, 12)
    k.callout(M - 10, ey0 - 10, 2)
    # tried
    ty = iy + 84 + 38
    k.t(M, ty + 18, "What was tried", 16, FG, 600)
    ay = ty + 30
    k.box(M, ay, cw, 90, "#451a03", "#92400e", 8)
    k.t(M + 12, ay + 24, "Balance corrected — refused by the system", 14, "#fef3c7", 500)
    k.t(M + cw - 12, ay + 24, "Oct 30, 2026, 9:18 PM", 12, MFG, 400, "end")
    k.t(M + 12, ay + 45, "Reason: Station reconciliation", 14, MFG)
    k.t(M + 12, ay + 72, "By Sam Rivera", 12, MFG)
    k.ring(M - 10, ty - 10, cw + 20, 30 + 90 + 20, 12)
    k.callout(M - 10, ty - 10, 3)
    # conclude
    cy = ay + 90 + 38
    k.t(M, cy + 18, "Conclude this case", 16, FG, 600)
    x = M
    for lab in ["Close as resolved", "Conclude: cannot be resolved", "Cancel this case"]:
        w = k.button(x, cy + 32, lab, "outline")
        x += w + 8
    k.ring(M - 10, cy - 10, x - M + 12, 82, 12)
    k.callout(M - 10, cy - 10, 4)
    k.h = cy + 90
    k.parts[0] = k.parts[0].replace(f'height="{H}"', f'height="{k.h}"')
    k.save(out("onsite-case-detail-page"))


def case_evidence_dialog():
    W, H = 556, 470
    k = K(W, H, bg="#050505")
    dx, dw = M, 500
    drawer(k, dx, 20, dw, H - 40, "Add evidence", [("Cancel", False), ("Add", False)])
    x, w = dx + 20, dw - 40
    y = 20 + 56 + 14
    y = field(k, x, y, w, "Kind", "select", "Named confirmation", "", req=False) + 18
    field(k, x, y, w, "What was confirmed, and by whom?", "area", "", "", rows=96,
          lines_val=("Duty manager Sam Rivera confirmed the cash was", "taken at station 3."),
          hint="Your name is recorded with this. Verbal agreement on its own isn't evidence.")
    k.save(out("onsite-case-add-evidence-dialog"))


def case_conclude_buttons():
    W, H = 880, 480
    k = K(W, H)
    # left: section
    x = M
    k.t(x, M + 20, "Conclude this case", 16, FG, 600)
    bx, by = x, M + 36
    w1 = k.button(bx, by, "Send for review", "outline")
    w2 = k.button(bx + w1 + 8, by, "Close as resolved", "outline")
    k.button(bx, by + 44, "Cancel this case", "outline")
    k.ring(bx - 4, by - 4, w1 + 8 + 4, 44, 10)
    # right: drawer, with select open
    dx, dw = 372, 480
    drawer(k, dx, 20, dw, H - 40, "Send for review", [("Cancel", False), ("Confirm", True)])
    k.vline(dx + w1 * 0, 0, 0)
    ix, iw = dx + 20, dw - 40
    y = 20 + 56 + 14
    ml = wrap("The desk could not safely act, so it has gone to a reviewer with a stated conclusion type.", iw, 14)
    y = k.lines(ix, y + 12, ml, 14, MFG, lh=20) + 14
    k.label(ix, y + 14, "What kind of review?", True)
    k.select(ix, y + 26, iw, "", "Choose the conclusion type")
    # dropdown
    oy = y + 26 + 40
    opts = ["Identity dispute", "Payment review", "Ticket entitlement review", "Operational incident"]
    k.box(ix, oy, iw, 8 + 4 * 32, "#171717", "#303030", 8)
    for i, o in enumerate(opts):
        yy = oy + 4 + i * 32
        if i == 1:
            k.box(ix + 4, yy, iw - 8, 32, "#262626", None, 6)
        k.t(ix + 14, yy + 21, o, 14, FG)
    k.save(out("onsite-case-conclude-buttons"))


if __name__ == "__main__":
    for fn in [command_center_overview, command_center_queue, command_center_alerts, guests_list, guests_add_form,
               cashless_overview, cashless_ledger, topup_investigation, transaction_detail, cases_list,
               cases_record_form, case_detail, case_evidence_dialog, case_conclude_buttons]:
        fn()
    print("ok")
