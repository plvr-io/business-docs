"""Illustrations for onsite/participants, onsite-staff, tickets, search, wristbands (Group E)."""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from onsite_b_kit import *  # noqa: F401,F403

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "onsite")


def save(c, name):
    c.save(os.path.join(OUT, name + ".svg"))


# ---------------------------------------------------------------- staff list
def staff_list():
    c = new(860, 424)
    X = 20
    # filter row
    T(c, X, 52, "Role", 14, FG, 500)
    select(c, X, 60, 180, "All Roles")
    T(c, X + 192, 52, "Search", 14, FG, 500)
    input_box(c, X + 192, 60, 220, placeholder="Search by login code")
    # right buttons
    w_add = btn_w("Add Staff", True)
    xa = 840 - w_add
    button(c, xa, 60, "Add Staff", "cta", ic="plus")
    w_ex = btn_w("Export", True)
    xe = xa - 8 - w_ex
    button(c, xe, 60, "Export", "outline", ic="arrow-up-from-line")
    # table
    tx, ty, tw_ = 20, 116, 820
    R(c, tx, ty, tw_, 44 + 5 * 50, "none", 6, BORDER)
    cols = [(12, "Role"), (120, "Login Code"), (232, "Note"), (372, "Status"), (518, "Last Login"), (668, "Expires")]
    for off, lab in cols:
        T(c, tx + off, ty + 26, lab, 14, FG, 500)
    rows = [
        ("Check-in staff", None, "K7M29QXA", "Alex - Gate A", "Active", "Oct 30, 2026, 17:58"),
        ("Binding staff", None, "R4T8NZ2B", "Maya - Binding", "Active", "Oct 30, 2026, 18:05"),
        ("Top-up staff", "Station A", "W9C3LD5H", "Sam - Cash desk", "Active", "Never"),
        ("Supervisor", None, "P6V1HJ7E", "Jordan - Lead", "Active", "Oct 30, 2026, 18:12"),
        ("Check-in staff", None, "D2X8FB4Q", "Taylor - Gate B", "Inactive", "Oct 29, 2026, 22:40"),
    ]
    y = ty + 44
    for role, st, code, note, status, last in rows:
        line(c, tx, y, tx + tw_, y, BORDER)
        cy = y + 25
        if st:
            T(c, tx + 12, y + 21, role, 14)
            T(c, tx + 12, y + 38, st, 13, MFG)
        else:
            T(c, tx + 12, cy + 5, role, 14)
        mono(c, tx + 120, cy + 5, code, 14)
        icon(c, tx + 120 + 78, cy - 6, "copy", 13, MFG)
        T(c, tx + 232, cy + 5, note, 14)
        select(c, tx + 372, y + 7, 128, status, dot="#22c55e" if status == "Active" else "#6b7280")
        T(c, tx + 518, cy + 5, last, 14, FG)
        T(c, tx + 668, cy + 5, "Never", 14, FG)
        icon(c, tx + 790, cy - 8, "pencil", 16, FG)
        y += 50
    # callouts
    ring(c, 12, 34, 408, 70, 8); num(c, 12, 34, 1)
    ring(c, xe - 4, 56, w_ex + 8, 44, 8); num(c, xe - 4, 56, 2)
    ring(c, xa - 4, 56, w_add + 8, 44, 8); num(c, xa + w_add + 4, 56, 3)
    ring(c, tx + 366, ty + 4, 140, 44 + 5 * 50 - 8, 8); num(c, tx + 366, ty + 4, 4)
    save(c, "onsite-staff-list")


def drawer(c, w, h, title):
    """Right-hand drawer frame (bg-background, border-l)."""
    R(c, 0, 0, w, h, BG, 0)
    line(c, 0.5, 0, 0.5, h, BORDER, 1)
    T(c, 20, 30, title, 16, FG, 600)


def drawer_footer(c, w, h, buttons):
    line(c, 0, h - 62, w, h - 62, BORDER)
    x = 20
    for label, kind, dis in buttons:
        x += button(c, x, h - 50, label, kind, disabled=dis) + 12


def staff_add_manual():
    W, H = 520, 518
    c = new(W, H)
    drawer(c, W, H, "Create Onsite Staff")
    tabs(c, 20, 44, ["Manual Creation", "CSV Import"], 0, w=480)
    T(c, 20, 108, "Role*", 14, FG, 500)
    select(c, 20, 114, 480, "Top-up staff")
    T(c, 20, 172, "Top-up Station*", 14, FG, 500)
    select(c, 20, 178, 480, "Station A")
    T(c, 20, 236, "Number of Login Codes*", 14, FG, 500)
    input_box(c, 20, 242, 480, "5")
    T(c, 20, 300, "Note", 14, FG, 500)
    R(c, 20, 306, 480, 52, INPUT_BG, 6, INPUT_B)
    T(c, 32, 328, "Alex - Gate team, Friday shift", 14, FG)
    T(c, 20, 376, "The same note will be applied to every code in this batch.", 13, MFG)
    T(c, 500, 376, "30/200 characters", 13, MFG, anchor="end")
    T(c, 20, 408, "Status*", 14, FG, 500)
    select(c, 20, 414, 480, "Active")  # overlaps footer? kept compact below
    drawer_footer(c, W, H + 0, [("Cancel", "outline", False), ("Generate Codes", "cta", False)])
    save(c, "onsite-staff-add-manual")


def staff_add_csv():
    W, H = 520, 516
    c = new(W, H)
    drawer(c, W, H, "Create Onsite Staff")
    tabs(c, 20, 44, ["Manual Creation", "CSV Import"], 1, w=480)
    # Alert (default): rounded-lg border bg-card px-4 py-3
    R(c, 20, 108, 480, 62, CARD, 8, BORDER_C)
    para(c, 36, 133, "Import up to 200 staff records. Login codes are created only when every row is valid.", 448, 14, FG)
    T(c, 20, 206, "Import from CSV", 14, FG, 500)
    bw = btn_w("Download Template", True, pad=12) - 0
    button(c, 500 - bw, 190, "Download Template", "outline", h=32, ic="download", pad=12)
    para(c, 20, 236, "Use the event-specific template and keep to the first four columns unchanged.", 480, 14, MFG)
    # dropzone
    R(c, 20, 280, 480, 112, "none", 6, INPUT_B, 1, "5 4")
    icon(c, 248, 294, "file-up", 24, MFG, 2)
    T(c, 260, 346, "Drop your CSV file here or click to choose a file", 14, FG, anchor="middle")
    T(c, 260, 368, "CSV only \u00b7 Maximum 200 staff records", 13, MFG, anchor="middle")
    # chosen file row
    R(c, 20, 404, 480, 38, "none", 6, BORDER)
    T(c, 32, 428, "staff-list.csv", 14, FG)
    T(c, 32 + tw("staff-list.csv", 14) + 6, 428, "\u00b7 1.2 KB", 14, MFG)
    icon(c, 476, 415, "x", 15, FG)
    drawer_footer(c, W, H, [("Cancel", "outline", False), ("Upload CSV", "cta", False)])
    save(c, "onsite-staff-add-csv")


# ---------------------------------------------------------------- search
def search_box(c, x, y, w, value, detected=None, clear=True):
    """Search results page input: h-14, border-2 border-btn-primary/60, search icon in btn-primary."""
    R(c, x, y, w, 56, INPUT_BG, 8, blend(CTA, BG, 0.6), 2)
    icon(c, x + 16, y + 18, "search", 20, CTA)
    T(c, x + 48, y + 34, value, 16, FG)
    rx = x + w - 12
    if clear:
        bw = btn_w("Clear", True, size=13, pad=12)
        rx -= bw
        button(c, rx, y + 12, "Clear", "ghost", h=32, ic="x", size=13, pad=12)
        rx -= 8
    if detected:
        pw = pill_w(detected)
        pill(c, rx - pw, y + 17, detected, "neutral")


