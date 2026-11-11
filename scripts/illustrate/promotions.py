import os, sys, random
sys.path.insert(0, os.path.dirname(__file__))
from promotions_kit import *

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "promotions")
os.makedirs(OUT, exist_ok=True)
DIM = "#050505"


def qr(c, x, y, size, seed=7, fg="#000", bg="#fff"):
    n = 25
    m = size / n
    rnd = random.Random(seed)
    c.rect(x, y, size, size, bg, 0)
    finders = [(0, 0), (n - 7, 0), (0, n - 7)]

    def in_finder(i, j):
        return any(fx <= i < fx + 8 and fy <= j < fy + 8 for fx, fy in finders)
    for i in range(n):
        for j in range(n):
            if in_finder(i, j):
                continue
            if rnd.random() < 0.5:
                c.parts.append(f'<rect x="{x+i*m:.2f}" y="{y+j*m:.2f}" width="{m+0.2:.2f}" height="{m+0.2:.2f}" fill="{fg}"/>')
    for fx, fy in finders:
        X, Y = x + fx * m, y + fy * m
        c.parts.append(f'<rect x="{X:.2f}" y="{Y:.2f}" width="{7*m:.2f}" height="{7*m:.2f}" fill="{fg}"/>')
        c.parts.append(f'<rect x="{X+m:.2f}" y="{Y+m:.2f}" width="{5*m:.2f}" height="{5*m:.2f}" fill="{bg}"/>')
        c.parts.append(f'<rect x="{X+2*m:.2f}" y="{Y+2*m:.2f}" width="{3*m:.2f}" height="{3*m:.2f}" fill="{fg}"/>')


def footer_btns(c, right, y, cancel="Cancel", ok="Save", ok_cta=True):
    wok = int(32 + tw(ok, 14, 500))
    wc = int(32 + tw(cancel, 14, 500))
    c.btn(right - wok - 8 - wc, y, cancel, outline=True)
    c.cta(right - wok, y, ok)


# =========================================================== PROMO CODES
def promo_table(c, x, y, w):
    """toolbar + table. returns bottom y"""
    c.field(x, y, 320, placeholder="Search promo codes", h=36)
    create_w = int(48 + tw("Create", 14, 500))
    ex_w = int(48 + tw("Export CSV", 14, 500))
    c.cta(x + w - create_w, y, "Create", "plus", w=create_w)
    c.cta(x + w - create_w - 8 - ex_w, y, "Export CSV", "arrow-up-from-line", outline=True, w=ex_w)
    ty = y + 56
    cols = [("Code", 112, 0), ("Description", 116, 0), ("Discount", 78, 0), ("Uses/Limit", 100, 1),
            ("Apply to", 124, 1), ("Revenue (USD)", 118, 1), ("Cost (USD)", 100, 1), ("Status", 130, 0), ("", 40, 0)]
    rows = [
        ("SPRING20", "Spring sale", "20%", "12/50", "Early Bird", "1,240.00", "310.00", "Active"),
        ("WELCOME10", "Welcome offer", "10%", "8/Unlimited", "All ticket types", "420.00", "42.00", "Active"),
        ("FRIEND5", "-", "USD 5.00", "3/20", "All ticket types", "150.00", "15.00", "Active"),
        ("EARLYBIRD", "Early supporters", "15%", "50/50", "Early Bird", "2,100.00", "315.00", "Inactive"),
    ]
    th = 40
    rh = 52
    tot = sum(cw for _, cw, _ in cols)
    H = th + rh * len(rows)
    c.table_frame(x, ty, w, H)
    cx = x
    for lab, cw, sort in cols:
        px = cx + 8
        if lab:
            c.t(px, ty + 25, lab, 13, BTN if sort else FG, 500)
            if sort:
                c.sort_tri(px + tw(lab, 13, 500) + 6, ty + 20)
        cx += cw
    for r, row in enumerate(rows):
        yy = ty + th + r * rh
        c.row_line(x, yy, w)
        cx = x
        for i, (lab, cw, sort) in enumerate(cols):
            px = cx + 8
            cy = yy + rh / 2 + 5
            if i < 7:
                s = row[i]
                if i == 0:
                    c.t(px, cy, s + " ⧉", 13)
                else:
                    c.t(px, cy, s, 13)
            elif i == 7:
                st = row[7]
                c.select(px, yy + 8, 118, value=st, dot=GREEN if st == "Active" else GRAY)
            else:
                c.dot_menu(cx - 2, yy + 8)
            cx += cw
    return ty, th, rh, cols


def img_promo_list():
    W = 960
    c = K(W, 440)
    c.page_header(20, 20, "Promo Codes", "Create and manage discount codes")
    x = 20
    mw = 176
    c.metric(x, 80, mw, "Tickets Sold", "78")
    c.metric(x + mw + 32, 80, mw, "Revenue", "3,910.00", "USD")
    c.metric(x + 2 * (mw + 32), 80, mw, "Cost", "682.00", "USD")
    promo_table(c, 20, 190, W - 40)
    c.h = 190 + 56 + 40 + 52 * 4 + 24
    c.parts[0] = f'<rect x="0" y="0" width="{W}" height="{c.h}" rx="0" fill="{BG}"/>'
    c.save(f"{OUT}/promo-codes-list.svg")


def drawer(c, x, y, w, h, title=None):
    c.rect(x, y, w, h, BG, 0, BORDER_CARD)
    if title:
        c.t(x + 16, y + 34, title, 16, FG, 600)


def lab_input(c, x, y, w, label, kind, value=None, placeholder=None, prefix=None):
    c.t(x, y + 14, label, 14, FG, 500)
    if kind == "input":
        c.field(x, y + 22, w, value, placeholder, prefix=prefix)
    else:
        c.select(x, y + 22, w, value, placeholder)
    return y + 22 + 36 + 24


