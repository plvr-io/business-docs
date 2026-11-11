import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from org_kit import *

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "images")
def out(sec, name): return os.path.join(ROOT, sec, name)

def req_label(c, x, cy, s):
    c.tc(x, cy, s, 14, weight=500)
    c.tc(x + len(s) * 8.4 + 2, cy, "*", 14, fill=RED, weight=500)

def section_row(c, x, y, w, title, extra=None):
    c.box(x, y, w, 52, None, 8, stroke="#fff", so=0.1)
    c.tc(x + 16, y + 26, title, 14, weight=600)
    if extra: c.tc(x + 16 + len(title) * 7.9 + 8, y + 26, extra, 14, fill=MUTED)
    c.icon("chevdown", x + w - 32, y + 18, 16, FG)

# ---------- Organization settings: top ----------
c = UI(780, 520)
X0, X1 = 40, 720
c.t(X0, 40, "Organization Settings", 18, weight=700)
c.t(X0, 64, "Manage your organization profile and settings", 14, MUTED)
c.box(X0, 92, 80, 80, SEC, 40, stroke="#fff", so=0.1, sw=2)
c.t(X0 + 40, 143, "NL", 24, FG, 600, "middle")
c.input(140, 92, X1 - 140, "Neon Lounge", h=48, size=20, weight=700)
c.t(X1, 168, "11/40", 13, MUTED, anchor="end")
c.t(140, 192, "plvr.io/organizers/neon-lounge", 14, BTN)
c.icon("copy", 140 + 30 * 7.6 + 8, 181, 14, MUTED)
c.t(X0, 238, "About My Organization", 16, weight=600)
c.input(X0, 252, X1 - X0, "", h=128, r=6)
c.t(X0 + 12, 278, "Underground electronic nights, every weekend.", 14)
c.section = None
section_row(c, X0, 404, X1 - X0, "Featured Event")
section_row(c, X0, 468, X1 - X0, "Website & Social Media")
c.ring(X0 - 4, 88, 88, 88, 44); c.callout(X0 - 2, 90, 1)
c.ring(136, 88, X1 - 136 + 4, 56, 8); c.callout(748, 116, 2)
c.ring(136, 178, 262, 24, 6); c.callout(412 + 4, 190, 3)
c.ring(X0 - 4, 248, X1 - X0 + 8, 136, 8); c.callout(748, 316, 4)
c.save(out("organization", "settings-profile-top.svg"))

# ---------- Organization settings: save + toast ----------
c = UI(780, 280)
section_row(c, X0, 24, X1 - X0, "Atmosphere Color", "#6B8E9B")
c.box(0, 184, 780, 96, BG, 0); c.line(0, 184.5, 780, 184.5, 0.1)
c.cta(X0, 208, X1 - X0, "Save", h=48)
# sonner toast above the footer, bottom right
tx, ty, tw = 332, 112, 408
c.parts.append(f'<rect x="{tx}" y="{ty+2}" width="{tw}" height="52" rx="8" fill="#000" fill-opacity=".3"/>')
c.box(tx, ty, tw, 52, CARD, 8, stroke="#fff", so=0.1)
c.icon("circlecheck", tx + 16, ty + 17, 18, FG)
c.tc(tx + 44, ty + 26, "Organization profile updated successfully", 14)
c.save(out("organization", "settings-save-confirmation.svg"))

# ---------- Team management ----------
c = UI(780, 470)
L, R = 40, 740
c.t(L, 46, "Team Management", 18, weight=700)
c.t(L, 70, "Manage your team members and their roles", 14, MUTED)
c.cta(R - 78, 32, 78, "Add", icon="plus")
c.ring(R - 82, 28, 86, 44); c.callout(R - 82, 28, 1)
ty0 = 102
c.box(L, ty0, R - L, 40 + 5 * 58 + 2, None, 6, stroke="#fff", so=0.1)
cm, cr = L + 8, L + 8 + 0.5 * (R - L)
c.tc(cm, ty0 + 20, "Member", 14, weight=500)
c.tc(cr, ty0 + 20, "Role", 14, weight=500)
c.tc(R - 16, ty0 + 20, "Action", 14, weight=500, anchor="end")
c.line(L, ty0 + 40.5, R, ty0 + 40.5)
rows = [("Alex Chen", "alex@example.com", "Owner"), ("Maya Patel", "maya@example.com", "Admin"),
        ("Sam Rivera", "sam@example.com", "Manager"), ("Jordan Lee", "jordan@example.com", "Manager"),
        ("Taylor Kim", "taylor@example.com", "Scanner")]
