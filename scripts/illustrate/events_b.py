import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ui import Canvas, FONT, ORANGE
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "events")

# dark theme tokens (globals.css .dark, oklch -> hex)
BG = "#0a0a0a"; FG = "#fafafa"; CARD = "#171717"; SEC = "#262626"; MUT = "#a3a3a3"
BRD = "#262626"      # border white/10% on card
BRD_BG = "#1f1f1f"   # border white/10% on background
INP = "#333333"      # input border white/15%
BTN = "#C795FF"      # btn-primary
LINK = "#8B5CF6"
GREEN = "#22c55e"; ORG = "#f97316"; GRAY = "#737373"; RED = "#ef4444"


def P(c, s):
    c.parts.append(s)


def T(c, x, y, s, size=14, fill=FG, weight=400, anchor="start"):
    c.text(x, y, s, size, fill, weight, anchor)


def R(c, x, y, w, h, fill=CARD, r=10, stroke=None, sw=1):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    P(c, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}/>')


def line(c, x1, y1, x2, y2, col=BRD, sw=1):
    P(c, f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}"/>')


def ico(c, x, y, d, col=MUT, size=16, sw=2, fill="none"):
    """lucide-style icon: 24 grid path d, top-left at x,y"""
    k = size / 24
    P(c, f'<g transform="translate({x},{y}) scale({k})" fill="{fill}" stroke="{col}" stroke-width="{sw}" '
         f'stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></g>')


CHEV = "m6 9 6 6 6-6"
CHEVR = "m9 18 6-6-6-6"
CHECK = "M20 6 9 17l-5-5"
XI = "M18 6 6 18M6 6l12 12"
PENCIL = "M21.2 6.8 17.2 2.8 3 17v4h4zM15 5l4 4"
BOOK = "M6 3h12a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H6zM9 8h6M9 12h6M9 16h4"
UPLOAD = "M12 15V3m0 0L7 8m5-5 5 5M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"
EXT = "M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"
SEARCH = "M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM21 21l-4.3-4.3"
INFO = "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 16v-4M12 8h.01"


def select(c, x, y, w, h, label, fg=FG, dot=None, bg=BG):
    R(c, x, y, w, h, bg, 8, INP)
    tx = x + 12
    if dot:
        P(c, f'<circle cx="{x+18}" cy="{y+h/2}" r="4.5" fill="{dot}"/>')
        tx = x + 32
    T(c, tx, y + h / 2 + 5, label, 14, fg)
    ico(c, x + w - 26, y + h / 2 - 8, CHEV, MUT, 16)


def inputbox(c, x, y, w, h, ph, icon=True, bg=BG):
    R(c, x, y, w, h, bg, 8, INP)
    tx = x + 12
    if icon:
        ico(c, x + 11, y + h / 2 - 8, SEARCH, MUT, 16)
        tx = x + 36
    T(c, tx, y + h / 2 + 5, ph, 14, MUT)


def badge(c, x, y, w, h, label, bg, fg, size=13, r=4, weight=500):
    R(c, x, y, w, h, bg, r)
    T(c, x + w / 2, y + h / 2 + size * 0.35, label, size, fg, weight, "middle")


def info(c, x, y, col=MUT):
    ico(c, x, y, INFO, col, 14, 2)


def save(c, name):
    c.save(os.path.join(OUT, name))


# ---------------------------------------------------------------- events list
def event_row(c, y, name, date, status, dot, rev, sold, ring=False, th=("#3b2a8c", "#c026d3")):
    R(c, 28, y, 704, 104, BG, 10, BRD_BG)
    gid = f"g{int(y)}"
    P(c, f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{th[0]}"/>'
         f'<stop offset="1" stop-color="{th[1]}"/></linearGradient></defs>')
    R(c, 46, y + 22, 60, 60, f"url(#{gid})", 6)
    T(c, 124, y + 40, name, 15, FG, 600)
    T(c, 124, y + 62, date, 13, MUT)
    T(c, 124, y + 84, "View event", 13, LINK)
    ico(c, 196, y + 72, EXT, LINK, 14)
    select(c, 340, y + 32, 130, 40, status, dot=dot)
    R(c, 484, y + 20, 112, 64, SEC, 8)
    T(c, 540, y + 49, rev, 14, FG, 600, "middle")
    T(c, 540, y + 71, "Revenue", 13, MUT, 400, "middle")
    R(c, 608, y + 20, 112, 64, SEC, 8)
    T(c, 664, y + 49, sold, 14, FG, 600, "middle")
    T(c, 664, y + 71, "Tickets Sold", 13, MUT, 400, "middle")