def img_promo_create():
    colw, gap = 312, 12
    W = colw * 3 + gap * 2
    H = 520
    c = K(W, H, DIM)
    # column 1
    x = 0
    drawer(c, x, 0, colw, H, "Create Promo Code")
    y = 56
    p = x + 16
    iw = colw - 32
    y = lab_input(c, p, y, iw, "Generation Method*", "select", "Manual")
    y = lab_input(c, p, y, iw, "Code*", "input", "SPRING20")
    y = lab_input(c, p, y, iw, "Description", "input", None, "Add a description for this promo code")
    y = lab_input(c, p, y, iw, "Discount Type*", "select", "Percentage")
    # column 2
    x = colw + gap
    drawer(c, x, 0, colw, H)
    p = x + 16
    y = 20
    y = lab_input(c, p, y, iw, "Discount Value*", "input", "20", prefix="%")
    y = lab_input(c, p, y, iw, "Apply To*", "select", "Specific ticket type")
    y = lab_input(c, p, y, iw, "Ticket Type*", "select", "Early Bird")
    c.t(p, y + 12, "Usage Limit", 14, FG, 500)
    c.switch(p + 96, y, True)
    y += 40
    c.t(p, y + 14, "Maximum transactions allowed", 14, FG, 500)
    c.t(p, y + 32, "for this code*", 14, FG, 500)
    c.field(p, y + 40, iw, "50")
    # column 3
    x = 2 * (colw + gap)
    drawer(c, x, 0, colw, H)
    p = x + 16
    y = 20
    c.t(p, y + 12, "Time Limit", 14, FG, 500)
    c.switch(p + 96, y, True)
    y += 40
    for lab, d, hh in (("Sales Start Date *", "Oct 1, 2026", "00"), ("Sales End Date *", "Oct 31, 2026", "23")):
        c.t(p, y + 14, lab, 14, FG, 500)
        c.rect(p, y + 22, 150, 36, INPUT_BG, 6, INPUT_BORDER)
        c.t(p + 12, y + 45, d, 14, FG)
        c.icon("calendar", p + 150 - 28, y + 30, 16, "#6e6e6e")
        c.t(p + 160, y + 14, "Hour", 14, FG, 500)
        c.t(p + 218, y + 14, "Minute", 14, FG, 500)
        c.rect(p + 160, y + 22, 52, 36, INPUT_BG, 6, INPUT_BORDER)
        c.t(p + 186, y + 45, hh, 14, FG, 400, "middle")
        c.t(p + 215, y + 45, ":", 14, FG)
        c.rect(p + 220, y + 22, 52, 36, INPUT_BG, 6, INPUT_BORDER)
        c.t(p + 246, y + 45, "00", 14, FG, 400, "middle")
        y += 58 + 18
    c.t(p, y + 14, "Remarks", 14, FG, 500)
    c.field(p, y + 22, iw)
    # footer
    c.rect(x + 1, H - 76, colw - 1, 76, BG, 0)
    c.btn(p, H - 56, "Cancel", outline=True)
    c.cta(p + int(32 + tw("Cancel", 14, 500)) + 8, H - 56, "Save")
    c.save(f"{OUT}/promo-codes-create-panel.svg")


def img_promo_usage():
    W, H = 900, 360
    c = K(W, H, DIM)
    # left: row snippet with menu
    c.table_frame(16, 24, 330, 56)
    c.t(28, 57, "SPRING20 ⧉", 13)
    c.select(150, 34, 118, value="Active", dot=GREEN)
    c.rect(290, 34, 36, 36, MUTED, 6)
    c.dot_menu(290, 34)
    h = c.drop(186, 78, 140, [("pencil", "Edit"), ("copy-plus", "Clone"), ("users", "View Usage")], hl=2)
    c.ring(190, 78 + 4 + 64, 132, 32, 4)
    # right: usage log drawer
    dx, dw = 370, 530
    drawer(c, dx, 0, dw, H, "Usage Log - SPRING20")
    c.rich(dx + dw - 20, 76, [("Uses: ", 400), ("12", 700), ("/ 50", 400)], anchor="end")
    ty = 96
    cols = [("Buyer", 170), ("Tickets", 120), ("Date & Time", 170)]
    x0 = dx + 20
    c.line(x0, ty + 40, x0 + 460, ty + 40)
    cx = x0
    for lab, cw in cols:
        c.t(cx + 8, ty + 25, lab, 14, FG, 500)
        cx += cw
    data = [("alex@example.com", "Early Bird", "Oct 12, 2026, 19:30"),
            ("maya@example.com", "Early Bird", "Oct 12, 2026, 20:05"),
            ("sam@example.com", "Early Bird", "Oct 13, 2026, 09:12"),
            ("jordan@example.com", "Early Bird", "Oct 14, 2026, 17:48")]
    for i, r in enumerate(data):
        yy = ty + 40 + i * 48
        cx = x0
        for (lab, cw), s in zip(cols, r):
            c.t(cx + 8, yy + 30, s, 14)
            cx += cw
        c.line(x0, yy + 48, x0 + 460, yy + 48)
    c.save(f"{OUT}/promo-codes-usage-log.svg")


