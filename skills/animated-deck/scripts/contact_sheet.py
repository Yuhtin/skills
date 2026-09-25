#!/usr/bin/env python3
"""Render every slide's resting frame (poster) in deck order and tile them 6 per sheet.

Usage: python3 tools/contact_sheet.py [--no-render]
Writes ROOT/renders/sheet-1.png, sheet-2.png, ... — read them in order, as the audience flips through.
Needs Pillow (python3 -m pip install pillow). --no-render reuses the existing <id>-poster.png files.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _deck import ROOT, order, slide_path  # noqa: E402

ids = order()
if "--no-render" not in sys.argv:
    for sid in ids:
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "render.py"), slide_path(sid), "poster"],
                           capture_output=True, text=True)
        errs = [l for l in r.stdout.splitlines() if "console:" in l or "NO PNG" in l]
        print(sid, "ok" if not errs else "\n  ".join([""] + errs))
from PIL import Image  # noqa: E402

for k in range(0, len(ids), 6):
    sheet = Image.new("RGB", (1920, 1620), (120, 120, 120))
    for j, sid in enumerate(ids[k:k + 6]):
        png = os.path.join(ROOT, "renders", f"{sid}-poster.png")
        if os.path.exists(png):
            sheet.paste(Image.open(png).convert("RGB").resize((958, 538)), ((j % 2) * 962, (j // 2) * 541))
    out = os.path.join(ROOT, "renders", f"sheet-{k // 6 + 1}.png")
    sheet.save(out)
    print(out)