for i, (n, e, r) in enumerate(rows):
    y = ty0 + 41 + i * 58
    c.tc(cm, y + 19, n, 14); c.tc(cm, y + 39, e, 14, fill=MUTED)
    c.tc(cr, y + 29, r, 14)
    if r != "Owner":
        c.icon("pencil", R - 8 - 36 - 4 - 36 + 10, y + 21, 16, FG)
        c.icon("trash", R - 8 - 36 + 10, y + 21, 16, RED)
    if i < 4: c.line(L, y + 57.5, R, y + 57.5)
y = ty0 + 41 + 58
c.ring(R - 8 - 36 - 4 - 36 + 2, y + 11, 36, 36, 6); c.callout(R - 8 - 36 - 4 - 36 + 2, y + 11, 2)
c.ring(R - 8 - 36 - 2 + 2, y + 11, 36, 36, 6); c.callout(R - 8 - 36 + 38, y + 11, 3)
c.save(out("organization", "team-management-page.svg"))

# ---------- Team: add member window ----------
c = UI(580, 500, bg="#050505")
dx, dy, dw = 34, 20, 512
c.parts.append(f'<rect x="{dx}" y="{dy+4}" width="{dw}" height="372" rx="8" fill="#000" fill-opacity=".4"/>')
c.box(dx, dy, dw, 372, BG, 8, stroke="#fff", so=0.1)
c.icon("x", dx + dw - 36, dy + 18, 16, FG)
c.tc(dx + 24, dy + 38, "Add a Team Member", 18, weight=600)
fx, fw = dx + 24, dw - 48
req_label(c, fx, dy + 84, "Name"); c.input(fx, dy + 100, fw, "Alex Chen")
req_label(c, fx, dy + 160, "Email"); c.input(fx, dy + 176, fw, "alex@example.com")
req_label(c, fx, dy + 236, "Role"); c.select(fx, dy + 252, fw, "Manager")
c.outline_btn(dx + dw - 24 - 72 - 8 - 62, dy + 312, 72, "Cancel")
c.cta(dx + dw - 24 - 62, dy + 312, 62, "Save")
# open dropdown
px, py, pw = fx, dy + 292, fw
c.popover(px, py, pw, 3 * 54 + 8)
opts = [("Admin", "Full access to PLVR Business and PLVR Scan"),
        ("Manager", "Access to PLVR Business and PLVR Scan, except Team Management"),
        ("Scanner", "Access to PLVR Scan only (ticket scanning)")]
for i, (n, d) in enumerate(opts):
    oy = py + 4 + i * 54
    if i == 1: c.box(px + 4, oy, pw - 8, 52, SEC, 4)
    c.tc(px + 14, oy + 18, n, 14); c.tc(px + 14, oy + 38, d, 13, fill=MUTED)
    if i == 1: c.icon("check", px + pw - 28, oy + 8, 16, FG)
c.h = 500
c.save(out("organization", "team-add-member-window.svg"))

# ---------- Audience: headline + charts ----------
def bars_chart(c, x, y, w, h, data, ticks, tmax, labels, stacked=None, lab_vals=None):
    ax = x + 34
    pw = w - 34
    for tv in ticks:
        yy = y + h - 22 - (h - 38) * tv / tmax
        c.line(ax, yy, x + w, yy, 0.12, 1, "3 3")
        c.t(ax - 6, yy + 4.5, f"{tv:,}", 13, MUTED, anchor="end")
    slot = pw / len(data)
    for i, v in enumerate(data):
        bw = slot * 0.6; bx = ax + i * slot + (slot - bw) / 2
        base = y + h - 22
        if stacked:
            n, p = v
            hn = (h - 38) * n / tmax; hp = (h - 38) * p / tmax
            c.box(bx, base - hn, bw, hn, BTN, 0)
            c.box(bx, base - hn - hp, bw, hp, BTN, 0, fo=0.35)
            top = base - hn - hp; val = n + p
        else:
            hh = (h - 38) * v / tmax
            c.box(bx, base - hh, bw, hh, BTN, 0); top = base - hh; val = v
        c.t(bx + bw / 2, top - 5, f"{val:,}", 13, FG, anchor="middle")
        c.t(bx + bw / 2, y + h - 4, labels[i], 12, MUTED, anchor="middle")

def metric(c, x, y, w, label, val):
    c.box(x, y, w, 76, BG, 6, stroke="#fff", so=0.1)
    c.t(x + 20, y + 28, label, 14, MUTED)
    c.t(x + 20, y + 56, val, 20, FG, 700)