# =========================================================== DOOR SALES
def poster(c, x, y, w, maxy=None):
    h = w * 4 / 3
    full_h = h
    if maxy is not None:
        h = min(h, maxy - y)
    s = w / 400
    c.parts.append(
        f'<defs><radialGradient id="pg1" cx="0.38" cy="0.3" r="0.55"><stop offset="0" stop-color="#4b2590"/><stop offset="1" stop-color="#4b2590" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="pg2" cx="0.95" cy="0.4" r="0.45"><stop offset="0" stop-color="#2a7280"/><stop offset="1" stop-color="#2a7280" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="pg3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#721BFD"/><stop offset="1" stop-color="#00A9EF"/></linearGradient>'
        f'<clipPath id="pc"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs>')
    h = full_h
    c.parts.append(f'<g clip-path="url(#pc)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#26384f"/>'
                   f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#2f2d6e" opacity="0.8"/>'
                   f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#pg1)"/>'
                   f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#pg2)"/>'
                   '')
    # logo wordmark placeholder
    c.t(x + w / 2, y + 50 * s, "PLVR", 28 * s, "#fff", 800, "middle")
    # glass card
    cx, cy, cw, ch = x + 20 * s, y + 70 * s, w - 40 * s, 290 * s
    c.parts.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="{16*s}" fill="#fff" fill-opacity="0.1" stroke="#fff" stroke-opacity="0.2"/>')
    # headline placeholder bars
    for i, bw in enumerate((130, 90)):
        c.parts.append(f'<rect x="{x + w/2 - bw*s/2}" y="{cy + (16 + i*13)*s}" width="{bw*s}" height="{6*s}" rx="{3*s}" fill="#fff" fill-opacity="0.75"/>')
    q = 173 * s
    qx, qy = x + w / 2 - q / 2, cy + 56 * s
    c.parts.append(f'<rect x="{qx}" y="{qy}" width="{q}" height="{q}" rx="{24*s}" fill="url(#pg3)"/>')
    p = 8 * s
    c.parts.append(f'<rect x="{qx+p}" y="{qy+p}" width="{q-2*p}" height="{q-2*p}" rx="{16*s}" fill="#fff"/>')
    qr(c, qx + 16 * s, qy + 16 * s, q - 32 * s, seed=11)
    c.t(x + w / 2, qy + q + 24 * s, "No app required", 10 * s, "#fff", 600, "middle")
    c.t(x + w / 2, qy + q + 37 * s, "Web purchase supported", 10 * s, "#fff", 600, "middle")
    # steps
    sy = cy + ch + 14 * s
    for i in range(2):
        yy = sy + i * 34 * s
        c.parts.append(f'<circle cx="{x+36*s}" cy="{yy+8*s}" r="{9*s}" fill="#721BFD"/>')
        c.t(x + 36 * s, yy + 12 * s, str(i + 1), 10 * s, "#fff", 700, "middle")
        if i == 0:
            c.parts.append(f'<rect x="{x+35.5*s}" y="{yy+17*s}" width="{1*s}" height="{16*s}" fill="#721BFD"/>')
        c.parts.append(f'<rect x="{x+56*s}" y="{yy+5*s}" width="{(150-i*30)*s}" height="{6*s}" rx="{3*s}" fill="#fff" fill-opacity="0.8"/>')
    c.parts.append(f'<rect x="{x}" y="{y+h-46*s}" width="{w}" height="{46*s}" fill="#fff" fill-opacity="0.1"/>')
    c.parts.append(f'<rect x="{x+w/2-80*s}" y="{y+h-26*s}" width="{160*s}" height="{5*s}" rx="{2.5*s}" fill="#fff" fill-opacity="0.5"/>')
    c.parts.append("</g>")
    return h


def door_right(c, x, y, wmax=560):
    """right column (spans 2 cols): title.. buttons. returns dict of positions"""
    c.t(x, y + 20, "Door Sales Poster", 24, FG, 700)
    d = ["Enable instant on-site purchases. Attendees can scan",
         "the poster to buy tickets directly on their mobile",
         "browser—no app download required."]
    for i, s in enumerate(d):
        c.t(x, y + 54 + i * 26, s, 16, FG)
    n = ["All sales generated via this poster are automatically",
         "tracked as “door_sales” in your ticket reports."]
    for i, s in enumerate(n):
        c.t(x, y + 150 + i * 24, s, 15, MFG)
    ly = y + 200
    c.t(x, ly + 22, "Poster Language", 14, FG, 500)
    sx = x + 128
    c.select(sx, ly, 200, value="English Only")
    by = ly + 52
    w1 = c.cta(x, by, "Download Poster (A3)", "download")
    w2 = c.btn(x + w1 + 16, by, "Download QR Code Only", "qr-code", outline=True)
    return dict(select=(sx, ly, 200, 36), b1=(x, by, w1, 36), b2=(x + w1 + 16, by, w2, 36), by=by)


def img_door_page():
    W, H = 900, 500
    c = K(W, H)
    c.page_header(20, 20, "Door Sales", "Generate QR codes and posters for on-site sales")
    mw = 176
    c.metric(20, 80, mw, "Total Scans", "860")
    c.metric(20 + mw + 32, 80, mw, "Tickets Sold", "120")
    c.metric(20 + 2 * (mw + 32), 80, mw, "Revenue", "3,250.00", "USD")
    gy = 196
    pw = 268
    poster(c, 20, gy, pw, maxy=H)
    r = door_right(c, 20 + pw + 24 + 24, gy)
    c.ring(r["select"][0] - 4, r["select"][1] - 4, r["select"][2] + 8, r["select"][3] + 8, 8)
    c.save(f"{OUT}/door-sales-page.svg")


def img_door_poster():
    W, H = 880, 440
    c = K(W, H)
    pw = 300
    poster(c, 20, 20, pw)
    r = door_right(c, 20 + pw + 40, 20)
    x, y, w, h = r["select"]
    c.ring(x - 4, y - 4, w + 8, h + 8, 8)
    c.callout(x + w + 24, y + 18, 1)
    x1, y1, w1, _ = r["b1"]
    x2, y2, w2, _ = r["b2"]
    c.ring(x1 - 4, y1 - 4, x2 + w2 - x1 + 8, 44, 8)
    c.callout(x2 + w2 + 24, y1 + 18, 2)
    c.save(f"{OUT}/door-sales-poster-preview.svg")