c = Canvas(760, 530)
P(c, '<path d="M44 20a12 12 0 1 0 12 14 10 10 0 0 1-12-14z" fill="#fbbf24"/>')
T(c, 68, 44, "Good night", 24, FG, 700)
R(c, 28, 66, 704, 42, BG, 8, INP)
ico(c, 42, 77, SEARCH, MUT, 18)
T(c, 70, 93, "Search events...", 14, MUT)
R(c, 28, 120, 188, 38, SEC if False else BG, 8, INP)
R(c, 32, 124, 44, 30, SEC, 6)
T(c, 54, 144, "All", 14, FG, 500, "middle")
T(c, 120, 144, "Upcoming", 14, MUT, 500, "middle")
T(c, 186, 144, "Past", 14, MUT, 500, "middle")
event_row(c, 172, "Neon Nights", "Fri, Apr 30, 1:13 PM", "Public", GREEN, "$0.00", "0/0")
event_row(c, 288, "Harbor Lights Festival", "Sat, Jan 2, 3:00 PM", "Public", GREEN, "$12,480", "250/1,000", th=("#7f1d1d", "#ef4444"))
event_row(c, 404, "Summer Rooftop Social", "Sat, Dec 12, 8:00 PM", "Public", GREEN, "$3,250", "100/500", th=("#0f766e", "#2563eb"))
c.ring(26, 64, 708, 46, 10); c.callout(26, 66, 1)
c.ring(26, 118, 192, 42, 10); c.callout(26, 120, 2)
c.ring(336, 200, 138, 48, 10); c.callout(336, 202, 3)
c.ring(120, 242, 100, 28, 8); c.callout(224, 244, 4)
save(c, "overview-events-list.svg")

# ---------------------------------------------------------------- status menu
c = Canvas(760, 290)
R(c, 28, 20, 704, 104, BG, 10, BRD_BG)
P(c, '<defs><linearGradient id="gm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b2a8c"/><stop offset="1" stop-color="#c026d3"/></linearGradient></defs>')
R(c, 46, 42, 60, 60, "url(#gm)", 6)
T(c, 124, 60, "Neon Nights", 15, FG, 600)
T(c, 124, 82, "Fri, Dec 18, 3:00 PM", 13, MUT)
T(c, 124, 104, "View event", 13, LINK); ico(c, 196, 92, EXT, LINK, 14)
select(c, 340, 52, 130, 40, "Private", dot=ORG)
R(c, 484, 40, 112, 64, SEC, 8); T(c, 540, 69, "$0.00", 14, FG, 600, "middle"); T(c, 540, 91, "Revenue", 13, MUT, 400, "middle")
R(c, 608, 40, 112, 64, SEC, 8); T(c, 664, 69, "0/0", 14, FG, 600, "middle"); T(c, 664, 91, "Tickets Sold", 13, MUT, 400, "middle")
R(c, 336, 98, 140, 128, CARD, 8, BRD)
for i, (lab, col) in enumerate([("Public", GREEN), ("Private", ORG), ("Inactive", GRAY)]):
    y = 104 + i * 38
    if lab == "Private":
        R(c, 342, y, 128, 34, SEC, 6)
        ico(c, 446, y + 9, CHECK, MUT, 16)
    P(c, f'<circle cx="356" cy="{y+17}" r="4.5" fill="{col}"/>')
    T(c, 370, y + 22, lab, 14, FG)
save(c, "overview-event-status-menu.svg")

# ---------------------------------------------------------------- summary cards
c = Canvas(860, 200)
T(c, 20, 36, "Overview", 24, FG, 700)
T(c, 20, 62, "Summary of your event performance and insights", 14, MUT)
cards = [("Total Revenue", False, "12,480", "/USD"), ("Tickets Sold", True, "250", "/1,000"),
         ("Add-ons Sold", True, "10", "/500"), ("Page Views", False, "4,000", ""),
         ("Conversion Rate", True, "6.3%", "")]
