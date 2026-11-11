import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from tap_kit import *

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "tap")
os.makedirs(OUT, exist_ok=True)


def wrap(s, width, size=14):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, size) > width and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    return lines


def section_head(c, x, y, w, title, desc, right=None):
    """h2 font-semibold + muted description (left), buttons right (items-start)."""
    c.text(x, y + 10, title, 16, FG, 600)
    avail = w - (right or 0) - 24
    for i, ln in enumerate(wrap(desc, avail)):
        c.text(x, y + 34 + i * 20, ln, 14, MFG)
    return 34 + len(wrap(desc, avail)) * 20


# ---------------------------------------------------------------- sidebar
def sidebar():
    SW, H, OX = 256, 592, 150
    W = SW
    c = T(SW + 2 * OX, H, BG)
    c.rect(OX, 0, SW, H, CARD, 0)
    c.line(OX + SW - .5, 0, OX + SW - .5, H)
    c.parts.append(f'<g transform="translate({OX} 0)">')
    x0 = 24  # pl-6
    # event header
    c.rect(x0, 20, 56, 56, "#a3a3a3", 4)
    c.text(x0 + 68, 38, "Neon Nights", 14, FG, 700)
    c.text(x0 + 68, 60, "View event", 14, BTN)
    c.icon("external-link", x0 + 68 + tw("View event", 14) + 5, 53, 14, BTN)
    y = 96

    def item(label, icon, chev=None, active=False):
        nonlocal y
        if active:
            c.rect(x0, y, W - x0 - 8, 32, MUTEDBG, 6)
        c.icon(icon, x0 + 8, y + 8, 16, FG)
        c.text(x0 + 34, y + 16, label, 14, FG)
        if chev:
            c.icon("chevron-right", W - 8 - 28, y + 8, 16, FG) if chev == "r" else c.icon("chevron-right", W - 36, y + 8, 16, FG)
        y += 40
        return y - 40

    def group_open(label, icon, subs, active_sub=None, badge=None):
        nonlocal y
        gy = y
        c.icon(icon, x0 + 8, y + 8, 16, FG)
        c.text(x0 + 34, y + 16, label, 14, FG)
        # open chevron rotated 90deg
        c.parts.append(f'<g transform="rotate(90 {W-36+8} {y+16})">')
        c.icon("chevron-right", W - 36, y + 8, 16, FG)
        c.parts.append("</g>")
        y += 32 + 4
        sx = x0 + 14 + 10          # mx-3.5 px-2.5
        top = y
        for s in subs:
            if s == active_sub:
                c.rect(sx, y, W - 8 - sx, 28, MUTEDBG, 6)
            c.text(sx + 8, y + 14, s, 14, FG)
            if badge and s == badge[0]:
                bx = sx + 8 + tw(s, 14) + 8
                bw = max(20, tw(str(badge[1]), 13, 500) + 12)
                c.rect(bx, y + 4, bw, 20, BTN, 10)
                c.text(bx + bw / 2, y + 14, str(badge[1]), 13, BTN_FG, 500, "middle")
            y += 32
        c.line(x0 + 14, gy + 32, x0 + 14, y - 4, MUTEDBG)
        y += 4 + 4
        return gy, y

    item("Overview", "chart-line")
    item("Event Editor", "pencil-line")
    item("Tickets", "ticket", "r")
    gy, ge = group_open("PLVR Tap", "nfc",
                        ["Top-up Setup", "Vendor Setup", "Approvals", "Cashless Activity", "Spending Report"],
                        badge=("Approvals", 2))
    item("Onsite Operations", "headset")
    item("Onsite Staff", "user-cog")
    item("Promotions", "tag", "r")
    item("Personalization Form", "fingerprint")
    c.ring(6, gy - 6, W - 14, ge - gy + 2, 8)
    c.parts.append("</g>")
    c.save(f"{OUT}/tap-event-sidebar.svg")




# ---------------------------------------------------------------- top-up setup
def tab_bar(c, x, y, active):
    return c.tabs(x, y, ["Top-up Stations", "Onsite Payment Methods"], active)


def stations_tab():
    W = 700
    c = T(W, 10)
    X, IW = 20, W - 40
    tab_bar(c, X, 20, 0)
    y = 80
    btn_w = tw("Add Top-up Station", 14, 500) + 24 + 32
    hh = section_head(c, X, y, IW, "Top-up Stations",
                      "Create locations for assigning Top-up Staff and tracking onsite top-ups.", btn_w)
    c.btn(X + IW - btn_w, y - 8, "Add Top-up Station", "cta", icon="plus")
    ty = y + hh + 14
    rows = [("Main Entrance", "Front gate, cash and card", "Active"),
            ("VIP Lounge", "Priority top-ups for VIP guests", "Active"),
            ("Side Gate", "Open on day two only", "Inactive")]
    cx, cw, ry, th = c.table(X, ty, IW, [170, None, 140, 60], ["Name", "Description", "Status", ""], [53] * 3)
    for (n, d, st), r in zip(rows, ry):
        c.text(cx[0] + 8, r + 26.5, n, 14)
        c.text(cx[1] + 8, r + 26.5, d, 14)
        c.select(cx[2] + 8, r + 8.5, cw[2] - 16, st, GREEN if st == "Active" else GRAY)
        c.icon_btn(cx[3] + 8, r + 8.5, "pencil")
    c.h = ty + th + 20
    c.rect(0, 0, 0, 0)
    c.save(f"{OUT}/tap-topup-stations-tab.svg")