# =========================================================== AFFILIATES
def aff_table(c, x, y, w, rows, enrolled):
    cols = [("Ticket Type", 150), ("Price (USD)", 100), ("Commission Status", 160), ("Commission Type", 140),
            ("Amount/Ratio", 110), ("Commission (USD)", 140), ("", 50)]
    th, rh = 40, 56
    H = th + (rh * len(rows) if rows else 96)
    c.table_frame(x, y, w, H)
    cx = x
    for lab, cw in cols:
        c.t(cx + 8, y + 25, lab, 14, FG, 500)
        cx += cw
    if not rows:
        c.row_line(x, y + th, w)
        c.t(x + w / 2, y + th + 53, "Enroll in the affiliate program to configure commissions.", 14, MFG, 400, "middle")
        return H
    for r, row in enumerate(rows):
        yy = y + th + r * rh
        c.row_line(x, yy, w)
        cx = x
        for i, (lab, cw) in enumerate(cols):
            px = cx + 8
            cy = yy + rh / 2 + 5
            if i == 0:
                c.t(px, cy, row[0], 14, FG, 500)
            elif i in (1, 3, 4, 5):
                c.t(px, cy, row[i], 14)
            elif i == 2:
                c.select(px, yy + 10, 130, value=row[2], dot=GREEN if row[2] == "Active" else GRAY)
            else:
                c.dot_menu(cx + 4, yy + 10)
            cx += cw
    return H


def create_sm(c, x, y, disabled=False):
    w = int(12 * 2 + 16 + 8 + tw("Create", 14, 500))
    c.cta(x - w, y, "Create", "plus", h=32, w=w, disabled=disabled)
    return w


def img_aff_enroll():
    W, H = 900, 360
    c = K(W, H)
    c.t(20, 38, "Affiliates", 20, FG, 600)
    c.t(20, 62, "Unlock additional promotion and sales channels by rewarding PLVR Affiliates", 14, MFG)
    c.t(20, 82, "to sell your tickets", 14, MFG)
    bw = c.cta(W - 20 - 80, 20, "Enroll", w=80)
    c.ring(W - 20 - 80 - 4, 16, 88, 44, 8)
    c.parts.append('<g opacity="0.5">')
    c.t(20, 128, "Commission Settings", 16, FG, 600)
    aff_table(c, 20, 148, W - 40, [], False)
    create_sm(c, W - 20, 148 + 136 + 16)
    c.parts.append("</g>")
    c.h = 148 + 136 + 16 + 32 + 20
    c.parts[0] = f'<rect x="0" y="0" width="{W}" height="{c.h}" rx="0" fill="{BG}"/>'
    c.save(f"{OUT}/affiliates-enroll.svg")


def img_aff_table():
    W = 900
    c = K(W, 400)
    c.t(20, 38, "Affiliates", 20, FG, 600)
    c.t(20, 62, "Unlock additional promotion and sales channels by rewarding PLVR Affiliates", 14, MFG)
    c.t(20, 82, "to sell your tickets", 14, MFG)
    ew = 96
    c.cta(W - 20 - ew, 20, "Enrolled", w=ew, disabled=True)
    c.callout(W - 20 - ew - 20, 38, 1)
    c.t(20, 128, "Commission Settings", 16, FG, 600)
    rows = [("Early Bird", "25.00", "Active", "Percent", "10%", "2.50"),
            ("General Admission", "40.00", "Active", "Fixed", "USD 5.00", "5.00"),
            ("VIP Pass", "120.00", "Inactive", "Percent", "15%", "18.00")]
    H = aff_table(c, 20, 148, W - 40, rows, True)
    # fix row text mapping: price, status(select), type, amount, commission
    w = create_sm(c, W - 20, 148 + H + 16)
    c.callout(W - 20 - w - 22, 148 + H + 32, 2)
    c.h = 148 + H + 16 + 32 + 24
    c.parts[0] = f'<rect x="0" y="0" width="{W}" height="{c.h}" rx="0" fill="{BG}"/>'
    c.save(f"{OUT}/affiliates-commission-table.svg")


def img_aff_add():
    W, H = 700, 420
    c = K(W, H, DIM)
    dw = 384
    x = W - dw
    drawer(c, x, 0, dw, H, "Add Commission")
    p = x + 16
    iw = dw - 32
    c.t(p, 84, "Ticket Type*", 14, FG, 500)
    c.select(p, 92, iw, "General Admission")
    c.t(p, 148, "Ticket price: USD 40.00", 13, MFG)
    c.t(p, 186, "Commission Type*", 14, FG, 500)
    c.select(p, 194, iw, "Percent (%)")
    c.t(p, 262, "Percentage (%)*", 14, FG, 500)
    c.field(p, 270, iw, "10")
    c.t(p + iw - 14, 293, "%", 14, MFG, 400, "end")
    c.t(p, 326, "Recommended: 1–40%", 13, MFG)
    c.rect(x + 1, H - 76, dw - 1, 76, BG, 0)
    c.btn(p, H - 56, "Cancel", outline=True)
    c.cta(p + 81 + 8, H - 56, "Create")
    c.save(f"{OUT}/affiliates-add-commission.svg")


# =========================================================== TRACKING LINKS
def chan_pill(c, x, y, label, ic, selected):
    w = int(12 * 2 + 14 + 6 + tw(label, 14))
    if selected:
        c.rect(x, y, w, 32, FG, 16, FG)
        c.icon(ic, x + 12, y + 9, 14, BG)
        c.t(x + 12 + 20, y + 21, label, 14, BG)
    else:
        c.rect(x, y, w, 32, BG, 16, BORDER)
        c.icon(ic, x + 12, y + 9, 14, FG)
        c.t(x + 12 + 20, y + 21, label, 14, FG)
    return w