def search_box_img():
    c = new(760, 96)
    search_box(c, 20, 20, 720, "alex@example.com", "Email \u00b7 auto-detected")
    save(c, "onsite-search-box")


def search_results():
    W, H = 800, 270
    c = new(W, H)
    search_box(c, 20, 16, 760, "alex@example.com", "Email \u00b7 auto-detected")
    # summary line
    x0 = 20
    T(c, x0, 104, "1 possible participant", 14, FG, 700)
    x1 = x0 + tw("1 possible participant", 14, 700) + 8
    T(c, x1, 104, "matched on email \u00b7 select the person actually at the desk", 14, MFG)
    # amber card
    cx, cy, cw, ch = 20, 120, 760, 134
    R(c, cx, cy, cw, ch, "#2a1604", 8, "#92400e")
    c.parts.append(f'<path d="M{cx} {cy + 8} a8 8 0 0 1 8 -8 h0 v{ch} h0 a8 8 0 0 1 -8 -8 z" fill="{AMBER}" opacity="0"/>')
    R(c, cx, cy, 4, ch, AMBER, 0)
    # left column
    lx = cx + 20
    T(c, lx, cy + 34, "Alex Chen", 16, FG, 600)
    pill(c, lx + tw("Alex Chen", 16, 600) + 8, cy + 18, "Group order", "warn")
    T(c, lx, cy + 56, "alex@example.com", 14, MFG)
    chip_w = 230
    R(c, lx, cy + 68, chip_w, 52, "#2d1c05", 4, "#92400e")
    icon(c, lx + 8, cy + 78, "alert-circle", 14, "#fef3c7")
    ytxt = cy + 87
    for ln in wrap("Matches the purchaser email, not the ticket holder", chip_w - 42, 13, 500):
        T(c, lx + 28, ytxt, ln, 13, "#fef3c7", 500)
        ytxt += 16
    # fact columns
    fx = cx + 292
    line(c, fx - 14, cy + 16, fx - 14, cy + ch - 16, "#92400e")
    cols = [("TICKET", ["TKT-20418"], ["General \u00b7 Fri"]), ("ENTRY", ["Not entered"], []), ("WRISTBAND", ["Not bound"], [])]
    xs = [fx, fx + 112, fx + 226]
    for xx, (h_, v, d) in zip(xs, cols):
        T(c, xx, cy + 34, h_, 12, MFG, 500, extra='letter-spacing="0.6"')
        T(c, xx, cy + 56, v[0], 14, FG, 500 if h_ == "TICKET" else 400)
        for i, dd in enumerate(d):
            T(c, xx, cy + 74, dd, 13, MFG)
        if h_ == "ENTRY":
            pill(c, xx, cy + 66, "Valid", "good")
    # buttons
    bx = cx + cw - 20 - 96
    button(c, bx, cy + 30, "Select", "outline", w=96)
    button(c, bx, cy + 74, "Resolve now", "ghost", h=32, size=13, w=96)
    # callouts
    ring(c, lx - 6, cy + 64, chip_w + 12, 60, 6); num(c, lx + chip_w + 6, cy + 64, 1)
    ring(c, cx - 4, cy - 4, cw + 8, ch + 8, 10); num(c, cx + cw - 40, cy - 4, 2)
    ring(c, fx - 8, cy + 14, 350, 76, 6); num(c, fx - 8, cy + 14, 3)
    ring(c, bx - 6, cy + 24, 108, 90, 6); num(c, bx + 102, cy + 24, 4)
    save(c, "onsite-search-results")


def search_nothing():
    W, H = 760, 300
    c = new(W, H)
    search_box(c, 20, 16, 720, "ZZZ999")
    py = 92
    panel(c, 20, py, 720, 190, "Nothing matched", "Search never ends on a blank page",
          "Unmatched cases are logged with the query, the time and your name, so they can be reconciled later.")
    bx, by, bw, bh = 36, py + 62, 330, 80
    R(c, bx, by, bw, bh, blend(CTA, CARD, 0.05), 6, CTA, 2)
    T(c, bx + 14, by + 28, "Create unmatched case", 14, FG, 500)
    yy = by + 48
    for ln in wrap("Record what they told you and escalate, so they aren't turned away with nothing.", bw - 28, 13):
        T(c, bx + 14, yy, ln, 13, MFG)
        yy += 17
    ring(c, bx - 5, by - 5, bw + 10, bh + 10, 8)
    save(c, "onsite-search-nothing-matched")


# ---------------------------------------------------------------- tickets
def tickets_list():
    W, H = 940, 524
    c = new(W, H)
    cw = 213
    cards = [
        ("Tickets issued", "1,200", "Everything sold for this event.", None),
        ("Entered", "640", "53% of tickets issued", "good"),
        ("Awaiting details", "12", "Recoverable at the desk \u2014 take the details, then force check-in.", "warn"),
        ("Blocked from entry", "23", "Grouped by reason on the right.", "bad"),
    ]
    for i, (l, v, f, t) in enumerate(cards):
        x = 20 + i * (cw + 16)
        R(c, x, 22, cw, 104, CARD, 8, BORDER_C)
        T(c, x + 14, 44, l, 13, MFG, 500)
        T(c, x + 14, 74, v, 24, {"good": "#6ee7b7", "warn": "#fcd34d", "bad": "#fca5a5"}.get(t, FG), 700)
        yy = 94
        for ln in wrap(f, cw - 28, 12.5):
            T(c, x + 14, yy, ln, 12.5, MFG)
            yy += 15
    ring(c, 14, 16, 912, 116, 10); num(c, 14, 16, 1)
    input_box(c, 20, 142, 330, placeholder="Filter by Ticket ID, holder or email\u2026", icon_left="search")
    button(c, 358, 142, "Filter", "outline")
    views = ["Needs attention", "All", "Valid", "Entered", "Blocked", "Transfer pending", "Cancelled"]
    x = 20
    for i, v in enumerate(views):
        w = tw(v, 13, 500) + 24
        button(c, x, 188, v, "default" if i == 0 else "outline", h=32, size=13, pad=12)
        x += w + 6
    ring(c, 14, 182, x - 20 + 4, 44, 8); num(c, 14, 182, 2)
    # table panel
    px, py, pw, ph = 20, 240, 610, 262
    panel(c, px, py, pw, ph, "Tickets", None)
    T(c, px + pw - 16, py + 29, "Showing blocked and exception tickets first", 12.5, MFG, anchor="end")
    ty = py + 46
    th_band(c, px + 1, ty, pw - 2, 32)
    cols = [(14, "Ticket ID"), (94, "Holder"), (170, "Type \u00b7 session"), (262, "Details"), (330, "Entry"), (414, "State")]
    for off, lab in cols:
        T(c, px + off, ty + 21, lab, 12.5, MFG, 500)
    rows = [
        ("TKT-20418", "Alex Chen", "GA \u00b7 Fri", "Pending", "warn", "Not entered", "Not personalized", "warn", "Take their details."),
        ("TKT-20533", "Maya Patel", "VIP \u00b7 Sat", "Complete", None, "Not entered", "Wrong session", "warn", "Direct them to the correct session."),
        ("TKT-20871", "Sam Rivera", "GA \u00b7 Fri", "Complete", None, "Not entered", "Refunded", "bad", None),
    ]
    y = ty + 32
    for tid, holder, ts, det, dt, ent, st, tone, nxt in rows:
        line(c, px + 1, y, px + pw - 1, y, BORDER_C)
        row_bg(c, px + 1, y + 1, pw - 2, 55, tone)
        stripe(c, px + 1, y + 1, 55, tone)
        T(c, px + 14, y + 23, tid, 12.5, FG, 500)
        T(c, px + 94, y + 23, holder, 13, CTA)
        T(c, px + 170, y + 23, ts, 13, MFG)
        if dt:
            pill(c, px + 262, y + 10, det, dt, size=12, h=20)
        else:
            T(c, px + 262, y + 23, det, 13, MFG)
        T(c, px + 330, y + 23, ent, 13, FG)
        pill(c, px + 414, y + 10, st, tone, size=12, h=20)
        if nxt:
            for j, ln in enumerate(wrap(nxt, 112, 12)):
                T(c, px + 414, y + 42 + j * 13, ln, 12, MFG)
        button(c, px + pw - 14 - 62, y + 10, "Resolve", "outline", h=28, w=62, size=12.5)
        y += 56
    ring(c, px - 4, py - 4, pw + 8, ph + 8, 10); num(c, px - 4, py - 4, 3)
    # why blocked panel
    qx, qw, qh = 642, 278, 262
    panel(c, qx, py, qw, qh, "Why blocked \u00b7 23")
    groups = [
        ("12", "Not personalized", True, "Take their details.", AMBER),
        ("8", "Wrong session", True, "Direct them to the correct session.", AMBER),
        ("3", "Refunded", False, "Record a service case.", RED),
    ]
    gy = py + 58
    for cnt, lab, rec, nxt, col in groups:
        c.parts.append(f'<rect x="{qx + 16}" y="{gy}" width="2" height="42" fill="{col}"/>')
        T(c, qx + 28, gy + 20, cnt, 20, FG, 700)
        lx = qx + 28 + 30
        T(c, lx, gy + 13, lab, 13.5, FG, 500)
        tag = "Recoverable at the desk" if rec else "Not recoverable here"
        tc = "#fcd34d" if rec else "#fca5a5"
        icon(c, lx, gy + 19, "check-circle" if rec else "ban", 11, tc)
        T(c, lx + 15, gy + 29, tag, 12, tc)
        T(c, lx, gy + 43, nxt, 12, MFG)
        gy += 54
    line(c, qx, py + qh - 44, qx + qw, py + qh - 44)
    fy = py + qh - 26
    for ln in wrap("Blocked is a reason, not a dead end \u2014 every reason above has a next step.", qw - 32, 12):
        T(c, qx + 16, fy, ln, 12, MFG)
        fy += 14
    ring(c, qx - 4, py - 4, qw + 8, qh + 8, 10); num(c, qx + qw - 6, py - 4, 4)
    save(c, "onsite-tickets-list")