def drawer_scene(name, W, PW, title, build, cancel, primary, backdrop=None, min_h=0, fixed_h=None, border=True):
    """Right drawer PW wide on a dimmed page. build(c, x, y, w) draws fields and returns the bottom y."""
    probe = T(W, 10)
    bottom = build(probe, 0, 72, PW - 40)
    H = fixed_h or max(int(bottom + 28 + 72), min_h)
    c = T(W, H)
    if backdrop:
        backdrop(c)
    c.dim(0, 0, W, H)
    px = W - PW
    c.drawer_panel(px, 0, PW, H, title)
    build(c, px + 20, 72, PW - 40)
    c.drawer_footer(px, 0, PW, H, cancel, primary, border)
    c.save(f"{OUT}/{name}.svg")


def page_skeleton(c, x, y, w):
    """Dim, unlabelled stand-in for the page behind a drawer."""
    for i in range(6):
        c.rect(x, y + i * 54, w, 38, CARD, 6)


def station_panel():
    def build(c, x, y, w):
        c.label(x, y + 7, "Name*")
        c.input(x, y + 22, w, value="Main Entrance")
        y += 22 + 36 + 24
        c.label(x, y + 7, "Description")
        c.textarea(x, y + 22, w, 64, value="Front gate, cash and card")
        c.text(x + w, y + 22 + 64 + 14, "25/200 characters", 14, MFG, anchor="end")
        y += 22 + 64 + 28 + 24
        c.label(x, y + 7, "Status*")
        c.select(x, y + 22, w, "Active")
        ls = wrap("Inactive stations are hidden in PLVR Onsite but remain available for staff assignment.", w)
        for i, ln in enumerate(ls):
            c.text(x, y + 22 + 36 + 16 + i * 20, ln, 14, MFG)
        return y + 22 + 36 + 16 + len(ls) * 20
    drawer_scene("tap-topup-create-station-panel", 640, 500, "Create Top-up Station", build,
                 "Cancel", "Create Station", lambda c: page_skeleton(c, 20, 20, 100))


def payment_methods_tab():
    W = 700
    c = T(W, 10)
    X, IW = 20, W - 40
    tab_bar(c, X, 20, 1)
    y = 80
    hh = section_head(c, X, y, IW, "Onsite Payment Methods",
                      "These options are used for reporting only and do not process payments.")
    y += hh + 14
    # quick add (flex-wrap) + custom CTA on the right
    c.text(X, y + 18, "Quick add", 14, MFG, 500)
    bx = X + tw("Quick add", 14, 500) + 8
    cta_w = tw("Custom Payment Method", 14, 500) + 24 + 32
    limit = X + IW - cta_w - 16
    by = y
    for lab, ic in [("QR Payment", "qr-code"), ("Bank Transfer", "landmark"), ("Other", "more-horizontal")]:
        bw = tw(lab, 14, 500) + 24 + 32
        if bx + bw > limit:
            bx, by = X, by + 44
        c.btn(bx, by, lab, "outline", icon=ic)
        bx += bw + 8
    c.btn(X + IW - cta_w, y, "Custom Payment Method", "cta", icon="plus")
    ty = by + 36 + 20
    rows = [("Cash", "System"), ("Card", "System"), ("Apple Pay", "Custom")]
    cx, cw, ry, th = c.table(X, ty, IW, [None, 140, 60], ["Payment Method", "Status", ""], [53] * 3)
    for (n, kind), r in zip(rows, ry):
        c.text(cx[0] + 8, r + 18, n, 14)
        c.text(cx[0] + 8, r + 37, kind, 13, MFG)
        c.select(cx[1] + 8, r + 8.5, cw[1] - 16, "Active", GREEN)
        if kind == "Custom":
            c.icon_btn(cx[2] + 8, r + 8.5, "pencil")
    c.h = ty + th + 20
    c.save(f"{OUT}/tap-topup-payment-methods-tab.svg")




# ---------------------------------------------------------------- vendors
def uploader(c, x, y, w, filled=True):
    """CroppableImageUploader: 112px box + outline button + hint."""
    c.rect(x + .5, y + .5, 111, 111, "#ffffff", 8, INPUT_B, op=0.03)
    if filled:
        c.thumb(x + 1, y + 1, 110, 0)
        c.circle(x + 112 - 14, y + 14, 10, DEST)
        c.icon("x", x + 112 - 20, y + 8, 12, "#ffffff", 2.5)
        c.btn(x + 124, y + 38, "Replace Image", "outline", icon="upload")
    else:
        c.icon("image", x + 40, y + 40, 32, MFG, 1.5)
        c.btn(x + 124, y + 38, "Upload Image", "outline", icon="upload")
    ls = wrap("Drag and drop an image here, or upload a JPG, PNG, or WebP file up to 5 MB. You can crop it to 1:1 after uploading.", w)
    for i, ln in enumerate(ls):
        c.text(x, y + 112 + 18 + i * 20, ln, 14, MFG)
    return y + 112 + 8 + len(ls) * 20