def label_help(c, x, y, s, star=False):
    c.t(x, y, s, 14, FG, 500)
    xx = x + tw(s, 14, 500) + 2
    if star:
        c.t(xx, y, "*", 14, FG, 500)
        xx += 8
    c.icon("circle-help", xx + 2, y - 10, 12, MFG)


def img_tl_builder():
    W, H = 900, 440
    c = K(W, H)
    c.rect(10, 10, W - 20, H - 20, CARD, 8, BORDER_CARD)
    x0 = 34
    c.t(x0, 52, "Link Builder", 16, FG, 600)
    c.icon("lightbulb", W - 34 - 16, 38, 16, MFG)
    # left column
    lw = W - 68 - 40 - 320
    label_help(c, x0, 92, "Channel", True)
    c.ring(x0 - 6, 74, 112, 28, 6)
    c.callout(x0 - 24, 90, 1)
    chans = [("Organic Social", "share-2"), ("Paid Social", "dollar-sign"), ("Messaging", "message-circle"),
             ("Email", "mail"), ("Paid Search", "search"), ("Affiliate", "users"), ("Referral", "globe"),
             ("Offline", "map-pinned")]
    px, py = x0, 108
    for i, (lab, ic) in enumerate(chans):
        w = int(24 + 14 + 6 + tw(lab, 14))
        if px + w > x0 + lw:
            px = x0
            py += 40
        chan_pill(c, px, py, lab, ic, i == 0)
        px += w + 8
    py += 40
    px = x0
    for lab in ["Facebook", "Instagram", "Twitter/X", "LinkedIn", "TikTok"]:
        w = int(24 + tw(lab, 14))
        if lab == "Instagram":
            c.parts.append(f'<rect x="{px}" y="{py}" width="{w}" height="32" rx="16" fill="{PRIM}" fill-opacity="0.1" stroke="{PRIM}"/>')
            c.t(px + 12, py + 21, lab, 14, PRIM)
        else:
            c.rect(px, py, w, 32, BG, 16, BORDER)
            c.t(px + 12, py + 21, lab, 14, FG)
        px += w + 8
    iy = py + 52
    label_help(c, x0, iy, "Campaign", True)
    c.field(x0, iy + 8, lw, "spring_sale_2024", icon_right="x")
    c.ring(x0 - 4, iy + 4, lw + 8, 44, 8)
    c.callout(x0 - 24, iy + 8, 2)
    iy += 76
    label_help(c, x0, iy, "Affiliate ID")
    c.field(x0, iy + 8, lw, "partner123", icon_right="x")
    c.ring(x0 - 4, iy + 4, lw + 8, 44, 8)
    c.callout(x0 - 24, iy + 8, 3)
    # right card
    rx = W - 34 - 320
    c.rect(rx, 74, 320, 290 - 44, CARD, 8, BORDER_CARD)
    c.t(rx + 16, 100, "Generated URL", 14, FG, 500)
    c.t(rx + 304, 100, "+4 params", 13, MFG, 400, "end")
    c.rect(rx + 16, 112, 288, 100, MUTED, 6)
    for i, s in enumerate(["https://plvr.io/events/10482?", "utm_source=instagram&", "utm_medium=social&", "utm_campaign=spring_sale_2024&", "aid=partner123"]):
        c.t(rx + 28, 132 + i * 17, s, 12.5, FG, 400, mono=True)
    c.btn(rx + 16, 224, "Copy", "copy", outline=True, h=32, w=240)
    c.rect(rx + 264, 224, 40, 32, INPUT_BG, 6, INPUT_BORDER)
    c.icon("external-link", rx + 276, 232, 16, FG)
    c.btn(rx + 16, 264, "Save to History", "plus", h=32, w=288)
    c.ring(rx + 12, 260, 296, 40, 8)
    c.callout(rx + 330 - 8, 280, 4)
    c.save(f"{OUT}/tracking-links-link-builder.svg")