def tickets_activity():
    W, H = 860, 290
    c = new(W, H)
    px, py, pw, ph = 20, 20, 820, 250
    panel(c, px, py, pw, ph, "Recent entry activity", None)
    T(c, px + pw - 16, py + 29, "Re-entry and the first check-in are two separate records for the same ticket", 12.5, MFG, anchor="end")
    ty = py + 46
    th_band(c, px + 1, ty, pw - 2, 32)
    cols = [(16, "Time"), (100, "Action"), (320, "Operator"), (430, "Reason"), (712, "Result")]
    for off, lab in cols:
        T(c, px + off, ty + 21, lab, 12.5, MFG, 500)
    rows = [
        ("6:58 PM", "Re-entry allowed", "Jordan Lee", "Left and came back", "Done", "good", "info"),
        ("6:51 PM", "Admitted with an override", "Taylor Kim", "Attendee details taken at the desk", "Done", "good", None),
        ("6:47 PM", "Admitted with an override", "Taylor Kim", "Identity verified at the desk", "Blocked", "bad", "bad"),
        ("6:40 PM", "Check-in undone", "Jordan Lee", "Staff scanned the wrong ticket", "Failed", "warn", None),
    ]
    y = ty + 32
    for tm, act, op, why, res, tone, st in rows:
        line(c, px + 1, y, px + pw - 1, y, BORDER_C)
        if st:
            row_bg(c, px + 1, y + 1, pw - 2, 39, st)
            stripe(c, px + 1, y + 1, 39, st)
        T(c, px + 16, y + 26, tm, 13.5, FG)
        T(c, px + 100, y + 26, act, 13.5, FG)
        T(c, px + 320, y + 26, op, 13.5, MFG)
        T(c, px + 430, y + 26, why, 13.5, MFG)
        pill(c, px + 712, y + 9, res, tone)
        y += 40
    save(c, "onsite-tickets-recent-entry-activity")


def stepper(c, x, y, w, steps, current, note):
    h = 104
    R(c, x, y, w, h, CARD, 8, BORDER_C)
    nw = 214
    ax0, ax1 = x + 24, x + w - nw - 30
    n = len(steps)
    r = 14
    li = (ax1 - ax0) / n
    cxs = [ax0 + r] + [ax0 + li * i + li / 2 for i in range(1, n - 1)] + [ax1 - r]
    cy = y + 28
    for i in range(n - 1):
        col = CTA if i < current else BORDER_C
        line(c, cxs[i] + r + 8, cy, cxs[i + 1] - r - 8, cy, col, 2)
    for i, (title, detail) in enumerate(steps):
        done, active = i < current, i == current
        cx = cxs[i]
        if done:
            c.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CTA}" stroke="{CTA}" stroke-width="2"/>')
            icon(c, cx - 8, cy - 8, "check", 16, "#ffffff", 2.5)
        elif active:
            c.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CTA}" stroke-width="2"/>')
            T(c, cx, cy + 5, str(i + 1), 13, CTA, 600, "middle")
        else:
            c.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BORDER_C}" stroke-width="2"/>')
            T(c, cx, cy + 5, str(i + 1), 13, MFG, 600, "middle")
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        tx = ax0 if i == 0 else (ax1 if i == n - 1 else cx)
        T(c, tx, cy + 34, title, 14, FG if (done or active) else MFG, 600, anchor)
        for j, ln in enumerate(wrap(detail, li - 24, 12.5)):
            T(c, tx, cy + 50 + j * 15, ln, 12.5, MFG, 400, anchor)
    line(c, ax1 + 14, y + 20, ax1 + 14, y + h - 20, BORDER_C)
    yy = y + 40
    for ln in wrap(note, nw - 24, 12.5):
        T(c, ax1 + 30, yy, ln, 12.5, MFG)
        yy += 17
    return h


def check_row(c, x, y, w, kind, label, detail, badge, tone):
    ic = {"ok": ("check", "#059669"), "bad": ("circle-x", "#dc2626"), "neutral": ("circle-dot", MFG)}[kind]
    icon(c, x, y - 12, ic[0], 16, ic[1])
    T(c, x + 28, y, label, 14, FG, 500)
    T(c, x + 28 + 128, y, detail, 14, MFG)
    bw = pill_w(badge)
    pill(c, x + w - bw, y - 16, badge, tone)