for i, (lab, inf, v, sub) in enumerate(cards):
    x = 20 + i * 166
    R(c, x, 84, 156, 100, BG, 10, BRD_BG)
    T(c, x + 16, 118, lab, 13, MUT)
    if inf:
        info(c, x + 16 + {"Tickets Sold": 81, "Add-ons Sold": 89, "Conversion Rate": 107}[lab], 106)
    T(c, x + 16, 154, v, 24, FG, 700)
    if sub:
        T(c, x + 16 + len(v) * 14 + 4, 154, sub, 13, MUT)
save(c, "overview-summary-cards.svg")

# ---------------------------------------------------------------- trend chart
c = Canvas(820, 420)
R(c, 10, 10, 800, 400, CARD, 14, BRD)
T(c, 30, 52, "Revenue", 18, "#8B5CF6", 600); ico(c, 108, 40, CHEV, "#8B5CF6", 14)
T(c, 134, 52, "Trend", 18, FG, 600)
# toggle Cumulative/Daily
R(c, 30, 70, 164, 36, BG, 8, BRD)
R(c, 34, 74, 92, 28, SEC, 6); T(c, 80, 93, "Cumulative", 13, FG, 500, "middle"); T(c, 160, 93, "Daily", 13, MUT, 500, "middle")
R(c, 206, 70, 224, 36, BG, 8, BRD)
T(c, 238, 93, "7 Days", 13, MUT, 500, "middle"); T(c, 306, 93, "30 Days", 13, MUT, 500, "middle")
R(c, 346, 74, 80, 28, SEC, 6); T(c, 386, 93, "All Time", 13, FG, 500, "middle")
R(c, 604, 70, 190, 36, BG, 8, BRD)
T(c, 644, 93, "Start Date", 13, MUT, 400, "middle"); T(c, 696, 93, "-", 13, MUT, 400, "middle"); T(c, 748, 93, "10/30/2026", 13, MUT, 400, "middle")
# axes
x0, x1, yb, yt = 90, 790, 350, 150
for i in range(5):
    y = yb - i * (yb - yt) / 4
    line(c, x0, y, x1, y, "#222222")
    T(c, 76, y + 5, ["0", "100K", "200K", "300K", "400K"][i], 13, MUT, 400, "end")
xs = ["6/15", "6/28", "7/11", "7/24", "8/6", "8/19", "9/1", "9/14", "9/27", "10/10", "10/29"]
for i, lab in enumerate(xs):
    T(c, x0 + i * (x1 - x0) / 10, 378, lab, 13, MUT, 400, "middle")
pts = [(0, 0), (.04, .02), (.1, .04), (.18, .05), (.19, .42), (.36, .43), (.4, .47), (.46, .55), (.5, .6), (.6, .64),
       (.66, .72), (.72, .76), (.8, .84), (.9, .88), (.96, .93), (1, .96)]
d = "M" + " L".join(f"{x0+px*(x1-x0):.1f},{yb-py*(yb-yt):.1f}" for px, py in pts)
P(c, f'<path d="{d}" fill="none" stroke="#B58CFF" stroke-width="2.5" stroke-linejoin="round"/>')
# open menu
R(c, 28, 60, 132, 190, CARD, 8, BRD)
for i, lab in enumerate(["Revenue", "Tickets Sold", "Add-ons Sold", "Page Views", "Conversion Rate"]):
    T(c, 44, 90 + i * 36, lab, 14, FG)
save(c, "overview-trend-chart.svg")

# ---------------------------------------------------------------- performance insights
c = Canvas(460, 420)
R(c, 10, 10, 440, 400, CARD, 14, BRD)
T(c, 34, 50, "Performance Insights", 17, FG, 600)
T(c, 34, 98, "REVENUE SOURCE", 13, MUT, 500)
for i, (lab, v) in enumerate([("Tickets & Bundles", "$9,000"), ("Add-ons", "$2,480"), ("Payment Links", "$1,000")]):
    y = 134 + i * 40
    T(c, 34, y, lab, 14, MUT); T(c, 426, y, v, 14, FG, 500, "end")
    if i < 2:
        line(c, 34, y + 14, 426, y + 14)