def img_tl_history():
    W = 900
    c = K(W, 460)
    c.rect(10, 10, W - 20, 430, CARD, 8, BORDER_CARD)
    x0 = 34
    c.t(x0, 50, "Link History", 16, FG, 600)
    c.rect(x0 + 100, 38, 22, 16, MUTED, 4)
    c.t(x0 + 111, 50, "4", 11, MFG, 500, "middle")
    c.t(x0, 72, "Track performance of your generated links", 14, MFG)
    ty = 92
    cols = [("Label", 215, "s"), ("Destination URL", 225, "s"), ("Channel", 90, "s"), ("Clicks", 55, "e"),
            ("Unique Clicks", 110, "e"), ("Last Click", 80, "e"), ("", 60, "s")]
    tw_ = sum(w for _, w, _ in cols)
    # scale columns to inner width
    inner = W - 68
    k = inner / tw_
    cols = [(a, b * k, d) for a, b, d in cols]
    c.line(x0, ty + 40, x0 + inner, ty + 40)
    cx = x0
    for lab, cw, al in cols:
        if al == "e":
            c.t(cx + cw - 8, ty + 25, lab, 14, FG, 500, "end")
        else:
            c.t(cx + 8, ty + 25, lab, 14, FG, 500)
        cx += cw
    rows = [
        ("instagram - spring_sale_2024", "a1b2c3", ["https://plvr.io/events/10482?", "utm_source=instagram&utm_", "medium=social&utm_campaign=", "spring_sale_2024"], "Social", "instagram", "320", "210", "2h ago"),
        ("newsletter - launch_week", "d4e5f6", ["https://plvr.io/events/10482?", "utm_source=newsletter&utm_", "medium=email&utm_campaign=", "launch_week"], "Email", "newsletter", "180", "150", "1d ago"),
        ("flyer - city_posters", "g7h8i9", ["https://plvr.io/events/10482?", "utm_source=flyer&utm_", "medium=offline&utm_campaign=", "city_posters"], "Offline", "flyer", "45", "40", "3d ago"),
        ("tiktok - teaser_clip", "j0k1l2", ["https://plvr.io/events/10482?", "utm_source=tiktok&utm_", "medium=social&utm_campaign=", "teaser_clip&aid=partner123"], "Social", "tiktok", "95", "80", "Never"),
    ]
    rh = 84
    for r, row in enumerate(rows):
        yy = ty + 40 + r * rh
        cx = x0
        label, slug, dest, med, src, clk, uq, last = row
        c.t(cx + 8, yy + 38, label.split(" - ")[0] + " - " + label.split(" - ")[1], 13, FG, 500)
        c.t(cx + 8, yy + 57, f"https://plvr.io/t/{slug}", 12.5, MFG)
        cx += cols[0][1]
        for i, s in enumerate(dest):
            c.t(cx + 8, yy + 26 + i * 15, s, 12, MFG, 400, mono=True)
        cx += cols[1][1]
        c.t(cx + 8, yy + 38, med, 14, FG, 500)
        c.t(cx + 8, yy + 57, src.capitalize(), 12.5, MFG)
        cx += cols[2][1]
        for (lab, cw, al), s, wt in zip(cols[3:6], (clk, uq, last), (500, 500, 400)):
            c.t(cx + cw - 8, yy + 47, s, 14 if wt == 500 else 13, FG if wt == 500 else MFG, wt, "end")
            cx += cw
        c.icon("copy", cx + 8, yy + 32, 16, FG)
        c.icon("qr-code", cx + 40, yy + 32, 16, FG)
        c.line(x0, yy + rh, x0 + inner, yy + rh)
    fy = ty + 40 + 4 * rh + 28
    c.t(x0, fy, "Total Clicks:", 14, MFG)
    c.t(x0 + 94, fy, "640", 14, FG, 600)
    c.t(x0 + 160, fy, "Total Unique Clicks:", 14, MFG)
    c.t(x0 + 160 + 140, fy, "480", 14, FG, 600)
    c.h = fy + 36
    c.parts[0] = f'<rect x="0" y="0" width="{W}" height="{c.h}" rx="0" fill="{BG}"/>'
    c.parts[1] = f'<rect x="10" y="10" width="{W-20}" height="{c.h-20}" rx="8" fill="{CARD}" stroke="{BORDER_CARD}"/>'
    c.save(f"{OUT}/tracking-links-history.svg")


def img_tl_qr():
    W, H = 520, 500
    c = K(W, H, DIM)
    dw = 360
    x = (W - dw) / 2
    c.dialog(x, 20, dw, 460)
    c.t(x + 24, 56, "QR Code", 18, FG, 600)
    c.dialog_close(x + dw - 36, 40)
    cx = W / 2
    c.t(cx, 98, "instagram - spring_sale_2024", 14, FG, 600, "middle")
    c.t(cx, 120, "Social · instagram", 14, MFG, 400, "middle")
    c.rect(cx - 106, 134, 212, 212, "#fff", 8, BORDER)
    qr(c, cx - 90, 150, 180, seed=3)
    c.rect(x + 40, 362, 280, 40, MUTED, 6)
    c.t(x + 52, 387, "https://plvr.io/t/a1b2c3", 12.5, MFG, 400, mono=True)
    c.btn(x + 40, 418, "Copy QR Code", "copy", outline=True, h=32, w=134, pad=8)
    c.btn(x + 186, 418, "Download PNG", "download", h=32, w=134, pad=8)
    c.save(f"{OUT}/tracking-links-qr-dialog.svg")


# =========================================================== CAMPAIGNS
def img_camp_overview():
    W = 900
    c = K(W, 420)
    c.page_header(20, 20, "Campaigns", "Send email campaigns to your attendees")
    bx, by, bw, bh = 20, 80, 236, 104
    c.rect(bx, by, bw, bh, MUTED, 6)
    c.icon("mail", bx + 8, by + 18, 16, MFG)
    c.t(bx + 32, by + 31, "Email Blast", 14, MFG, 700)
    c.t(bx + 8, by + 60, "Remaining Blasts: 2", 14, MFG)
    c.icon("info", bx + 8 + tw("Remaining Blasts: 2", 14) + 8, by + 48, 16, MFG)
    c.t(bx + 8, by + 90, "Send emails >", 14, BTN, 700)
    c.t(20, 232, "Emails (4)", 24, FG, 700)
    ty = 252
    cols = [("Campaign Name", 230), ("Status", 120), ("Recipients", 100), ("Open Rate", 90), ("Click Rate", 90), ("Revenue", 140), ("", 50)]
    th, rh = 40, 64
    rows = [("Launch announcement", "Sent on Oct 2, 2026, 10:00 AM", "sent", "320", "42.5%", "6.1%", "USD 1,240.00"),
            ("Lineup reveal", "Sent on Oct 9, 2026, 6:30 PM", "sent", "310", "38.2%", "5.4%", "USD 860.00"),
            ("Last call", None, "sending", "335", "--", "--", "--"),
            ("Early bird reminder", "Sent on Sep 25, 2026, 9:00 AM", "sent", "280", "45.0%", "7.3%", "USD 1,980.00")]
    H = th + rh * len(rows)
    inner = W - 40
    c.table_frame(20, ty, inner, H)
    cx = 20
    for lab, cw in cols:
        c.t(cx + 8, ty + 25, lab, 14, FG, 500)
        cx += cw
    for r, row in enumerate(rows):
        yy = ty + th + r * rh
        c.row_line(20, yy, inner)
        cx = 20
        name, sub, st, rec, o, k_, rev = row
        c.t(cx + 8, yy + (28 if sub else 38), name, 14, FG, 500)
        if sub:
            c.t(cx + 8, yy + 48, sub, 13, MFG)
        cx += cols[0][1]
        if st == "sent":
            c.pill(cx + 8, yy + 20, "Sent", GREEN, "check")
        else:
            c.pill(cx + 8, yy + 20, "Sending", ORANGE500, "circle-dashed")
        cx += cols[1][1]
        for (lab, cw), s in zip(cols[2:6], (rec, o, k_, rev)):
            c.t(cx + 8, yy + 37, s, 14)
            cx += cw
        c.icon("eye", cx + 12, yy + 24, 16, FG)
    c.h = ty + H + 24
    c.parts[0] = f'<rect x="0" y="0" width="{W}" height="{c.h}" rx="0" fill="{BG}"/>'
    c.save(f"{OUT}/campaigns-overview.svg")