def ticket_resolution():
    W, H = 860, 590
    c = new(W, H)
    T(c, 20, 46, "Attendee details are missing", 30, FG, 700)
    T(c, 20, 70, "Neon Nights \u00b7 Oct 30, 2026 \u00b7 TKT-20418 \u00b7 Alex Chen", 14, MFG)
    x = 20
    x += pill(c, x, 90, "Tap event \u00b7 wristbands", "info") + 8
    vx = x
    vw = pill(c, x, 90, "Needs a look", "warn")
    x += vw + 8
    button(c, x, 83, "See everything for this person", "outline")
    ring(c, 14, 14, 420, 66, 8); num(c, 14, 14, 1)
    ring(c, vx - 4, 85, vw + 8, 32, 8)
    sy = 130
    stepper(c, 20, sy, 820, [("Identify", "TKT-20418 \u00b7 Alex Chen"), ("Validate", "Needs a look \u00b7 not used"),
                              ("Prepare", "Wristband scan required"), ("Confirm", "Review and apply")], 3,
            "Tap events add a fourth step for wristband binding.")
    ring(c, 14, sy - 6, 832, 116, 10); num(c, 14, sy - 6, 2)
    py = 252
    panel(c, 20, py, 820, 318, "Validation summary", None)
    T(c, 824, py + 29, "Checked 6:42 PM", 12.5, MFG, anchor="end")
    ry = py + 80
    x0, w0 = 36, 788
    rows = [("ok", "Ticket status", "TKT-20418", "Not personalized", "warn"),
            ("ok", "Event & session", "Whole event \u2014 no session on this ticket", "In window", "good"),
            ("bad", "Attendee details", "Name and email on file", "Pending", "warn"),
            ("neutral", "Entry history", "No entry recorded for this ticket", "No previous entry", "neutral")]
    for i, r_ in enumerate(rows):
        check_row(c, x0, ry + i * 38, w0, *r_)
        if i < 3:
            line(c, 36, ry + i * 38 + 14, 824, ry + i * 38 + 14)
    by = ry + 3 * 38 + 28
    R(c, 36, by, 788, 92, "none", 6, BORDER_C)
    c.parts.append(f'<path d="M42 {by} h-6 v92 h6" fill="none"/>')
    c.parts.append(f'<rect x="36" y="{by + 1}" width="4" height="90" fill="{RED}"/>')
    T(c, 54, by + 26, "Attendee details are missing", 14, FG, 500)
    T(c, 54, by + 48, "Take their details.", 14, FG)
    para(c, 54, by + 72, "Say to the participant: \u201cWe need a few details for this ticket before you can go in.\u201d", 750, 12.5, MFG)
    ring(c, 26, py + 52, 808, 4 * 38 + 4, 8); num(c, 26, py + 52, 3)
    ring(c, 30, by - 6, 800, 104, 8); num(c, 830, by - 6, 4)
    save(c, "onsite-ticket-resolution-page")


def change_preview(c, x, y, w, changes, unchanged):
    T(c, x, y, "WHAT WILL CHANGE", 12, MFG, 600, extra='letter-spacing="0.6"')
    y += 20
    for ln in changes:
        icon(c, x, y - 12, "check", 16, "#059669")
        for l in wrap(ln, w - 26, 13.5):
            T(c, x + 24, y, l, 13.5, FG)
            y += 18
        y += 4
    y += 8
    T(c, x, y, "WHAT WILL NOT CHANGE", 12, MFG, 600, extra='letter-spacing="0.6"')
    y += 20
    for ln in unchanged:
        c.parts.append(f'<circle cx="{x + 7}" cy="{y - 5}" r="3" fill="{MFG}"/>')
        for l in wrap(ln, w - 26, 13.5):
            T(c, x + 24, y, l, 13.5, MFG)
            y += 18
        y += 4
    return y


def tool_button(c, x, y, w, label, effect, limit, h=None, lock=False, note=None):
    le = wrap(effect, w - 24, 12.5)
    ll = wrap(limit, w - 24, 12.5) if limit else []
    auto = 12 + 14 + 6 + 16 * len(le) + 16 * len(ll) + (18 if note else 0) + 12
    h = max(h or 0, auto) if h is None else h
    if h is None:
        h = auto
    R(c, x, y, w, h, "none", 6, BORDER_C)
    T(c, x + 12, y + 24, label, 14, FG, 500)
    if lock:
        pill(c, x + 12 + tw(label, 14, 500) * 1.04 + 12, y + 8, "Supervisor", "warn", lock=True)
    yy = y + 44
    for ln in le:
        T(c, x + 12, yy, ln, 12.5, MFG); yy += 16
    for ln in ll:
        T(c, x + 12, yy, ln, 12.5, FG, 500); yy += 16
    if note:
        T(c, x + 12, yy + 2, note, 12.5, MFG)
    return h


def ticket_what_you_can_do():
    W, H = 860, 602
    c = new(W, H)
    px, py, pw = 20, 20, 380
    panel(c, px, py, pw, 330, "Confirmation preview", None)
    T(c, px + pw - 16, py + 29, "TKT-20418", 12.5, MFG, anchor="end")
    change_preview(c, px + 16, py + 76, pw - 32,
                   ["Ticket TKT-20418 is marked as entered.",
                    "The override is recorded against your name, with the reason and the block it cleared."],
                   ["The underlying block stays on the ticket \u2014 this admits the person, it does not fix the data.",
                    "No wristband relationship is created \u2014 this event does not use them.",
                    "No cashless wallet exists for this event."])
    qx, qy, qw, qh = 416, 20, 424, 562
    panel(c, qx, qy, qw, qh, "What you can do", None)
    T(c, qx + qw - 16, qy + 29, "Recommended first", 12.5, MFG, anchor="end")
    by = qy + 62
    recommended_box(c, qx + 16, by, qw - 32, 118)
    pill(c, qx + 28, by + 12, "Recommended", "info")
    T(c, qx + 28, by + 52, "Admit with an override", 14, FG, 500)
    T(c, qx + 28, by + 70, "Admits past a block that can be cleared at the desk.", 12.5, MFG)
    button(c, qx + 28, by + 76, "Admit with an override", "cta", w=qw - 56, h=32)
    ty = by + 118 + 10
    R(c, qx + 16, ty, qw - 32, 34, "none", 6, BORDER_C)
    T(c, qx + 28, ty + 22, "Hide everything else (2)", 14, FG, 500)
    icon(c, qx + qw - 44, ty + 9, "chevron-down", 16, FG)
    gy = ty + 34 + 18
    T(c, qx + 16, gy, "ENTRY", 12, MFG, 600, extra='letter-spacing="0.6"')
    gy += 8
    tool_button(c, qx + 16, gy, qw - 32, "Check in", "Marks the ticket as entered.", "Creates no wristband relationship.", 66)
    gy += 74
    tool_button(c, qx + 16, gy, qw - 32, "Check in manually", "Marks the ticket as entered without a scan.", "Recorded as a manual entry, so it is distinguishable later.", 66)
    gy += 74
    line(c, qx + 16, gy, qx + qw - 16, gy)
    button(c, qx + 16, gy + 12, "Record a service case", "outline", w=qw - 32)
    T(c, qx + 16, gy + 68, "Use this when nothing above resolves it, so the participant isn't", 12.5, MFG)
    T(c, qx + 16, gy + 84, "turned away with nothing recorded.", 12.5, MFG)
    fy = qy + qh - 56
    line(c, qx, fy, qx + qw, fy)
    yy = fy + 20
    for ln in wrap("Anything not listed here isn't possible for this event. An action that's listed but refused will tell you why, and the attempt is recorded.", qw - 44, 12):
        T(c, qx + 16, yy, ln, 12, MFG)
        yy += 15
    save(c, "onsite-ticket-what-you-can-do")