c = UI(840, 530)
c.t(20, 44, "Audience", 20, weight=600)
c.t(20, 68, "Understand who is attending your events and how loyal they are", 14, MUTED)
mw = (800 - 32) / 3
for i, (l, v) in enumerate([("Total Unique Attendees", "1,250"), ("Returning Attendees", "380"), ("Retention Rate", "30.4%")]):
    metric(c, 20 + i * (mw + 16), 90, mw, l, v)
cw = (800 - 48) / 3
cards = [("Audience Distribution", ["Number of attendees", "by events attended"]),
         ("Returning Attendees Growth", ["Cumulative returning", "attendees over time"]),
         ("Monthly Active Attendees", ["Unique attendees who purchased", "a ticket each month"])]
for i, (title, desc) in enumerate(cards):
    x = 20 + i * (cw + 24); y = 190
    c.box(x, y, cw, 322, CARD, 12, stroke="#fff", so=0.1)
    c.t(x + 20, y + 40, title, 16 if i != 1 else 15, FG, 600)
    c.t(x + 20, y + 62, desc[0], 13, MUTED); c.t(x + 20, y + 80, desc[1], 13, MUTED)
    ch = (x + 16, y + 98, cw - 32, 210)
    if i == 0:
        bars_chart(c, *ch, [870, 250, 130], [0, 250, 500, 750], 900, ["1 event", "2 events", "3 events"])
    elif i == 1:
        bars_chart(c, *ch, [(40, 220), (50, 260), (70, 310)], [0, 100, 200, 300], 400, ["Aug 2026", "Sep 2026", "Oct 2026"], stacked=True)
    else:
        bars_chart(c, *ch, [180, 240, 310], [0, 100, 200, 300], 400, ["Aug 2026", "Sep 2026", "Oct 2026"])
c.save(out("organization", "audience-headline-and-charts.svg"))

# ---------- Audience: returning attendees table ----------
c = UI(780, 500)
c.box(20, 20, 740, 460, CARD, 12, stroke="#fff", so=0.1)
c.t(44, 60, "Returning Attendees", 16, FG, 600)
c.t(44 + 19 * 8.6 + 8, 60, "380 total", 14, MUTED)
c.t(44, 84, "Attendees who have purchased tickets to 2 or more events", 14, MUTED)
c.outline_btn(576, 40, 160, "Export CSV", icon="export")
c.ring(572, 36, 168, 44); c.callout(572, 36, 1)
cols = [(44, "Name", "start"), (170, "Email", "start"), (548, "Events", "end"), (648, "First Purchase", "end"), (736, "Became Returning", "end")]
cx = {"n": 44, "e": 176, "ev": 456, "fp": 586, "br": 736}
ty = 112
for x, lab, a in [(cx["n"], "Name", "start"), (cx["e"], "Email", "start"), (cx["ev"], "Events", "end"), (cx["fp"], "First Purchase", "end"), (cx["br"], "Became Returning", "end")]:
    c.t(x, ty + 22, lab, 14, MUTED, 500, a)
c.line(44, ty + 36.5, 736, ty + 36.5)
data = [("Alex Chen", "alex@example.com", "4", "Jan 12, 2026", "Feb 20, 2026"),
        ("Maya Patel", "maya@example.com", "3", "Feb 3, 2026", "Mar 14, 2026"),
        ("Sam Rivera", "sam@example.com", "3", "Jan 25, 2026", "Apr 2, 2026"),
        ("Jordan Lee", "jordan@example.com", "2", "Mar 8, 2026", "May 16, 2026"),
        ("Taylor Kim", "taylor@example.com", "2", "Apr 19, 2026", "Jun 6, 2026"),
        ("Casey Morgan", "casey@example.com", "2", "May 1, 2026", "Jul 11, 2026"),
        ("Riley Zhang", "riley@example.com", "2", "Jun 14, 2026", "Aug 22, 2026")]
for i, (n, e, ev, fp, br) in enumerate(data):
    y = ty + 37 + i * 44
    m = y + 22
    c.tc(cx["n"], m, n, 14, weight=500)
    c.tc(cx["e"], m, e, 13, fill=MUTED, font=MONO)
    c.tc(cx["ev"], m, ev, 14, anchor="end")
    c.tc(cx["fp"], m, fp, 14, fill=MUTED, anchor="end")
    c.tc(cx["br"], m, br, 14, fill=MUTED, anchor="end")
    if i < 6: c.line(44, y + 43.5, 736, y + 43.5)
