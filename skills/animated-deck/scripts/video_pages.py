#!/usr/bin/env python3
"""Build one page per slide for the MP4, each scene driven by a virtual clock, plus the timing plan.

Usage: python3 tools/video_pages.py
Inside each scene, performance.now() is replaced by a clock the recorder sets: the parent posts
{vt, seq} and the scene answers {ack: seq} after two animation frames, so every video frame is a
finished frame at an exact time, however slow the machine is.
A slide lasts: its scene until END (divided by the scene's clock speed) + holdMs; ambient slides
(cover, closing) last ambientMs, or END + ambientTailMs. Writes ROOT/video/pages/*.html and plan.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _deck import ROOT, config, embed_body, end_and_speed, order, slide_page, slide_path  # noqa: E402

CLOCK = ("<script>(function(){var vt=0;performance.now=function(){return vt};"
         "addEventListener('message',function(e){var d=e.data;if(!d||d.vt==null)return;vt=d.vt;"
         "requestAnimationFrame(function(){requestAnimationFrame(function(){parent.postMessage({ack:d.seq},'*')})})})})();</script>")

cfg = config()
os.makedirs(os.path.join(ROOT, "video/pages"), exist_ok=True)
plan = []
for sid in order():
    raw = open(slide_path(sid), encoding="utf-8").read()
    end, sp = end_and_speed(embed_body(raw))
    open(os.path.join(ROOT, "video/pages", sid + ".html"), "w", encoding="utf-8").write(slide_page(raw, CLOCK))
    if sid in cfg["ambientMs"]:
        dur = cfg["ambientMs"][sid]
    elif end is None:
        dur = 12000
    else:
        dur = round(end / sp) + cfg["ambientTailMs"].get(sid, cfg["holdMs"])
    plan.append({"id": sid, "end": end, "speed": sp, "dur": dur})
json.dump(plan, open(os.path.join(ROOT, "video/plan.json"), "w"), indent=1)
total = sum(p["dur"] for p in plan)
for p in plan:
    print(f'{p["id"]:20} END={p["end"]} ×{p["speed"]} → {p["dur"] / 1000:.1f}s')
print(f"total {total / 1000:.0f}s = {total / 60000:.1f} min, {total * 30 // 1000} frames at 30 fps")