def vendor_list():
    W = 880
    c = T(W, 10)
    X, IW = 20, W - 40
    c.text(X, 27, "Search", 14, FG, 500)
    c.input(X, 42, 280, placeholder="Search by vendor name")
    addw = tw("Add Vendor", 14, 500) + 24 + 32
    c.btn(X + IW - addw, 42, "Add Vendor", "cta", icon="plus")
    ty = 98
    rows = [("Taco Cart", "Active", 2, 6, 3), ("Craft Bar", "Active", 3, 12, 4), ("Noodle House", "Active", 1, 8, 2),
            ("Merch Table", "Inactive", 1, 5, 1), ("Cold Brew Stand", "Active", 1, 4, 2), ("Pizza Slice", "Active", 2, 7, 3)]
    cx, cw, ry, th = c.table(X, ty, IW, [None, 140, 140, 100, 120, 170],
                             ["Vendor Name", "Status", "Sales Locations", "Items", "Login Codes", ""], [53] * len(rows))
    for (n, st, a, b, d), r in zip(rows, ry):
        c.avatar(cx[0] + 8, r + 10.5, n[0])
        c.text(cx[0] + 48, r + 26.5, n, 14, FG, 500)
        c.select(cx[1] + 8, r + 8.5, cw[1] - 16, st, GREEN if st == "Active" else GRAY)
        for i, v in zip((2, 3, 4), (a, b, d)):
            c.text(cx[i] + 8, r + 26.5, str(v), 14)
        ex = cx[5] + cw[5] - 8
        c.text(ex - 18, r + 26.5, "View Details", 14, MFG, anchor="end")
        c.icon("arrow-right", ex - 14, r + 19.5, 14, MFG)
        c.icon_btn(ex - 18 - tw("View Details", 14) - 8 - 36, r + 8.5, "pencil")
    c.ring(X + IW - addw - 4, 38, addw + 8, 44, 8)
    c.callout(X + IW - addw - 4, 38, 1)
    c.h = ty + th + 20
    c.save(f"{OUT}/tap-vendor-list.svg")


def vendor_panel():
    def build(c, x, y, w):
        c.label(x, y + 7, "Vendor Image", "Optional", x + w)
        y2 = uploader(c, x, y + 22, w)
        y = y2 + 24
        c.label(x, y + 7, "Name*")
        c.input(x, y + 22, w, value="Craft Bar")
        y += 22 + 36 + 24
        c.label(x, y + 7, "Note")
        c.textarea(x, y + 22, w, 64, value="Cocktails and craft beer")
        c.text(x + w, y + 22 + 64 + 14, "24/200 characters", 14, MFG, anchor="end")
        y += 22 + 64 + 28 + 24
        c.label(x, y + 7, "Status*")
        c.select(x, y + 22, w, "Active")
        c.text(x, y + 22 + 36 + 16, "Inactive vendors are unavailable for login and new orders.", 14, MFG)
        return y + 22 + 36 + 28
    drawer_scene("tap-vendor-create-panel", 640, 500, "Create Vendor", build, "Cancel", "Create Vendor",
                 lambda c: page_skeleton(c, 20, 20, 100))