T(c, 34, 274, "TICKET SALES ATTRIBUTION", 13, MUT, 500); info(c, 213, 261)
for i, (lab, v) in enumerate([("Full Price Sales", "219"), ("Promo Sales", "26"), ("Comp Tickets", "0")]):
    y = 310 + i * 36
    T(c, 34, y, lab, 14, MUT); info(c, {"Full Price Sales": 132, "Promo Sales": 116, "Comp Tickets": 124}[lab], y - 12)
    T(c, 426, y, v, 14, FG, 500, "end")
    if i < 2:
        line(c, 34, y + 12, 426, y + 12)
save(c, "overview-performance-insights.svg")

# ---------------------------------------------------------------- sales breakdown
c = Canvas(860, 530)
R(c, 10, 10, 840, 510, CARD, 14, BRD)
T(c, 30, 46, "Sales Breakdown", 16, FG, 600)
inputbox(c, 30, 62, 220, 36, "Search items", True, CARD)
R(c, 262, 62, 130, 36, CARD, 8, INP); T(c, 276, 85, "All Items", 14, FG); ico(c, 366, 71, CHEV, MUT, 16)
CX = dict(item=30, price=340, sold=470, avail=570, rev=700, pct=830)
hy = 132
T(c, CX["item"] + 6, hy, "Item", 13, MUT, 500)
T(c, CX["price"], hy, "Price (USD)", 13, MUT, 500, "end")
T(c, CX["sold"], hy, "Sold / Limit", 13, MUT, 500, "end"); info(c, CX["sold"] + 4, hy - 12)
T(c, CX["avail"] - 18, hy, "Available", 13, MUT, 500, "end"); info(c, CX["avail"] - 14, hy - 12)
T(c, CX["rev"], hy, "Revenue (USD)", 13, MUT, 500, "end")
T(c, CX["pct"] - 18, hy, "% of Revenue", 13, MUT, 500, "end"); info(c, CX["pct"] - 14, hy - 12)


def brow(y, h, name, indent, price, sold, limit, pct_bar, badges, avail, rev, pct, group=False, tag=None, chev=None):
    if group:
        R(c, 20, y, 820, h, SEC, 0)
    line(c, 20, y, 840, y, "#2f2f2f")
    cy = y + h / 2
    x = 30 + indent
    if chev:
        ico(c, x, cy - 7, CHEV if chev == "d" else CHEVR, FG, 14)
        x += 18
    T(c, x, cy + 5, name, 14, FG, 600 if group else 400)
    if tag:
        tx = x + len(name) * 7.6 + 8
        R(c, tx, cy - 9, len(tag) * 7.4 + 12, 20, "#2f2f2f", 4)
        T(c, tx + 6, cy + 5, tag, 12.5, MUT)
    T(c, CX["price"], cy + 5, price, 14, FG if price != "-" else MUT, 400, "end")
    if pct_bar is None:
        T(c, CX["sold"], cy + 5, f"{sold} / {limit}", 14, FG, 500, "end")
    else:
        T(c, CX["sold"], y + 22, f"{sold} / {limit}", 14, FG, 500, "end")
        R(c, CX["sold"] - 92, y + 30, 64, 5, "#3a3a3a", 3)
        R(c, CX["sold"] - 92, y + 30, max(3, 64 * pct_bar / 100), 5, "#10b981", 3)
        T(c, CX["sold"], y + 37, f"{pct_bar}%", 12.5, GRAY, 400, "end")
    bx = CX["sold"]
    for lab, col in reversed(badges):
        w = len(lab) * 7.4 + 10
        bx -= w
        R(c, bx, y + 43, w, 18, "#14352b" if col == "g" else "#2d1b54", 4)
        T(c, bx + 5, y + 56, lab, 12.5, "#34d399" if col == "g" else "#c084fc", 600)
        bx -= 6
    T(c, CX["avail"] - 18, cy + 5, avail, 14, FG, 400, "end")
    T(c, CX["rev"], cy + 5, rev, 14, FG, 400, "end")
    T(c, CX["pct"] - 18, cy + 5, pct, 14, FG, group and 600 or 400, "end")