def ticket_action_panel():
    W, H = 520, 790
    c = new(W, H)
    drawer(c, W, H, "Admit with an override")
    x, w = 20, 480
    # 1 acting on
    y = 52
    R(c, x, y, w, 66, "none", 6, BORDER)
    T(c, x + 12, y + 22, "YOU ARE ACTING ON", 12, MFG, 500, extra='letter-spacing="0.6"')
    T(c, x + 12, y + 42, "TKT-20418", 14, FG, 500)
    T(c, x + 12, y + 59, "Alex Chen", 13, MFG)
    # warning callout
    y = 128
    bd, bg, fg = CALLOUT["warn"]
    R(c, x, y, w, 88, bg, 8, bd)
    T(c, x + 16, y + 26, "Overriding: Attendee details are missing", 14, fg, 600)
    yy = y + 48
    for ln in wrap("This admits the person. It does not fix the ticket \u2014 the block stays on the record and stays visible to anyone who looks later.", w - 32, 13):
        T(c, x + 16, yy, ln, 13, fg); yy += 18
    # 2 impact
    y = 236
    T(c, x, y, "WHAT WILL HAPPEN", 12, MFG, 500, extra='letter-spacing="0.6"')
    c.parts.append(f'<circle cx="{x + 12}" cy="{y + 19}" r="2.5" fill="{FG}"/>')
    T(c, x + 24, y + 24, "Admits past a block that can be cleared at the desk.", 13.5, FG)
    T(c, x, y + 56, "WHAT WILL NOT HAPPEN", 12, MFG, 500, extra='letter-spacing="0.6"')
    yy = y + 80
    c.parts.append(f'<circle cx="{x + 12}" cy="{yy - 5}" r="2.5" fill="{MFG}"/>')
    for ln in wrap("Does not fix the underlying record \u2014 the block stays on the ticket and stays visible.", w - 36, 13.5):
        T(c, x + 24, yy, ln, 13.5, MFG); yy += 18
    # 3 reason
    y = 376
    T(c, x, y, "Reason", 14, FG, 500); T(c, x + 54, y, "*", 14, DESTR, 500)
    select(c, x, y + 8, w, "Choose why you\u2019re doing this", placeholder=True)
    yy = y + 62
    for ln in wrap("A reason is required for this action. The note below is extra detail, not a substitute.", w - 24, 12.5):
        T(c, x, yy, ln, 12.5, MFG); yy += 16
    # 4 verify
    y = 482
    T(c, x, y, "What did you verify?", 14, FG, 500); T(c, x + 144, y, "*", 14, DESTR, 500)
    R(c, x, y + 8, w, 68, INPUT_BG, 6, INPUT_B)
    yy = y + 30
    for ln in wrap("Who approved it, what you checked, and how you confirmed who they are.", w - 24, 13.5):
        T(c, x + 12, yy, ln, 13.5, MFG); yy += 18
    yy = y + 96
    for ln in wrap("Required, at least 12 characters. A reason code alone doesn\u2019t say who approved this or what you checked \u2014 and this is the action someone will ask about later.", w - 24, 12.5):
        T(c, x, yy, ln, 12.5, MFG); yy += 16
    # 5 acknowledgement
    y = 626
    R(c, x, y, w, 68, blend("#451a03", BG, 0.9), 6, "#92400e")
    checkbox(c, x + 12, y + 14)
    yy = y + 27
    for ln in wrap("I understand this admits a ticket the ordinary check-in refuses, and that the block stays on the record.", w - 64, 13.5):
        T(c, x + 38, yy, ln, 13.5, FG); yy += 18
    # footer
    line(c, 0, 712, W, 712, BORDER)
    T(c, 20, 736, "Choose a reason.", 12.5, MFG)
    button(c, 20, 746, "Cancel", "outline", w=232)
    button(c, 268, 746, "Confirm", "cta", w=232, disabled=True)
    # callouts
    ring(c, 14, 46, 492, 74, 8); num(c, 14, 46, 1)
    ring(c, 14, 220, 492, 130, 8); num(c, 14, 220, 2)
    ring(c, 14, 360, 492, 106, 8); num(c, 14, 360, 3)
    ring(c, 14, 466, 492, 154, 8); num(c, 14, 466, 4)
    ring(c, 14, 620, 492, 80, 8); num(c, 14, 620, 5)
    save(c, "onsite-action-panel")


# ---------------------------------------------------------------- wristbands
def band_state(c, x, y, label, usable):
    """List page state chip: rounded border px-2 py-0.5 text-xs."""
    bd, bg = ("#065f46", "#022c22") if usable else ("#991b1b", "#450a0a")
    w = tw(label, 13, 500) + 16
    R(c, x, y, w, 22, bg, 4, bd)
    T(c, x + 8, y + 16, label, 13, FG, 500)
    return w


def wristband_list():
    W, H = 900, 480
    c = new(W, H)
    # search + filters
    iw = 400
    input_box(c, 20, 20, iw, placeholder="Wristband id, Ticket ID or holder email", icon_left="search")
    x = 20 + iw + 8
    x += button(c, x, 20, "Search", "outline") + 8
    x += button(c, x, 20, "All", "default") + 8
    x += button(c, x, 20, "Not working", "outline")
    ring(c, 14, 14, x - 14 + 6, 48, 8); num(c, 14, 14, 1)
    # table
    tx, ty, tw_ = 20, 78, 860
    rows_h = 84
    R(c, tx, ty, tw_, 40 + 4 * rows_h, "none", 6, BORDER)
    c.parts.append(f'<rect x="{tx + 1}" y="{ty + 1}" width="{tw_ - 2}" height="39" fill="{blend(MUTED, BG, 0.5)}"/>')
    cols = [(14, "Band"), (186, "State"), (282, "On ticket"), (382, "Holder"), (498, "Their balance"), (620, "Since")]
    for off, lab in cols:
        T(c, tx + off, ty + 25, lab, 14, FG, 500)
    data = [
        ("04A2B3C4D5E6", "WB-8842-19", "Working", True, "TKT-20418", "Alex Chen", "$25.00", "6:14 PM", ("Freeze", "Take off")),
        ("04A2B3C4D5E7", "WB-8842-20", "Frozen", False, "TKT-20533", "Maya Patel", "$40.00", "6:02 PM", ("Unfreeze", "Take off")),
        ("04A2B3C4D5E8", "WB-8842-21", "Working", True, None, None, None, "\u2014", ("Freeze", "Bind to ticket")),
        ("04A2B3C4D5E9", "WB-8842-22", "Stopped", False, None, None, None, "\u2014", ()),
    ]
    y = ty + 40
    for uid, pid, st, usable, tk, holder, bal, since, acts in data:
        line(c, tx, y, tx + tw_, y, BORDER)
        mono(c, tx + 14, y + 26, uid, 14, CTA)
        T(c, tx + 14, y + 44, f"ID {pid}", 12.5, MFG)
        band_state(c, tx + 186, y + 12, st, usable)
        if tk:
            T(c, tx + 282, y + 26, tk, 14, FG)
            T(c, tx + 382, y + 26, holder, 14, CTA)
            T(c, tx + 498, y + 26, bal, 14, FG)
        else:
            T(c, tx + 282, y + 26, "Nobody", 14, MFG)
            T(c, tx + 382, y + 26, "\u2014", 14, FG)
            T(c, tx + 498, y + 26, "\u2014", 14, FG)
        T(c, tx + 620, y + 26, since, 14, FG)
        by = y + 10
        for a in acts:
            bw = btn_w(a, size=13, pad=12)
            button(c, tx + 720, by, a, "outline", h=32, w=118, size=13)
            by += 36
        y += rows_h
    ring(c, tx + 174, ty + 4, 96, 4 * rows_h + 32, 8); num(c, tx + 174, ty + 4, 2)
    ring(c, tx + 712, ty + 44, 134, 3 * rows_h - 4 - 40 + 40, 8) if False else None
    ring(c, tx + 712, ty + 46, 134, 3 * rows_h - 12, 8); num(c, tx + 712, ty + 46, 3)
    save(c, "onsite-wristband-list")