def vendor_detail():
    W = 860
    c = T(W, 10)
    X, IW = 20, W - 40
    c.icon("chevron-left", X, 22, 16, MFG)
    c.text(X + 18, 30, "Vendor Setup", 14, MFG)
    c.text(X, 68, "Craft Bar", 20, FG, 600)
    c.badge(X + tw("Craft Bar", 20, 600) + 12, 68, "Active", "default")
    c.text(X, 96, "Manage sales locations, items, and login codes for this vendor.", 14, MFG)
    pos, _ = c.tabs(X, 130, ["Sales Locations", "Items", "Login Codes"], 1)
    y = 190
    bw = [tw("Export", 14, 500) + 24 + 32, tw("Add Category", 14, 500) + 24 + 32, tw("Add Item", 14, 500) + 24 + 32]
    total = sum(bw) + 16
    bx = X + IW - total
    c.btn(bx, y - 8, "Export", "outline", icon="download")
    c.btn(bx + bw[0] + 8, y - 8, "Add Category", "outline", icon="plus")
    c.btn(bx + bw[0] + bw[1] + 16, y - 8, "Add Item", "cta", icon="plus")
    c.text(X, y + 10, "Items (2)", 16, FG, 600)
    ls = wrap("Create and manage categories and items across this vendor's sales locations.", IW - total - 24)
    for i, ln in enumerate(ls):
        c.text(X, y + 34 + i * 20, ln, 14, MFG)
    fy = y + 34 + len(ls) * 20 + 20 + 4
    # filters
    c.text(X, fy + 7, "Sales Location", 14, FG, 500)
    c.select(X, fy + 22, 200, "All Locations")
    c.text(X + 212, fy + 7, "Category", 14, FG, 500)
    c.select(X + 212, fy + 22, 200, "All Categories")
    c.text(X + 424, fy + 7, "Search", 14, FG, 500)
    c.input(X + 424, fy + 22, 260, placeholder="Search by item name", icon="search")
    ty = fy + 58 + 20
    cx, cw, ry, th = c.table(X, ty, IW, [None, None, 100, 140, 60],
                             ["Name", "Sales Locations", "Price (USD)", "Status", ""], [40, 53, 53])
    # category group row
    c.rect(X + 1, ry[0], IW - 2, 40, MUTEDBG, 0, op=0.5)
    c.parts.append(f'<g transform="rotate(90 {X+16} {ry[0]+20})">')
    c.icon("chevron-right", X + 8, ry[0] + 12, 16, FG)
    c.parts.append("</g>")
    c.text(X + 28, ry[0] + 20, "Cocktails (2)", 14, FG, 500)
    c.icon("pencil", X + 28 + tw("Cocktails (2)", 14, 500) + 14, ry[0] + 13, 14, FG)
    for (n, loc, pr), r in zip([("Mojito", "Main Bar +1", "9.00"), ("Margarita", "Main Bar", "11.00")], ry[1:]):
        c.avatar(cx[0] + 8, r + 10.5, n[0])
        c.text(cx[0] + 48, r + 26.5, n, 14)
        c.text(cx[1] + 8, r + 26.5, loc, 14)
        c.text(cx[2] + 8, r + 26.5, pr, 14)
        c.select(cx[3] + 8, r + 8.5, cw[3] - 16, "Active", GREEN)
        c.icon_btn(cx[4] + 8, r + 8.5, "pencil")
    # selected tab is "Items"
    c.h = ty + th + 20
    c.save(f"{OUT}/tap-vendor-detail-tabs.svg")


def vendor_item_form():
    def build(c, x, y, w):
        c.label(x, y + 7, "Sales Locations*")
        c.rect(x + .5, y + 22.5, w - 1, 40 - 1, "#ffffff", 6, INPUT_B, op=0.045)
        bx = x + 12
        for n in ("Main Bar", "Patio Bar"):
            bw = tw(n, 13, 500) + 18 + 16
            c.rect(bx, y + 22 + 9, bw, 22, MUTEDBG, 6)
            c.text(bx + 9, y + 22 + 20, n, 13, FG, 500)
            c.icon("x", bx + bw - 21, y + 22 + 14, 12, FG)
            bx += bw + 4
        c.icon("chevrons-up-down", x + w - 28, y + 22 + 12, 16, MFG, op=0.7)
        c.text(x, y + 22 + 40 + 16, "Select all Sales Locations where this item is sold.", 14, MFG)
        y += 22 + 40 + 28 + 24
        c.label(x, y + 7, "Category")
        c.select(x, y + 22, w, "Cocktails")
        y += 22 + 36 + 24
        c.label(x, y + 7, "Item Name*")
        c.input(x, y + 22, w, value="Mojito")
        y += 22 + 36 + 24
        c.label(x, y + 7, "Price (USD)*")
        c.input(x, y + 22, w, value="9")
        c.text(x, y + 22 + 36 + 16, "Deducted from the attendee's event balance.", 14, MFG)
        return y + 22 + 36 + 28
    drawer_scene("tap-vendor-add-item-form", 640, 500, "Create Item", build, "Cancel", "Create Item",
                 lambda c: page_skeleton(c, 20, 20, 100))


def vendor_login_codes():
    def build(c, x, y, w):
        c.label(x, y + 7, "Vendor")
        c.input(x, y + 22, w, value="Craft Bar", disabled=True)
        y += 22 + 36 + 24
        c.label(x, y + 7, "Number of Login Codes*")
        c.input(x, y + 22, w, value="3")
        y += 22 + 36 + 24
        c.label(x, y + 7, "Note")
        c.input(x, y + 22, w, value="Alex - Vendor Manager")
        c.text(x, y + 22 + 36 + 16, "Applied to every code in this batch.", 14, MFG)
        y += 22 + 36 + 28 + 24
        c.label(x, y + 7, "Status*")
        c.select(x, y + 22, w, "Active")
        c.text(x, y + 22 + 36 + 16, "Inactive login codes cannot sign in or perform new actions.", 14, MFG)
        return y + 22 + 36 + 28
    drawer_scene("tap-vendor-login-codes", 640, 500, "Create Vendor Login Code", build, "Cancel", "Generate Codes",
                 lambda c: page_skeleton(c, 20, 20, 100))



# ---------------------------------------------------------------- approvals
FG80 = "#cbcbcb"


def meta_line(c, x, cy, label, value):
    c.text(x, cy, label + ":", 14, MFG)
    c.text(x + tw(label + ": ", 14) + 3, cy, value, 14, FG80)