brow(142, 56, "FESTIVAL TICKET", 0, "-", 225, "1,000", None, [], "775", "11,500", "92.1%", True, chev="d")
brow(198, 66, "General Admission", 18, "45.00", 200, "400", 50, [("F 174", "g"), ("P 26", "p")], "200", "9,000", "72.1%")
brow(264, 66, "VIP", 18, "100.00", 25, "600", 4, [("F 25", "g")], "575", "2,500", "20.0%")
brow(330, 66, "All-Access Pass", 18, "30.00", 10, "500", 2, [("F 10", "g")], "490", "300", "2.4%", tag="Add-on")
brow(396, 46, "SHUTTLE PASSES", 0, "-", 0, "500", None, [], "500", "0", "0.0%", True, chev="r")
brow(442, 46, "HOTEL", 0, "-", 17, "2,000", None, [], "1,983", "680", "5.4%", True, chev="r")
line(c, 20, 488, 840, 488, "#2f2f2f")
T(c, 36, 508, "Total", 14, FG, 600)
T(c, CX["rev"], 508, "12,480", 14, FG, 600, "end")
T(c, CX["pct"] - 18, 508, "100.0%", 14, FG, 600, "end")
save(c, "overview-ticket-breakdown-table.svg")

# ---------------------------------------------------------------- followers
c = Canvas(840, 440)
T(c, 16, 34, "Followers", 22, FG, 700)
T(c, 16, 58, "View users who are following this event", 14, MUT)
R(c, 16, 76, 808, 308, BG, 10, BRD_BG)
T(c, 32, 106, "Name", 14, FG, 500); T(c, 280, 106, "Email", 14, FG, 500); T(c, 580, 106, "Followed At", 14, FG, 500)
rows = [("Alex Chen", "alex.chen", "Sep 18, 2026, 10:04 AM"), ("Sam Rivera", "sam.rivera", "Sep 8, 2026, 06:17 AM"),
        ("Jordan Lee", "jordan.lee", "Aug 26, 2026, 07:10 AM"), ("Drew Santos", "drew.santos", "Aug 6, 2026, 09:34 AM"),
        ("Maya Patel", "maya.patel", "Aug 6, 2026, 02:44 AM"), ("Riley Chen", "riley.chen", "Aug 5, 2026, 01:54 PM"),
        ("Jamie Ortiz", "jamie.ortiz", "Aug 5, 2026, 10:28 AM"), ("Taylor Kim", "taylor.kim", "Aug 4, 2026, 11:06 AM")]
for i, (n, e, d) in enumerate(rows):
    y = 120 + i * 33
    line(c, 17, y, 823, y, BRD_BG)
    T(c, 32, y + 22, n, 14); T(c, 280, y + 22, e + "@example.com", 14); T(c, 580, y + 22, d, 14)
T(c, 16, 420, "Showing 1 to 8 of 8 followers", 13, MUT)
for x, w, lab in [(676, 76, "Previous"), (760, 64, "Next")]:
    R(c, x, 398, w, 34, BG, 8, INP); T(c, x + w / 2, 420, lab, 13, MUT, 500, "middle")
save(c, "followers-table.svg")


# ---------------------------------------------------------------- rsvp
def checkbox(c, x, y, on=False):
    R(c, x, y, 16, 16, "#d4d4d4" if on else BG, 4, INP)
    if on:
        ico(c, x + 2, y + 2, CHECK, "#171717", 12, 3)


def appr_rej(c, x, y):
    R(c, x, y, 84, 26, "#16a34a", 13); ico(c, x + 9, y + 5, CHECK, "#fff", 15, 2.5); T(c, x + 28, y + 18, "Approve", 13, "#fff", 600)
    R(c, x + 90, y, 74, 26, "#ef4444", 13); ico(c, x + 99, y + 5, XI, "#fff", 15, 2.5); T(c, x + 118, y + 18, "Reject", 13, "#fff", 600)