def wristband_add_panel():
    W, H = 560, 560
    c = new(W, H)
    drawer(c, W, H, "Add wristbands to this event")
    x, w = 20, 520
    y = 52
    h = callout(c, x, y, w, "info", "These bands won\u2019t belong to anyone yet",
                "This makes them available on this event so they can be bound when someone collects one. It creates no wallet and binds nothing.")
    y += h + 18
    T(c, x, y, "Wristband UIDs or printed IDs", 14, FG, 500); T(c, x + 192, y, "*", 14, DESTR, 500)
    R(c, x, y + 8, w, 132, INPUT_BG, 6, INPUT_B)
    for i, uid in enumerate(["WB-8842-19", "WB-8842-20", "WB-8842-21"]):
        mono(c, x + 12, y + 34 + i * 22, uid, 14, FG)
    yy = y + 160
    for ln in wrap("One per line \u2014 a tag UID from a reader, or the printed ID. Separators don\u2019t matter: 04:A2:B3 and 04a2b3 are the same band. 3 bands ready.", w - 20, 12.5):
        T(c, x, yy, ln, 12.5, MFG); yy += 16
    ring(c, x - 6, y - 20, w + 12, 190, 8) if False else None
    y = yy + 14
    T(c, x, y, "Note", 14, FG, 500)
    input_box(c, x, y + 8, w, placeholder="Which box these came from, if it matters later.")
    y += 68
    icon(c, x, y - 11, "info", 14, MFG)
    tx = x + 22
    runs = [("A band nobody has seen before is registered to this event as you add it. Check each result: a band shown as ", 400),
            ("newly registered", 700), (" when you expected an existing one usually means a mistyped ID.", 400)]
    # simple wrap with mixed weights
    cx, cy_ = tx, y
    for txt, wt in runs:
        for word in txt.split(" "):
            if not word:
                continue
            ww = tw(word, 12.5, wt) + 12.5 * 0.29
            if cx + ww > x + w:
                cx = tx; cy_ += 16
            T(c, cx, cy_, word, 12.5, FG if wt == 700 else MFG, wt)
            cx += ww
    line(c, 0, H - 64, W, H - 64, BORDER)
    button(c, 20, H - 52, "Cancel", "outline", w=252)
    button(c, 288, H - 52, "Add 3 bands", "cta", w=252)
    save(c, "onsite-wristband-add-panel")


def wristband_detail():
    W, H = 860, 520
    c = new(W, H)
    # summary cards
    cw = 196
    xs = [20 + i * (cw + 12) for i in range(4)]
    cards = [("Tag UID", "04A2B3C4D5E6", "What a reader produces from this band.", None, True),
             ("Band status", "Working", None, "good", False),
             ("Bound to", "TKT-20418", "Alex Chen \u00b7 alex@example.com", None, False),
             ("Wallet link", "$25.00", "Wallet of Alex Chen \u00b7 not on this band", None, False)]
    for x, (lab, val, foot, tone, isuid) in zip(xs, cards):
        R(c, x, 20, cw, 96, CARD, 8, BORDER_C)
        T(c, x + 14, 42, lab, 13, MFG, 500)
        if isuid:
            mono(c, x + 14, 70, val, 14.5, FG)
            icon(c, x + 14 + 112, 57, "copy", 14, MFG)
        else:
            T(c, x + 14, 72, val, 22 if lab != "Bound to" else 20, {"good": "#6ee7b7"}.get(tone, FG), 700)
        if foot:
            yy = 92
            for ln in wrap(foot, cw - 28, 12):
                T(c, x + 14, yy, ln, 12, MFG); yy += 14
    ring(c, 14, 14, 832, 108, 10); num(c, 14, 14, 1)
    # band history
    py, pw = 134, 820
    panel(c, 20, py, pw, 190, "Band history", None)
    T(c, 20 + pw - 16, py + 29, "Every recorded action \u2014 the blocked attempts are kept as evidence", 12.5, MFG, anchor="end")
    ty = py + 46
    th_band(c, 21, ty, pw - 2, 30)
    for off, lab in [(16, "Time"), (100, "Action"), (330, "Operator"), (450, "Reason"), (700, "Result")]:
        T(c, 20 + off, ty + 20, lab, 12.5, MFG, 500)
    hist = [("6:14 PM", "Wristband bound", "Taylor Kim", "\u2014", "Done", "good", None),
            ("6:12 PM", "Wristband bound", "Taylor Kim", "\u2014", "Blocked", "bad", "bad"),
            ("6:10 PM", "Wristband taken off", "Jordan Lee", "Returned", "Done", "good", None)]
    y = ty + 30
    for tm, act, op, why, res, tone, st in hist:
        line(c, 21, y, 20 + pw - 1, y, BORDER_C)
        if st:
            row_bg(c, 21, y + 1, pw - 2, 36, st); stripe(c, 21, y + 1, 36, st)
        T(c, 36, y + 24, tm, 13.5, FG); T(c, 120, y + 24, act, 13.5, FG)
        T(c, 350, y + 24, op, 13.5, MFG); T(c, 470, y + 24, why, 13.5, MFG)
        pill(c, 720, y + 8, res, tone)
        y += 37
    ring(c, 14, py - 6, pw + 12, 202, 10); num(c, 14, py - 6, 2)
    # bindings
    by, bh = 346, 160
    panel(c, 20, by, pw, bh, "Bindings", None)
    T(c, 20 + pw - 16, by + 29, "Replaced and unbound bindings are kept \u2014 \u2018which band did they have then\u2019 has to be answerable", 12, MFG, anchor="end")
    ty = by + 46
    th_band(c, 21, ty, pw - 2, 30)
    for off, lab in [(16, "Ticket"), (150, "Bound"), (280, "Ended"), (410, "Reason"), (640, "State")]:
        T(c, 20 + off, ty + 20, lab, 12.5, MFG, 500)
    binds = [("TKT-20418", "6:14 PM", "\u2014", "\u2014", "Active", "good"),
             ("TKT-20102", "4:30 PM", "6:10 PM", "Returned", "Unbound", "neutral")]
    y = ty + 30
    for tk, b, e, why, st, tone in binds:
        line(c, 21, y, 20 + pw - 1, y, BORDER_C)
        if tone == "good":
            stripe(c, 21, y + 1, 36, "good")
        T(c, 36, y + 24, tk, 13.5, FG); T(c, 170, y + 24, b, 13.5, FG)
        T(c, 300, y + 24, e, 13.5, FG); T(c, 430, y + 24, why, 13.5, MFG)
        pill(c, 660, y + 8, st, tone)
        y += 37
    ring(c, 14, by - 6, pw + 12, bh + 12, 10); num(c, 14, by - 6, 3)
    save(c, "onsite-wristband-detail-page")


def action_card(c, x, y, w, label, effect, limit, btn=None, restricted=False, reason=None):
    lines_e = wrap(effect, w - 28, 12.5)
    lines_l = wrap(limit, w - 28, 12.5) if limit else []
    h = 14 + 22 + 6 + 16 * len(lines_e) + 6 + 16 * len(lines_l) + (12 + 32 if btn else 0) + (22 if reason else 0) + 10
    if restricted:
        R(c, x, y, w, h, "none", 6, INPUT_B, 2, "5 4")
    else:
        R(c, x, y, w, h, "none", 6, BORDER_C)
    T(c, x + 14, y + 28, label, 14, FG, 500)
    if restricted:
        pw = pill_w("Restricted", lock=True)
        pill(c, x + w - 14 - pw, y + 14, "Restricted", "warn", lock=True)
    yy = y + 50
    for ln in lines_e:
        T(c, x + 14, yy, ln, 12.5, MFG); yy += 16
    yy += 4
    for ln in lines_l:
        T(c, x + 14, yy, ln, 12.5, FG, 500); yy += 16
    if btn:
        button(c, x + 14, yy + 2, btn, "destructive" if restricted else "outline", h=32, w=w - 28, size=13)
    if reason:
        T(c, x + 14, yy + 14, reason, 12.5, MFG)
    return h