def submission_cell(c, x, r, name, typ, item_id, vendor, when):
    y = r + 20
    c.text(x, y + 12, name, 14, FG, 600)
    c.badge(x + tw(name, 14, 600) + 10, y + 12, "Pending", "pending")
    c.text(x, y + 36, typ, 14, MFG)
    y += 24 + 22 + 12
    meta_line(c, x, y + 10, "Item ID", item_id)
    meta_line(c, x, y + 34, "Submitted by", vendor)
    meta_line(c, x, y + 58, "Submitted at", when)


def changed_field(c, x, y, label, cur, req):
    c.text(x, y + 10, label, 14, FG, 500)
    c.text(x, y + 38, "Current", 14, MFG)
    c.text(x + 156, y + 38, cur, 14, FG)
    c.text(x, y + 66, "Requested", 14, BTN)
    c.text(x + 156, y + 66, req, 14, FG, 600)
    return y + 76


def submitted_field(c, x, y, label, val):
    c.text(x, y + 12, label, 14, MFG)
    c.text(x + 156, y + 12, val, 14, FG, 600)


def approvals_head_checkbox(c, cx, y, checked=False):
    c.checkbox(cx[0] + 8, y + 12, checked)


def approvals_list():
    W = 1000
    c = T(W, 10)
    X, IW = 20, W - 40
    fx = X
    for lab, w, val in (("Vendor", 220, "All Vendors"), ("Status", 180, "Pending"), ("Type", 180, "All Types")):
        c.text(fx, 27, lab, 14, FG, 500)
        c.select(fx, 42, w, val)
        fx += w + 16
    c.text(fx, 27, "Search", 14, FG, 500)
    c.input(fx, 42, X + IW - fx, placeholder="Search by name, item ID, category ID, or submission ID", icon="search")
    c.ring(X - 6, 14, IW + 12, 72, 10)
    c.callout(X - 6, 14, 1)
    c.text(X + IW, 108, "2 submissions \u00b7 Newest first", 14, MFG, anchor="end")
    ty = 138
    cx, cw, ry, th = c.table(X, ty, IW, [52, 340, None, 240], ["", "Submission", "Review Details", "Actions"],
                             [212, 166], extra=56)
    c.checkbox(cx[0] + 8, ty + 12, False)
    # row 1: pending Edit Item
    r = ry[0]
    c.checkbox(cx[0] + 8, r + 24, False)
    submission_cell(c, cx[1] + 8, r, "Mojito", "Edit Item", "1042", "Craft Bar", "Oct 12, 2026, 10:15 AM")
    y = r + 20
    y = changed_field(c, cx[2] + 8, y, "Item Name", "Mojito", "Classic Mojito") + 20
    changed_field(c, cx[2] + 8, y, "Price", "USD 8.00", "USD 9.00")
    ax = cx[3] + cw[3] - 8
    ap_w = tw("Approve", 14, 500) + 24 + 32
    rj_w = tw("Reject", 14, 500) + 24 + 32
    c.btn(ax - ap_w, r + 20, "Approve", "cta", icon="check")
    c.btn(ax - ap_w - 8 - rj_w, r + 20, "Reject", "outline", icon="x", fg=DEST)
    c.ring(cx[2] + 2, r + 12, cw[2] - 4, 188, 8)
    c.callout(cx[2] + 2, r + 12, 2)
    c.ring(ax - ap_w - 8 - rj_w - 6, r + 14, ap_w + rj_w + 8 + 12, 48, 8)
    c.callout(ax - ap_w - 8 - rj_w - 6, r + 14, 3)
    # row 2: pending Create Item
    r = ry[1]
    c.checkbox(cx[0] + 8, r + 24, False)
    submission_cell(c, cx[1] + 8, r, "Taco Combo", "Create Item", "1057", "Taco Cart", "Oct 12, 2026, 11:02 AM")
    submitted_field(c, cx[2] + 8, r + 20, "Item Name", "Taco Combo")
    submitted_field(c, cx[2] + 8, r + 20 + 24 + 16, "Price", "USD 12.00")
    c.btn(ax - ap_w, r + 20, "Approve", "cta", icon="check")
    c.btn(ax - ap_w - 8 - rj_w, r + 20, "Reject", "outline", icon="x", fg=DEST)
    # pagination footer
    fy = ty + th
    c.line(X + 1, fy, X + IW - 1, fy)
    c.text(X + 16, fy + 28, "1\u20132 of 2", 14, MFG)
    c.icon_btn(X + IW - 16 - 36 - 8 - 36, fy + 10, "chevron-left", color="#6b6b6b")
    c.icon_btn(X + IW - 16 - 36, fy + 10, "chevron-right", color="#6b6b6b")
    c.h = fy + 56 + 20
    c.save(f"{OUT}/tap-approvals-list.svg")