c.save(out("organization", "audience-returning-attendees-table.svg"))

# ---------- Table booking: shared form pieces ----------
def hint(c, x, y, lines):
    for i, s in enumerate(lines): c.tc(x, y + i * 20, s, 14, fill=MUTED)

def venue_card(c, x, y, w):
    c.box(x, y, w, 58, None, 6, stroke="#fff", so=0.1)
    c.icon("pin", x + 16, y + 19, 16, MUTED)
    c.t(x + 44, y + 26, "Lumi Lounge", 14, FG, 500)
    c.t(x + 44, y + 46, "1 Example Road, Central, Hong Kong", 13, MUTED)

def zigzag(c, x, y, w):
    pts = " ".join(f"{x + i*10},{y + (5 if i % 2 else 0)}" for i in range(int(w // 10) + 1))
    c.parts.append(f'<polyline points="{pts}" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="1.5"/>')

FX, FW = 30, 640
# ---------- Table booking: setup ----------
c = UI(700, 500)
y = 24
c.tc(FX, y + 8, "Name*", 14, weight=500); c.input(FX, y + 24, FW, "Lumi Lounge"); y += 24 + 36 + 24
c.tc(FX, y + 8, "Currency*", 14, weight=500); c.select(FX, y + 24, FW, "HKD")
hint(c, FX, y + 24 + 36 + 18, ["Every table and table order is priced in it."]); y += 24 + 36 + 38 + 24
c.tc(FX, y + 8, "Venue", 14, weight=500); c.tc(FX + FW, y + 8, "Optional", 14, fill=MUTED, anchor="end")
c.input(FX, y + 24, FW, "Search for a venue...", color=MUTED, icon="search")
venue_card(c, FX, y + 24 + 36 + 12, FW)
hint(c, FX, y + 24 + 36 + 12 + 58 + 18, ["Leave empty to use your organization's venue. Booking times follow the venue's timezone."])
y += 24 + 36 + 12 + 58 + 38 + 20
zigzag(c, FX, y, FW); y += 28
c.cta(FX + FW - 190, y, 190, "Create Table Booking")
c.h = y + 36 + 24; c.parts[0] = c.parts[0].replace(f'height="500"', f'height="{c.h}"')
c.save(out("other", "table-booking-setup.svg"))

# ---------- Table booking: settings ----------
c = UI(700, 500)
y = 20
c.tc(FX, y + 8, "Currency*", 14, weight=500); c.select(FX, y + 24, FW, "HKD")
hint(c, FX, y + 24 + 36 + 18, ["Every table and table order is priced in it."])
c.ring(FX - 4, y + 20, FW + 8, 44); c.callout(FX + FW + 4, y + 42, 1)
y += 24 + 36 + 38 + 24
c.tc(FX, y + 8, "Venue", 14, weight=500)
c.input(FX, y + 24, FW, "Search for a venue...", color=MUTED, icon="search")
venue_card(c, FX, y + 24 + 36 + 12, FW)
hint(c, FX, y + 24 + 36 + 12 + 58 + 18, ["Booking times follow the venue's timezone (currently Asia/Hong_Kong)."])
c.ring(FX - 4, y + 20, FW + 8, 44 + 12 + 58 + 4); c.callout(FX + FW + 4, y + 70, 2)
y += 24 + 36 + 12 + 58 + 38 + 24
c.tc(FX, y + 8, "Status*", 14, weight=500); c.select(FX, y + 24, FW, "Active")
hint(c, FX, y + 24 + 36 + 18, ["Table booking cannot be deleted. While inactive it is hidden from onsite until it is set",
                                "back to active."])
c.ring(FX - 4, y + 20, FW + 8, 44); c.callout(FX + FW + 4, y + 42, 3)
y += 24 + 36 + 58 + 24
zigzag(c, FX, y, FW); y += 24
c.cta(FX + FW - 140, y, 140, "Save Changes")
c.ring(FX + FW - 144, y - 4, 148, 44); c.callout(FX + FW - 144, y - 4, 4)
c.h = y + 36 + 20; c.parts[0] = c.parts[0].replace('height="500"', f'height="{c.h}"')
c.save(out("other", "table-booking-settings.svg"))

# ---------- Table booking: tables list ----------
c = UI(760, 480)
L, R = 30, 730
c.t(L, 46, "Tables", 20, weight=600)
c.t(L, 70, "The tables guests can book, with the capacity and minimum spend each table order starts from.", 14, MUTED)
c.tc(L, 110, "Search", 14, weight=500)
c.input(L, 124, 280, "Search by table name", color=MUTED)
c.cta(R - 128, 124, 128, "Add Tables", icon="plus")
c.ring(R - 132, 120, 136, 44); c.callout(R - 132, 120, 1)
ty = 184
c.box(L, ty, R - L, 40 + 6 * 41 + 1, None, 6, stroke="#fff", so=0.1)
cap, ms = L + 8 + 330, L + 8 + 330 + 180
c.tc(L + 8, ty + 20, "Table Name", 14, weight=500); c.tc(cap, ty + 20, "Default Capacity", 14, weight=500)
c.tc(ms, ty + 20, "Minimum Spend", 14, weight=500)
c.line(L, ty + 40.5, R, ty + 40.5)
for i in range(6):
    y = ty + 41 + i * 41
    c.tc(L + 8, y + 20, f"A{i+1}", 14, weight=500); c.tc(cap, y + 20, "4", 14); c.tc(ms, y + 20, "HKD 500.00", 14)
    c.icon("pencil", R - 8 - 36 + 10, y + 12, 16, FG)
    if i < 5: c.line(L, y + 40.5, R, y + 40.5)
y = ty + 41
c.ring(R - 8 - 36 + 2, y + 2, 36, 36, 6); c.callout(R - 8 - 36 + 38, y + 2, 2)
c.h = ty + 40 + 6 * 41 + 20; c.parts[0] = c.parts[0].replace('height="480"', f'height="{c.h}"')
c.save(out("other", "table-booking-tables-list.svg"))

# ---------- Table booking: add tables drawer ----------
c = UI(640, 370, bg=BG)
c.line(0.5, 0, 0.5, 370, 0.15)
c.tc(16, 28, "Add Tables", 16, weight=600)
gx, gw = 20, 640 - 40 - 8 - 36
cwid = (gw - 24) / 3
labels = ["Name*", "Default Capacity*", "Minimum Spend (HKD)"]
for i, l in enumerate(labels): c.tc(gx + i * (cwid + 12), 82, l, 14, weight=500)
rows = [("A7", "4", "500"), ("A8", "4", "500")]
for r, vals in enumerate(rows):
    yy = 96 if r == 0 else 96 + 36 + 12 + 22
    yy = 96 if r == 0 else 144
    for i, v in enumerate(vals):
        c.input(gx + i * (cwid + 12), yy, cwid, v)
    c.icon("trash2", gx + gw + 8 + 10, yy + 10, 16, FG)
c.outline_btn(20, 202, 112, "Add Row", icon="plus")
c.tc(620, 220, "2/100", 14, fill=MUTED, anchor="end")
hint(c, 20, 256, ["Capacity and minimum spend are defaults that prefill a table order onsite.", "Each order can still change them."])
c.box(0, 294, 640, 76, BG, 0); c.line(0, 294.5, 640, 294.5, 0.1)
c.outline_btn(20, 314, 80, "Cancel"); c.cta(112, 314, 118, "Add 2 Tables")
c.save(out("other", "table-booking-add-tables.svg"))

# ---------- RSVP: approve ticket selection ----------
c = UI(580, 420, bg="#050505")
dx, dy, dw = 34, 20, 512
c.parts.append(f'<rect x="{dx}" y="{dy+4}" width="{dw}" height="300" rx="8" fill="#000" fill-opacity=".4"/>')
c.box(dx, dy, dw, 300, BG, 8, stroke="#fff", so=0.1)
c.tc(dx + 24, dy + 38, "Approve Attendee", 18, weight=600)
c.tc(dx + 24, dy + 66, "Select a ticket type for this attendee.", 14, fill=MUTED)
fx, fw = dx + 24, dw - 48
c.tc(fx, dy + 110, "Ticket Type*", 14, weight=500)
c.select(fx, dy + 126, fw, "Select ticket type", color=MUTED)
c.outline_btn(dx + dw - 24 - 62 - 8 - 72, dy + 238, 72, "Cancel")
c.cta(dx + dw - 24 - 62, dy + 238, 62, "Confirm")
px, py = fx, dy + 166
c.popover(px, py, fw, 3 * 32 + 8)
for i, n in enumerate(["General Admission", "VIP", "Early Bird"]):
    c.tc(px + 14, py + 4 + i * 32 + 16, n, 14)
c.h = 340
c.parts[0] = c.parts[0].replace('height="420"', 'height="340"')
c.save(out("events", "rsvp-approve-ticket-selection.svg"))
print("ok")