def wristband_actions():
    W = 520
    c = new(W, 560)
    px, pw = 20, 480
    # compute card heights first by drawing into a scratch canvas
    items = [
        dict(label="Freeze the wristband", effect="Stops this band being accepted at gates and tills.",
             limit="Blocks this band only. The balance stays spendable on any other band this person holds \u2014 freeze the wallet for that.", btn="Freeze the wristband"),
        dict(label="Force rebind the wristband", effect="Moves this band off the current holder\u2019s ticket and onto another one.",
             limit="Detaches the current holder\u2019s band. Their entry history and purchases are kept, and no balance moves.", btn="Force rebind the wristband", restricted=True),
        dict(label="Unfreeze the wristband", effect="Lets this band be used again.",
             limit="Does not unfreeze the wallet. If spending is also stopped, that is a separate action.", reason="This band is not frozen."),
    ]
    tmp = new(W, 10)
    hs = [action_card(tmp, 0, 0, pw - 32, **it) for it in items]
    total = 46 + 16 + sum(hs) + 8 * (len(hs) - 1) + 16 + 40
    c = new(W, total + 40)
    panel(c, px, 20, pw, total, "Available actions", None)
    T(c, px + pw - 16, 49, "Each says what it leaves alone", 12.5, MFG, anchor="end")
    y = 20 + 62
    for it, h in zip(items, hs):
        action_card(c, px + 16, y, pw - 32, **it)
        y += h + 8
    line(c, px, 20 + total - 38, px + pw, 20 + total - 38)
    T(c, px + 16, 20 + total - 14, "Freezing a band and freezing a wallet are separate actions on separate objects.", 12, MFG)
    save(c, "onsite-wristband-available-actions")


def conflict_side(c, x, y, w, heading, tone, name, tid, lines, h=170):
    if tone == "warn":
        R(c, x, y, w, h, blend("#451a03", CARD, 0.3), 6, "#92400e")
    else:
        R(c, x, y, w, h, "none", 6, BORDER_C)
    pill(c, x + 12, y + 12, heading, tone)
    T(c, x + 12, y + 56, name, 15, FG, 600)
    T(c, x + 12, y + 76, tid, 13, MFG)
    for i, ln in enumerate(lines):
        c.parts.append(f'<circle cx="{x + 16}" cy="{y + 98 + i * 22}" r="2.5" fill="{FG}"/>')
        T(c, x + 26, y + 102 + i * 22, ln, 13, FG)


def wristband_conflict():
    W, H = 900, 420
    c = new(W, H)
    T(c, 20, 44, "04A2B3C4D5E6", 30, FG, 700)
    T(c, 20, 68, "Bound 6:14 PM", 14, MFG)
    bw = btn_w("Add note")
    button(c, 880 - bw, 24, "Add note", "outline")
    pw_ = pill_w("Binding blocked")
    pill(c, 880 - bw - 8 - pw_, 31, "Binding blocked", "bad")
    # ownership conflict panel
    px, py, pw, ph = 20, 92, 580, 306
    panel(c, px, py, pw, ph, "Ownership conflict", None)
    sw = 234
    conflict_side(c, px + 16, py + 62, sw, "Currently bound", "neutral", "Alex Chen", "TKT-20418 \u00b7 General \u00b7 Fri",
                  ["Bound 6:14 PM", "Entered 6:32 PM", "3 cashless transactions \u00b7 $25.00"])
    conflict_side(c, px + pw - 16 - sw, py + 62, sw, "Requesting bind", "warn", "Sam Rivera", "TKT-20871 \u00b7 General \u00b7 Fri",
                  ["Requesting now", "Not entered", "No cashless activity"])
    cw_ = pill_w("Conflict")
    pill(c, px + pw / 2 - cw_ / 2, py + 62 + 74, "Conflict", "bad")
    yy = py + 62 + 170 + 22
    for ln in wrap("Whoever has entry history and spending on this band has been using it. Rebinding detaches both from the band they are wearing, so resolve ownership before moving anything.", pw - 32, 13):
        T(c, px + 16, yy, ln, 13, MFG); yy += 18
    ring(c, px + 10, py + 56, sw + 12, 182, 8); num(c, px + 10, py + 56, 1)
    ring(c, px + pw - 16 - sw - 6, py + 56, sw + 12, 182, 8); num(c, px + pw - 16 - sw - 6, py + 56, 2)
    # safe route
    qx, qw = 616, 264
    panel(c, qx, py, qw, 226, "The safe route", None)
    yy = py + 68
    for ln in wrap("Open an ownership case with both tickets, their entry history and their spending attached. It carries everything automatically \u2014 nobody has to retype what happened at the desk.", qw - 40, 13):
        T(c, qx + 16, yy, ln, 13, MFG); yy += 18
    button(c, qx + 16, yy + 6, "Investigate ownership", "outline", w=qw - 32)
    ring(c, qx + 10, yy + 0, qw - 20, 48, 8); num(c, qx + 10, yy + 0, 3)
    save(c, "onsite-wristband-ownership-conflict")


# ---------------------------------------------------------------- participants
def fact_box(c, x, y, w, label, value, detail=None, h=64):
    R(c, x, y, w, h, "none", 6, BORDER_C)
    T(c, x + 12, y + 21, label, 12.5, MFG)
    T(c, x + 12, y + 40, value, 14, FG, 600)
    if detail:
        T(c, x + 12, y + 57, detail, 12, MFG)


def participant_overview():
    W, H = 780, 612
    c = new(W, H)
    x, w = 20, 740
    labels = ["Overview", "Tickets (1)", "Wristbands (0)", "Cashless", "Activity"]
    tw_tabs = tabs(c, x, 16, labels, 0)
    ring(c, x - 5, 11, tw_tabs + 10, 46, 10); num(c, x - 5, 11, 4)
    # identity panel
    y = 66
    R(c, x, y, w, 254, CARD, 8, BORDER_C)
    T(c, x + 16, y + 34, "Alex Chen", 20, FG, 700)
    T(c, x + 16, y + 56, "alex@example.com \u00b7 +1 555 0100", 14, MFG)
    vw = pill_w("Needs a look")
    pill(c, x + w - 16 - vw, y + 16, "Needs a look", "warn")
    for i, ln in enumerate(wrap("You can deal with this, but read the notes first.", 250, 12.5)):
        T(c, x + w - 16, y + 52 + i * 16, ln, 12.5, MFG, anchor="end")
    fw = (w - 32 - 12) / 2
    fact_box(c, x + 16, y + 94, fw, "Selected event", "Neon Nights", "Tap event \u2014 entry by wristband")
    fact_box(c, x + 16 + fw + 12, y + 94, fw, "Admission", "1 ticket", "None entered yet")
    fact_box(c, x + 16, y + 94 + 76, fw, "Wristbands", "0 active bands", "None bound", h=0 + 64)
    fact_box(c, x + 16 + fw + 12, y + 94 + 76, fw, "Cashless balance", "$0.00 \u00b7 one wallet", None)
    ring(c, x + w - 16 - 258, y + 8, 266, 76, 8); num(c, x + w - 16 - 264, y + 8, 1)
    # attention
    y = 334
    panel(c, x, y, w, 150, "What needs attention", None)
    T(c, x + w - 16, y + 29, "1 item", 12.5, MFG, anchor="end")
    c.parts.append(f'<rect x="{x + 16}" y="{y + 62}" width="2" height="68" fill="{AMBER}"/>')
    T(c, x + 28, y + 76, "Attendee details are missing", 14, FG, 500)
    pill(c, x + 28 + tw("Attendee details are missing", 14, 500) * 1.04 + 14, y + 60, "TKT-20418", "neutral")
    T(c, x + 28, y + 98, "Take their details.", 14, FG)
    T(c, x + 28, y + 120, "Say: \u201cWe need a few details for this ticket before you can go in.\u201d", 12.5, MFG)
    ring(c, x - 5, y - 5, w + 10, 160, 10); num(c, x - 5, y - 5, 2)
    # recommended
    y = 498
    recommended_box(c, x, y, w, 84)
    pill(c, x + 16, y + 12, "Recommended", "info")
    T(c, x + 16, y + 56, "Put a wristband on", 14, FG, 600)
    T(c, x + 16, y + 74, "Take their details.", 13, MFG)
    bw = btn_w("Start resolution")
    button(c, x + w - 16 - bw, y + 24, "Start resolution", "cta")
    ring(c, x - 5, y - 5, w + 10, 94, 10); num(c, x - 5, y - 5, 3)
    save(c, "onsite-participant-overview")