def approvals_bulk():
    W = 1000
    c = T(W, 10)
    X, IW = 20, W - 40
    ty = 20
    cx, cw, ry, th = c.table(X, ty, IW, [52, 340, None, 240], ["", "Submission", "Review Details", "Actions"], [166, 166])
    c.checkbox(cx[0] + 8, ty + 12, True)
    ax = cx[3] + cw[3] - 8
    ap_w = tw("Approve", 14, 500) + 24 + 32
    rj_w = tw("Reject", 14, 500) + 24 + 32
    for r, (n, it, v, when, vid) in zip(ry, [("Taco Combo", "1057", "Taco Cart", "Oct 12, 2026, 11:02 AM", "USD 12.00"),
                                              ("Iced Latte", "1061", "Cold Brew Stand", "Oct 12, 2026, 11:20 AM", "USD 5.00")]):
        c.checkbox(cx[0] + 8, r + 24, True)
        submission_cell(c, cx[1] + 8, r, n, "Create Item", it, v, when)
        submitted_field(c, cx[2] + 8, r + 20, "Item Name", n)
        submitted_field(c, cx[2] + 8, r + 20 + 24 + 16, "Price", vid)
        c.btn(ax - ap_w, r + 20, "Approve", "cta", icon="check")
        c.btn(ax - ap_w - 8 - rj_w, r + 20, "Reject", "outline", icon="x", fg=DEST)
    by = ty + th + 24
    c.rect(0, by, W, 62, BG, 0)
    c.line(0, by, W, by)
    c.text(X, by + 31, "2 selected", 14, FG, 500)
    c.btn(X + tw("2 selected", 14, 500) + 16, by + 13, "Clear", "ghost")
    ab = tw("Approve Selected", 14, 500) + 32
    rb = tw("Reject Selected", 14, 500) + 32
    c.btn(X + IW - ab, by + 13, "Approve Selected", "cta")
    c.btn(X + IW - ab - 8 - rb, by + 13, "Reject Selected", "outline", fg=DEST)
    c.h = by + 62
    c.save(f"{OUT}/tap-approvals-bulk-bar.svg")



# ---------------------------------------------------------------- cashless activity
GREEN_TXT = EMERALD7


def metric_cards(c, x, y, w):
    gap = 12
    cw = (w - 3 * gap) / 4
    items = [("Top-up Transactions", "128", None), ("Top-up Amount", "6,400.00", "USD"),
             ("Spending Transactions", "342", None), ("Spending Amount", "4,130.00", "USD")]
    for i, (lab, val, cur) in enumerate(items):
        cx = x + i * (cw + gap)
        c.rect(cx + .5, y + .5, cw - 1, 87, BG, 6, BORDER)
        c.text(cx + 20, y + 30, lab, 14, MFG)
        c.icon("info", cx + 20 + tw(lab, 14) + 10, y + 23, 14, MFG)
        c.text(cx + 20, y + 62, val, 20, FG, 700)
        if cur:
            c.text(cx + 20 + tw(val, 20, 700) + 12, y + 64, "/ " + cur, 13, MFG)
    return cw


def cashless_rows(c, cx, cw, ry, rows, mid):
    """rows: (when, id, name, email, mid_top, mid_sub, status, amount)."""
    for r, (when, tid, name, email, m1, m2, st, amt) in zip(ry, rows):
        cancelled = st == "Cancelled"
        c.text(cx[0] + 8, r + 19, when, 14)
        c.text(cx[0] + 8, r + 38, tid, 13, MFG)
        c.text(cx[1] + 8, r + 19, name, 14)
        c.text(cx[1] + 8, r + 38, email, 13, MFG)
        c.text(cx[2] + 8, r + 19, m1, 14)
        c.text(cx[2] + 8, r + 38, m2, 13, MFG)
        c.text(cx[3] + 8, r + 28, st, 14, MFG if cancelled else GREEN_TXT)
        c.text(cx[4] + cw[4] - 8, r + 28, amt, 14, MFG if cancelled else FG, 500, "end")


def cashless_overview():
    W = 1000
    c = T(W, 10)
    X, IW = 20, W - 40
    cw = metric_cards(c, X, 20, IW)
    c.ring(X - 6, 14, IW + 12, 100, 10)
    c.callout(X - 6, 14, 1)
    pos, tot = c.tabs(X, 138, ["All", "Top-ups", "Spending"], 0)
    c.ring(X - 5, 133, tot + 10, 46, 10)
    c.callout(X - 5, 133, 2)
    fy = 198
    c.text(X, fy + 7, "Status", 14, FG, 500)
    c.select(X, fy + 22, 180, "All")
    c.text(X + 192, fy + 7, "Search", 14, FG, 500)
    c.input(X + 192, fy + 22, 300, placeholder="Search by name, email or transaction ID")
    c.ring(X - 6, fy - 6, 192 + 300 + 12, 72, 10)
    c.callout(X - 6, fy - 6, 3)
    ew = tw("Export", 14, 500) + 24 + 32
    c.btn(X + IW - ew, fy + 22, "Export", "outline", icon="arrow-up-from-line")
    c.ring(X + IW - ew - 5, fy + 17, ew + 10, 46, 8)
    c.callout(X + IW - ew - 5, fy + 17, 4)
    ty = fy + 58 + 24
    rows = [("10/28/2026, 9:41:07 PM", "100231", "Alex Chen", "alex@example.com", "Top-up", "In-App", "Successful", "+50.00"),
            ("10/28/2026, 9:52:33 PM", "100232", "Maya Patel", "maya@example.com", "Spending", "Taco Cart", "Successful", "\u221212.00"),
            ("10/28/2026, 10:05:18 PM", "100233", "Sam Rivera", "sam@example.com", "Spending", "Craft Bar", "Cancelled", "\u22128.00")]
    cx, cw2, ry, th = c.table(X, ty, IW, [230, 230, 160, 130, None],
                              ["Transaction", "Attendee", "Activity", "Status", ("Top-up / Spending Amount (USD)", "right")], [57] * 3)
    cashless_rows(c, cx, cw2, ry, rows, None)
    c.h = ty + th + 20
    c.save(f"{OUT}/tap-cashless-activity-overview.svg")