def rsvp_rows(c, y0, rh, rows, checks=None):
    X = dict(chk=28, att=64, st=250, tt=410, rt=520, ac=700)
    for i, (n, e, st, tt, rt) in enumerate(rows):
        y = y0 + i * rh
        line(c, 17, y, 823, y, BRD_BG)
        if checks is not None:
            checkbox(c, X["chk"], y + rh / 2 - 8, checks[i])
        if n:
            T(c, X["att"], y + rh / 2 - 2, n, 14); T(c, X["att"], y + rh / 2 + 17, e, 13, MUT)
        else:
            T(c, X["att"], y + rh / 2 + 5, e, 13, MUT)
        if st == "Approved":
            badge(c, X["st"], y + rh / 2 - 12, 74, 24, "Approved", "#14532d", "#86efac")
        elif st == "Rejected":
            badge(c, X["st"], y + rh / 2 - 12, 70, 24, "Rejected", "#7f1d1d", "#fca5a5")
        else:
            appr_rej(c, X["st"], y + rh / 2 - 13)
        if tt:
            T(c, X["tt"], y + rh / 2 + 5, tt, 13); ico(c, X["tt"] + 32, y + rh / 2 - 6, PENCIL, FG, 13)
        T(c, X["rt"], y + rh / 2 + 5, rt, 13)
        if st != "Approved":
            ico(c, X["ac"], y + rh / 2 - 8, PENCIL, FG, 16)
        ico(c, X["ac"] + 34, y + rh / 2 - 8, BOOK, FG, 16)


def rsvp_head(c, y, checks=True):
    T(c, 64, y, "Attendee", 13, FG, 500); T(c, 250, y, "Status", 13, FG, 500); T(c, 410, y, "Ticket Type", 13, FG, 500)
    T(c, 520, y, "Registration Time", 13, FG, 500); T(c, 700, y, "Actions", 13, FG, 500)
    if checks:
        checkbox(c, 28, y - 13)


ROWS = [("Maya Patel", "maya.patel@example.com", "Approved", "rsvp", "Sep 17, 2026, 09:23"),
        ("Leo Park", "leo.park@example.com", "Pending", None, "Aug 24, 2026, 13:33"),
        ("Nina Ross", "nina.ross@example.com", "Rejected", None, "Aug 24, 2026, 13:24"),
        (None, "guest1@example.com", "Pending", None, "Aug 21, 2026, 06:29"),
        ("Omar Haddad", "omar.haddad@example.com", "Pending", None, "May 10, 2026, 17:25")]

c = Canvas(840, 520)
T(c, 16, 34, "RSVP", 22, FG, 700)
T(c, 16, 58, "Track event RSVPs and attendance confirmations", 14, MUT)
for i, (lab, v, sub) in enumerate([("Total", "8", ""), ("Approved", "1", "/8"), ("Pending", "6", "/8"), ("Declined", "1", "/8")]):
    x = 16 + i * 204
    R(c, x, 76, 192, 74, BG, 10, BRD_BG)
    T(c, x + 18, 102, lab, 13, MUT); T(c, x + 18, 133, v, 20, FG, 700)
    if sub:
        T(c, x + 18 + 14, 133, sub, 13, MUT)
select(c, 16, 168, 100, 38, "All")
inputbox(c, 126, 168, 200, 38, "Search by email", False)
R(c, 586, 168, 120, 38, BG, 8, "#7c3aed"); ico(c, 598, 178, UPLOAD, BTN, 17); T(c, 620, 192, "Export CSV", 13, BTN, 600)
R(c, 714, 168, 110, 38, "#5b3a99", 8); T(c, 769, 192, "Bulk Actions", 13, "#d9bfff", 600, "middle")
R(c, 16, 222, 808, 284, BG, 10, BRD_BG)
rsvp_head(c, 248)
rsvp_rows(c, 262, 48 + 0, ROWS, [False] * 5)
c.ring(12, 72, 816, 82, 10); c.callout(14, 74, 1)
c.ring(12, 164, 108, 46, 10); c.callout(14, 168, 2)
c.ring(244, 316, 176, 36, 10); c.callout(244, 318, 3)
c.ring(692, 316, 80, 36, 10); c.callout(692, 318, 4)
c.ring(710, 164, 118, 46, 10); c.callout(722, 166, 5)
c.ring(582, 164, 128, 46, 10); c.callout(590, 166, 6)
save(c, "rsvp-page-overview.svg")