def editor(c, x, y, w, with_chip_button=True, body_h=110):
    c.rect(x, y, w, 44 + body_h, INPUT_BG, 6, INPUT_BORDER)
    c.line(x, y + 44, x + w, y + 44, BORDER)
    c.rect(x + 8, y + 8, 32, 28, MUTED, 6)  # bold shown active? keep ghost
    c.parts.pop()
    c.icon("bold", x + 16, y + 14, 16, FG)
    c.icon("italic", x + 56, y + 14, 16, FG)
    c.line(x + 80, y + 10, x + 80, y + 34, BORDER_CARD)
    c.icon("image", x + 100, y + 14, 16, FG)
    ty = y + 44 + 30
    c.t(x + 16, ty, "Hi", 14)
    nx = x + 16 + tw("Hi", 14) + 6
    c.rect(nx, ty - 18, 52, 24, "#ec808d", 6)
    c.t(nx + 26, ty - 1, "Name", 14, "#fff", 500, "middle")
    c.t(nx + 54, ty, ",", 14)
    c.t(x + 16, ty + 24, "Doors for Neon Nights open at 9 PM. Early bird tickets end Friday.", 14)
    if with_chip_button:
        c.rect(x + 16, ty + 44, 122, 36, "#3b82f6", 18)
        c.t(x + 77, ty + 67, "Get tickets", 14, "#fff", 600, "middle")


def img_camp_form():
    W = 900
    c = K(W, 700, MUTED)
    x0, iw = 20, 860
    c.icon("chevron-left", 28, 24, 20, FG)
    c.t(60, 44, "New Email Campaign", 24, FG, 700)
    stw = int(32 + tw("Send test", 14, 500))
    sew = int(48 + tw("Send email", 14, 500))
    c.cta(W - 20 - sew, 20, "Send email", "play", w=sew)
    c.cta(W - 20 - sew - 12 - stw, 20, "Send test", outline=True, w=stw)
    c.ring(W - 20 - sew - 12 - stw - 4, 16, stw + 8, 44, 8)
    c.callout(W - 20 - sew - 12 - stw - 4, 16, 3)
    c.ring(W - 20 - sew - 4, 16, sew + 8, 44, 8)
    c.callout(W - 20 - sew - 4, 16, 4)
    c.line(20, 76, W - 20, 76, BORDER_CARD)
    y = 100
    c.t(x0, y + 14, "Campaign Name", 14, FG, 500)
    c.t(x0 + tw("Campaign Name", 14, 500) + 4, y + 14, "*", 14, RED, 500)
    c.field(x0, y + 24, iw, "Launch announcement")
    c.t(x0, y + 82, "For your internal review/identification only (not shown to recipients)", 14, MFG)
    y += 114
    c.t(x0, y + 14, "Recipients", 14, FG, 500)
    c.t(x0 + tw("Recipients", 14, 500) + 4, y + 14, "*", 14, RED, 500)
    c.t(x0, y + 38, "Who are you sending this campaign to?", 14, MFG)
    aw = c.btn(x0, y + 50, "Add Recipients", outline=True)
    c.ring(x0 - 4, y + 46, aw + 8, 44, 8)
    c.callout(x0 + aw + 4, y + 46, 1)
    c.t(x0, y + 116, "To: Ticket Buyers; Interested (No Purchase)", 14)
    ey = y + 128
    s1 = "This campaign will be sent to 405 recipients"
    w1 = int(12 + 16 + 8 + tw(s1, 14) + 12 - 40)
    c.rect(x0, ey, 366, 26, CARD, 8, GREEN)
    c.icon("mail", x0 + 12, ey + 5, 16, FG)
    c.rich(x0 + 36, ey + 18, [("This campaign will be sent to ", 400), ("405", 700), (" recipients", 400)])
    c.rect(x0 + 378, ey, 288, 26, CARD, 8, ORANGE500)
    c.icon("clock", x0 + 390, ey + 5, 16, FG)
    c.t(x0 + 414, ey + 18, "Estimated send time: 5 minutes", 14)
    y += 180
    c.t(x0, y + 14, "Email Subject", 14, FG, 500)
    c.t(x0 + tw("Email Subject", 14, 500) + 4, y + 14, "*", 14, RED, 500)
    c.field(x0, y + 24, iw, "Doors open at 9 PM, tickets still available")
    y += 84
    c.t(x0, y + 14, "Email Content", 14, FG, 500)
    c.t(x0 + tw("Email Content", 14, 500) + 4, y + 14, "*", 14, RED, 500)
    editor(c, x0, y + 24, iw, True, 120)
    c.ring(x0 - 3, y + 21, iw + 6, 50, 6)
    c.callout(x0 - 8, y + 24, 2)
    by = y + 24 + 44 + 120 + 12
    w1 = c.btn(x0, by, "Insert Name", "user", outline=True, h=32)
    c.btn(x0 + w1 + 8, by, "Edit Button", "link-2", outline=True, h=32)
    c.h = by + 32 + 24
    c.parts[0] = f'<rect x="0" y="0" width="{W}" height="{c.h}" rx="0" fill="{MUTED}"/>'
    c.save(f"{OUT}/campaigns-new-form.svg")