def cashless_filters():
    W = 1060
    c = T(W, 10)
    X, IW = 20, W - 40
    c.tabs(X, 20, ["All", "Top-ups", "Spending"], 2)
    fy = 80
    xs = []
    fx = X
    for lab, val in (("Status", "All"), ("Vendor", "All Vendors"), ("Sales Location", "All Locations")):
        c.text(fx, fy + 7, lab, 14, FG, 500)
        c.select(fx, fy + 22, 180, val)
        xs.append(fx)
        fx += 188
    c.text(fx, fy + 7, "Search", 14, FG, 500)
    c.input(fx, fy + 22, 300, placeholder="Search by name, email or transaction ID")
    ew = tw("Export", 14, 500) + 24 + 32
    c.btn(X + IW - ew, fy + 22, "Export", "outline", icon="arrow-up-from-line")
    ty = fy + 58 + 24
    rows = [("10/28/2026, 9:52:33 PM", "100232", "Maya Patel", "maya@example.com", "Taco Cart", "Main Window", "Successful", "\u221212.00"),
            ("10/28/2026, 10:05:18 PM", "100233", "Sam Rivera", "sam@example.com", "Craft Bar", "Main Bar", "Cancelled", "\u22128.00"),
            ("10/28/2026, 10:12:40 PM", "100234", "Jordan Lee", "jordan@example.com", "Noodle House", "Noodle Counter", "Successful", "\u221215.00")]
    cx, cw2, ry, th = c.table(X, ty, IW, [230, 230, 190, 130, None],
                              ["Transaction", "Attendee", "Vendor", "Status", ("Spending Amount (USD)", "right")], [57] * 3)
    cashless_rows(c, cx, cw2, ry, rows, None)
    # open Vendor dropdown (drawn last so it overlays the table)
    c.select(xs[1], fy + 22, 180, "All Vendors")
    c.dropdown(xs[1], fy + 22 + 36 + 4, 180, ["All Vendors", "Taco Cart", "Craft Bar", "Noodle House"], 0)
    c.h = ty + th + 20
    c.save(f"{OUT}/tap-cashless-activity-filters.svg")


# ---------------------------------------------------------------- spending report
def spending_report():
    W = 1120
    c = T(W, 10)
    X, IW = 20, W - 40
    pos, tot = c.tabs(X, 20, ["By Vendor", "By Item"], 0)
    c.ring(X - 5, 15, tot + 10, 46, 10)
    c.callout(X - 5, 15, 1)
    fy = 80
    c.text(X, fy + 7, "Search", 14, FG, 500)
    c.input(X, fy + 22, 300, placeholder="Search by Vendor Name")
    w1 = tw("Export Summary", 14, 500) + 24 + 32
    w2 = tw("Export All Vendor Reports", 14, 500) + 24 + 32
    c.btn(X + IW - w2, fy + 22, "Export All Vendor Reports", "cta", icon="download")
    c.btn(X + IW - w2 - 8 - w1, fy + 22, "Export Summary", "outline", icon="download")
    c.ring(X + IW - w2 - 8 - w1 - 5, fy + 17, w1 + w2 + 8 + 10, 46, 8)
    c.callout(X + IW - w2 - 8 - w1 - 5, fy + 17, 3)
    ty = fy + 58 + 24
    heads = ["Vendor", ("Successful Txns", "info"), ("Cancelled Txns", "info"), ("Gross Sales (USD)", "info"),
             ("Refunded Amount (USD)", "info"), ("Net Sales (USD)", "info"), ""]
    cx, cw, ry, th = c.table(X, ty, IW, [None, 150, 145, 160, 200, 145, 140], heads, [40, 50, 50, 50])
    # Total row
    r = ry[0]
    c.rect(X + 1, r, IW - 2, 40, MUTEDBG, 0, op=0.7)
    tot_row = ["Total", "485", "7", "10,450.00", "300.00", "10,150.00"]
    for i, v in enumerate(tot_row):
        c.text(cx[i] + 8, r + 20, v, 14, FG, 600)
    c.ring(X - 4, r - 2, IW + 8, 44, 6)
    c.callout(X - 4, r - 2, 2)
    vend = [("Taco Cart", "210", "4", "3,250.00", "100.00", "3,150.00"),
            ("Craft Bar", "180", "2", "4,800.00", "0.00", "4,800.00"),
            ("Noodle House", "95", "1", "2,400.00", "200.00", "2,200.00")]
    for k, (row, r) in enumerate(zip(vend, ry[1:])):
        for i, v in enumerate(row):
            c.text(cx[i] + 8, r + 25, v, 14)
        c.icon("download", cx[6] + 12, r + 17, 16, BTN)
        c.text(cx[6] + 36, r + 25, "Export Report", 14, BTN, 500)
        if k == 0:
            c.ring(cx[6] + 2, r + 5, cw[6] - 2, 40, 8)
            c.callout(cx[6] + 2, r + 5, 4)
    c.h = ty + th + 20
    c.save(f"{OUT}/tap-spending-report-by-vendor.svg")