# ---------------------------------------------------------------- edit attendee dialogs
def modal_base(c, w, h, title, desc):
    R(c, 20, 20, w, h, BG, 12, "#2a2a2a")
    T(c, 44, 62, title, 20, FG, 600)
    ico(c, 20 + w - 36, 36, XI, MUT, 16)
    T(c, 44, 90, desc, 14, MUT)


c = Canvas(560, 400)
modal_base(c, 520, 360, "Edit Attendee", "You are updating 1 attendee.")
T(c, 44, 128, "Status*", 14, FG, 500)
select(c, 44, 142, 472, 42, "Pending", bg=CARD)
R(c, 44, 220, 472, 60, BG, 0)
for lab, bx in [("Cancel", 336), ("Confirm", 428)]:
    pass
R(c, 340, 312, 78, 38, CARD, 8, INP); T(c, 379, 336, "Cancel", 14, FG, 500, "middle")
R(c, 430, 312, 86, 38, BTN, 8); T(c, 473, 336, "Confirm", 14, "#2a0a52", 600, "middle")
R(c, 44, 190, 472, 124, CARD, 8, BRD)
for i, lab in enumerate(["Approved", "Rejected", "Pending"]):
    y = 196 + i * 38
    if lab == "Pending":
        R(c, 50, y, 460, 36, SEC, 6)
        ico(c, 484, y + 10, CHECK, MUT, 16)
    T(c, 62, y + 24, lab, 14, FG)
save(c, "rsvp-edit-attendee-window.svg")

c = Canvas(560, 400)
modal_base(c, 520, 360, "Edit Attendee", "You are updating 1 attendee.")
T(c, 44, 128, "Status*", 14, FG, 500)
select(c, 44, 142, 472, 42, "Approved", bg=CARD)
T(c, 44, 224, "Ticket Type*", 14, FG, 500)
select(c, 44, 238, 472, 42, "Select ticket type", MUT, bg=CARD)
R(c, 340, 312, 78, 38, CARD, 8, INP); T(c, 379, 336, "Cancel", 14, FG, 500, "middle")
R(c, 430, 312, 86, 38, BTN, 8); T(c, 473, 336, "Confirm", 14, "#2a0a52", 600, "middle")
R(c, 44, 286, 472, 46, CARD, 8, BRD)
R(c, 50, 291, 460, 36, SEC, 6); T(c, 62, 315, "rsvp", 14, FG)
save(c, "rsvp-edit-attendee-ticket-type.svg")

# ---------------------------------------------------------------- bulk actions
c = Canvas(840, 470)
select(c, 16, 14, 100, 38, "All", MUT)
inputbox(c, 126, 14, 200, 38, "Search by email", False)
R(c, 560, 14, 120, 38, BG, 8, "#7c3aed"); ico(c, 572, 24, UPLOAD, BTN, 17); T(c, 594, 38, "Export CSV", 13, BTN, 600)
R(c, 688, 14, 108, 38, "#5b3a99", 8); T(c, 742, 38, "Bulk Actions (3)", 13, "#d9bfff", 600, "middle")
R(c, 800, 14, 28, 38, "#5b3a99", 8); ico(c, 806, 26, XI, "#d9bfff", 15)
c.ring(684, 10, 116, 46, 10)
R(c, 16, 66, 808, 388, BG, 10, BRD_BG)
rsvp_head(c, 92)
rsvp_rows(c, 106, 56, ROWS + [("Ivy Tan", "ivy.tan@example.com", "Pending", None, "May 4, 2026, 15:57")][:0], [False, True, False, True, True])
P(c, '<rect x="0" y="0" width="840" height="470" fill="#000" opacity="0.55"/>')
R(c, 200, 140, 440, 220, BG, 12, "#2a2a2a")
T(c, 228, 184, "Bulk Actions", 20, FG, 600)
T(c, 228, 212, "You are processing 3 attendees.", 14, MUT)
T(c, 228, 244, "Status*", 14, FG, 500)
select(c, 228, 256, 384, 42, "Select status", MUT, bg=CARD)
R(c, 448, 312, 78, 38, CARD, 8, INP); T(c, 487, 336, "Cancel", 14, FG, 500, "middle")
R(c, 536, 312, 76, 38, BTN, 8); T(c, 574, 336, "Confirm", 14, "#2a0a52", 600, "middle")
save(c, "rsvp-bulk-actions.svg")
