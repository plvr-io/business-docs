import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ui import *

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "getting-started")

# Sign-in card
c = Canvas(560, 400)
c.card(60, 30, 440, 340)
c.text(90, 80, "Welcome to PLVR Business", 22, weight=700)
c.text(90, 106, "Register or sign in and we'll get started.", 14, MUTED)
c.input(90, 130, 380, "Enter your email", "you@example.com")
c.button(90, 182, 380, "Continue")
c.text(280, 244, "Or", 13, MUTED, anchor="middle")
c.button(90, 258, 380, "Continue with Apple", fill=BG, stroke=BORDER)
c.button(90, 308, 380, "Continue with Google", fill=BG, stroke=BORDER)
c.save(f"{OUT}/onboarding-sign-in-screen.svg")

# Event status menu
c = Canvas(560, 300)
c.card(30, 30, 500, 70)
c.text(54, 72, "Neon Nights", 16, weight=600)
c.button(390, 48, 120, "Status ▾", h=34, fill=BG, stroke=BORDER)
c.card(390, 90, 140, 130)
for i, (label, hl) in enumerate([("Public", True), ("Private", False), ("Inactive", False)]):
    if hl:
        c.rect(398, 100 + i * 38, 124, 32, "#2a1a52", 6)
    c.text(412, 122 + i * 38, label, 14, FG, 600 if hl else 400)
c.ring(394, 96, 132, 40, 8)
c.callout(380, 116, 1)
c.save(f"{OUT}/quickstart-event-status-menu.svg")