def participant_cashless():
    W, H = 780, 560
    c = new(W, H)
    x, w = 20, 740
    tabs(c, x, 14, ["Overview", "Tickets (1)", "Wristbands (1)", "Cashless", "Activity"], 3)
    # wallet panel
    y = 66
    panel(c, x, y, w, 214, "Wallet", None)
    T(c, x + w - 16, y + 29, "One wallet per person, per event", 12.5, MFG, anchor="end")
    T(c, x + 16, y + 92, "$25.00", 30, FG, 700)
    sx = x + 16 + tw("$25.00", 30, 700) + 16
    pill(c, sx, y + 70, "Active", "good")
    ring(c, x + 8, y + 56, sx - x + 62 - 8, 50, 8); num(c, x + 8, y + 56, 1)
    line(c, x + 16, y + 112, x + w - 16, y + 112)
    bx = x + 16
    for lab in ["Correct the balance", "Issue a reward credit", "Freeze the wallet"]:
        bx += button(c, bx, y + 122, lab, "outline") + 8
    ring(c, x + 10, y + 116, bx - x - 12, 48, 8); num(c, x + 10, y + 116, 2)
    for i, ln in enumerate(wrap("Freezing the wallet stops spending on every band this person holds. It does not stop them entering, and it does not freeze any wristband.", w - 64, 12.5)):
        T(c, x + 16, y + 188 + i * 16, ln, 12.5, MFG)
    # note under buttons (xs)
    c.parts.append("")
    # recent money
    y2 = 296
    ph = 46 + 32 + 3 * 46 + 4
    panel(c, x, y2, w, ph, "Recent money", None)
    T(c, x + w - 16, y2 + 29, "Every row keeps its own amount and the balance it left", 12.5, MFG, anchor="end")
    ty = y2 + 46
    th_band(c, x + 1, ty, w - 2, 32)
    cols = [(14, "Time"), (86, "Type"), (180, "Channel"), (268, "Reference"), (470, "Amount", "end"), (584, "Balance after", "end"), (610, "Status")]
    for col in cols:
        T(c, x + col[0], ty + 21, col[1], 12.5, MFG, 500, col[2] if len(col) > 2 else "start")
    rows = [
        ("6:41 PM", "Purchase", "Main Bar", "Onsite", "No payment reference", "-$5.00", "$25.00", "Completed", "good"),
        ("6:20 PM", "Top-up", None, "Online", "pi_3Qx8Neon0042", "+$20.00", "$30.00", "Completed", "good"),
        ("6:05 PM", "Top-up", None, "Onsite", "No payment reference", "+$10.00", "$10.00", "Pending", "warn"),
    ]
    y = ty + 32
    for tm, ty_, stall, ch, ref, amt, bal, st, tone in rows:
        line(c, x + 1, y, x + w - 1, y, BORDER_C)
        if tone == "warn":
            row_bg(c, x + 1, y + 1, w - 2, 45, "warn"); stripe(c, x + 1, y + 1, 45, "warn")
        T(c, x + 14, y + 26, tm, 13, FG)
        T(c, x + 86, y + 26 if not stall else y + 22, ty_, 13, FG)
        if stall:
            T(c, x + 86, y + 38, stall, 12, MFG)
        pill(c, x + 180, y + 12, ch, "neutral", size=12, h=20)
        T(c, x + 268, y + 26, ref, 12, MFG)
        T(c, x + 470, y + 26, amt, 13, FG, 600, "end")
        T(c, x + 584, y + 26, bal, 13, FG, 400, "end")
        pill(c, x + 610, y + 12, st, tone, size=12, h=20)
        y += 46
    ring(c, x - 5, y2 - 5, w + 10, ph + 10, 10); num(c, x - 5, y2 - 5, 3)
    save(c, "onsite-participant-cashless-tab")


def participant_what():
    W = 460
    c = new(W, 900)
    qx, qy, qw = 20, 20, 420
    by = qy + 62
    recommended_box(c, qx + 16, by, qw - 32, 118)
    pill(c, qx + 28, by + 12, "Recommended", "info")
    T(c, qx + 28, by + 52, "Put a wristband on", 14, FG, 500)
    T(c, qx + 28, by + 70, "Binds a band to this ticket.", 12.5, MFG)
    button(c, qx + 28, by + 76, "Put a wristband on", "cta", w=qw - 56, h=32)
    ty = by + 128
    R(c, qx + 16, ty, qw - 32, 34, "none", 6, BORDER_C)
    T(c, qx + 28, ty + 22, "Hide everything else (3)", 14, FG, 500)
    icon(c, qx + qw - 44, ty + 9, "chevron-down", 16, FG)
    gy = ty + 34 + 22
    T(c, qx + 16, gy, "ENTRY", 12, MFG, 600, extra='letter-spacing="0.6"')
    gy += 8
    h = tool_button(c, qx + 16, gy, qw - 32, "Admit with an override", "Admits past a block that can be cleared at the desk.",
                    "Does not fix the underlying record \u2014 the block stays on the ticket and stays visible.")
    gy += h + 20
    T(c, qx + 16, gy, "WRISTBANDS", 12, MFG, 600, extra='letter-spacing="0.6"')
    gy += 8
    h = tool_button(c, qx + 16, gy, qw - 32, "Put a wristband on and check in", "Binds a band and admits them in one step.",
                    "No balance moves \u2014 the balance belongs to the person, not the band.")
    gy += h + 8
    c.parts.append('<g opacity="0.7">')
    h = tool_button(c, qx + 16, gy, qw - 32, "Put a wristband on anyway", "Binds a band to a ticket the checks object to.",
                    "Does not fix what was objected to \u2014 that stays on the ticket. No balance moves, and they are not entered until they tap.",
                    lock=True, note="Only a supervisor can do this. Ask one, or open a case.")
    c.parts.append("</g>")
    ring(c, qx + 10, gy - 4, qw - 20, h + 8, 8); num(c, qx + 10, gy - 4, 1)
    gy += h + 16
    line(c, qx + 16, gy, qx + qw - 16, gy)
    button(c, qx + 16, gy + 10, "Record a service case", "outline", w=qw - 32)
    T(c, qx + 16, gy + 70, "Use this when nothing above resolves it, so the participant isn't", 12.5, MFG)
    T(c, qx + 16, gy + 86, "turned away with nothing recorded.", 12.5, MFG)
    ring(c, qx + 10, gy + 4, qw - 20, 44, 8); num(c, qx + 10, gy + 4, 2)
    gy += 104
    # footer
    line(c, qx, gy, qx + qw, gy)
    yy = gy + 20
    for ln in wrap("Anything not listed here isn't possible for this event. An action that's listed but refused will tell you why, and the attempt is recorded.", qw - 56, 12):
        T(c, qx + 16, yy, ln, 12, MFG); yy += 15
    ph = yy - qy + 6
    # panel frame drawn behind (insert first)
    frame = []
    tmp = new(W, 10)
    panel(tmp, qx, qy, qw, ph, "What you can do", None)
    T(tmp, qx + qw - 16, qy + 29, "Recommended first", 12.5, MFG, anchor="end")
    c.parts[1:1] = tmp.parts[1:]
    c.h = qy + ph + 20
    save(c, "onsite-participant-what-you-can-do")


if __name__ == "__main__":
    staff_list()
    staff_add_manual()
    staff_add_csv()
    search_box_img()
    search_results()
    search_nothing()
    tickets_list()
    tickets_activity()
    ticket_resolution()
    ticket_what_you_can_do()
    ticket_action_panel()
    wristband_list()
    wristband_add_panel()
    wristband_detail()
    wristband_actions()
    wristband_conflict()
    participant_overview()
    participant_cashless()
    participant_what()