# ---------------------------------------------------------------- personalization form
def pf_table(c, x, y, w, rows):
    cx, cw, ry, th = c.table(x, y, w, [40, None, None, None], ["", "Question", "Required", "Status"], [53] * len(rows), boxed=False)
    for (q, req, st), r in zip(rows, ry):
        c.icon("grip-vertical", cx[0] + 8, r + 18.5, 16, MFG)
        c.text(cx[1] + 8, r + 26.5, q, 14, FG, 500)
        c.switch(cx[2] + 8, r + 17.3, req)
        c.select(cx[3] + 8, r + 8.5, 118, st, GREEN if st == "Active" else GRAY)
    return cx, cw, ry, th


def personalization_page():
    W = 760
    c = T(W, 10)
    X, IW = 20, W - 40
    c.text(X, 38, "Quick add", 14, MFG, 500)
    bx = X + tw("Quick add", 14, 500) + 16
    q0 = bx
    for lab, ic in (("Nationality", "globe"), ("Identity Document", "id-card")):
        bw = tw(lab, 14, 500) + 24 + 32
        c.btn(bx, 20, lab, "outline", icon=ic)
        bx += bw + 16
    c.ring(q0 - 6, 14, bx - q0 - 16 + 12, 48, 8)
    c.callout(q0 - 6, 14, 1)
    c.text(X, 98, "Preset Questions", 14, FG, 600)
    ty = 120
    cx, cw, ry, th = pf_table(c, X, ty, IW, [("Gender", True, "Active"), ("Phone Number", True, "Active"), ("Date of Birth", False, "Active")])
    c.ring(X - 4, ry[0] + 2, IW + 8, 49, 8)
    c.callout(X - 4, ry[0] + 2, 3)
    cy0 = ty + th + 32
    c.text(X, cy0 + 18, "Custom Questions", 14, FG, 600)
    cb = tw("Custom question", 14, 500) + 24 + 32
    c.btn(X + IW - cb, cy0, "Custom question", "cta", icon="plus")
    c.ring(X + IW - cb - 5, cy0 - 5, cb + 10, 46, 8)
    c.callout(X + IW - cb - 5, cy0 - 5, 2)
    ty2 = cy0 + 36 + 12
    cx, cw, ry, th2 = pf_table(c, X, ty2, IW, [("T-shirt size", True, "Active")])
    c.h = ty2 + th2 + 20
    c.save(f"{OUT}/tap-personalization-form-page.svg")


def custom_question_panel():
    def build(c, x, y, w):
        c.label(x, y + 7, "Question*")
        c.input(x, y + 22, w, value="T-shirt size")
        y += 22 + 36 + 24
        c.label(x, y + 7, "Description")
        c.textarea(x, y + 22, w, 96, placeholder="Enter description")
        y += 22 + 96 + 24
        c.label(x, y + 7, "Answer Type*")
        c.select(x, y + 22, w, "Single choice")
        y += 22 + 36 + 24
        c.text(x, y + 7, "Options*", 14, FG, 500)
        y += 22
        for v in ("Small", "Large"):
            c.input(x, y, w - 52, value=v)
            c.icon("x", x + w - 36, y + 8, 20, FG)
            y += 44
        c.btn(x, y, "Add Option", "outline", icon="plus", w=w)
        y += 36 + 24
        c.text(x, y + 9, "Required", 14, FG, 500)
        c.switch(x + tw("Required", 14, 500) + 12, y, False)
        return y + 24
    drawer_scene("tap-personalization-custom-question-panel", 640, 384, "Create Custom Question", build,
                 "Cancel", "Save", lambda c: page_skeleton(c, 20, 20, 160), border=False)


#MAIN
if __name__ == "__main__":
    sidebar()
    stations_tab()
    station_panel()
    payment_methods_tab()
    vendor_list()
    vendor_panel()
    vendor_detail()
    vendor_item_form()
    vendor_login_codes()
    approvals_list()
    approvals_bulk()
    cashless_overview()
    cashless_filters()
    spending_report()
    personalization_page()
    custom_question_panel()