def img_camp_ready():
    W, H = 640, 260
    c = K(W, H, DIM)
    dw = 512
    x = (W - dw) / 2
    c.dialog(x, 20, dw, 220)
    c.dialog_close(x + dw - 36, 40)
    c.t(x + 24, 60, "\U0001F389 Ready to Go", 18, FG, 600)
    c.rich(x + 24, 100, [("You are about to send your campaign to ", 400), ("405 recipients", 600), (" with one click", 400)], fill="#9ca3af")
    sw = int(32 + tw("Send", 14, 500))
    cw = int(32 + tw("Cancel", 14, 500))
    c.cta(x + dw - 24 - sw, 190 - 4, "Send", w=sw)
    c.btn(x + dw - 24 - sw - 8 - cw, 190 - 4, "Cancel", outline=True, w=cw)
    c.save(f"{OUT}/campaigns-ready-to-go.svg")


def img_camp_recipients():
    W, H = 740, 520
    c = K(W, H, DIM)
    dw = 672
    x = (W - dw) / 2
    c.dialog(x, 16, dw, 488)
    c.t(x + 24, 54, "Add Recipients", 18, FG, 600)
    c.dialog_close(x + dw - 36, 36)
    bx, by, bw, bh = x + 24, 74, dw - 48, 340
    c.rect(bx, by, bw, bh, BG, 0, BORDER_CARD)
    # tabs
    c.rect(bx + 16, by + 16, 160, 36, MUTED, 6)
    c.t(bx + 28, by + 39, "Recommendation", 14, FG, 500)
    c.t(bx + 28, by + 39 + 40, "Custom", 14, MFG, 500)
    c.line(bx + 192, by, bx + 192, by + bh, BORDER_CARD)
    gx = bx + 192 + 24
    gw = bw - 192 - 24 - 24
    groups = [("Ticket Buyers", "(320)", "Everyone who bought a ticket", "sel"),
              ("Pending RSVPs", "(0)", "People who RSVP'd but haven't been approved", "dis"),
              ("Interested (No Purchase)", "(85)", "People who marked “Interested” but didn't buy", "")]
    gy = by + 32
    for lab, cnt, desc, st in groups:
        op = 0.5 if st == "dis" else 1
        c.parts.append(f'<g opacity="{op}">')
        c.rect(gx, gy, gw, 76, BG, 8, BTN if st == "sel" else BORDER_CARD)
        if st == "sel":
            c.parts.append(f'<rect x="{gx+1}" y="{gy+1}" width="{gw-2}" height="74" rx="7" fill="none" stroke="{BTN}" stroke-width="1.5"/>')
        c.t(gx + 16, gy + 30, lab, 14, FG, 600)
        c.t(gx + 16 + tw(lab, 14, 400) + 6, gy + 30, cnt, 14, MFG)
        c.t(gx + 16, gy + 54, desc, 14, MFG)
        c.parts.append("</g>")
        gy += 88
    # footer
    fy = by + bh + 22
    c.icon("mail", x + 24, fy, 16, FG)
    c.rich(x + 48, fy + 13, [("This campaign will be sent to ", 400), ("320", 700), (" recipients", 400)])
    c.icon("clock", x + 24, fy + 26, 16, FG)
    c.t(x + 48, fy + 39, "Estimated send time: 4 minutes", 14)
    sw = int(32 + tw("Save", 14, 500))
    c.cta(x + dw - 24 - sw, fy + 6, "Save", w=sw)
    c.save(f"{OUT}/campaigns-add-recipients.svg")


def img_camp_toolbar():
    W, H = 760, 230
    c = K(W, H, MUTED)
    editor(c, 20, 20, W - 40, False, 100)
    by = 20 + 44 + 100 + 12
    w1 = c.btn(20, by, "Insert Name", "user", outline=True, h=32)
    c.btn(20 + w1 + 8, by, "Add Button", "link-2", outline=True, h=32)
    c.h = by + 32 + 20
    c.parts[0] = f'<rect x="0" y="0" width="{W}" height="{c.h}" rx="0" fill="{MUTED}"/>'
    c.save(f"{OUT}/campaigns-editor-toolbar.svg")


def img_camp_button():
    W, H = 640, 400
    c = K(W, H, DIM)
    dw = 512
    x = (W - dw) / 2
    c.dialog(x, 20, dw, 360)
    c.dialog_close(x + dw - 36, 40)
    c.t(x + 24, 58, "Add Button", 18, FG, 600)
    c.t(x + 24, 82, "The button will be shown at the bottom of your email content", 14, MFG)
    iw = dw - 48
    c.t(x + 24, 124, "Button Text*", 14, FG, 500)
    c.field(x + 24, 132, iw, "Get tickets")
    c.t(x + dw - 24, 188, "11/50", 14, MFG, 400, "end")
    c.t(x + 24, 220, "Link to*", 14, FG, 500)
    c.select(x + 24, 228, iw, "Event Page")
    c.t(x + 24, 284, "Track clicks and revenue when linked to your event page", 14, MFG)
    sw = int(32 + tw("Save", 14, 500))
    c.cta(x + dw - 24 - sw, 318, "Save", w=sw)
    c.save(f"{OUT}/campaigns-add-button.svg")


if __name__ == "__main__":
    for f in [img_promo_list, img_promo_create, img_promo_usage, img_door_page, img_door_poster,
              img_aff_enroll, img_aff_table, img_aff_add, img_tl_builder, img_tl_history, img_tl_qr,
              img_camp_overview, img_camp_form, img_camp_ready, img_camp_recipients, img_camp_toolbar,
              img_camp_button]:
        f()
