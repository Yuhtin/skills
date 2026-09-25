#!/usr/bin/env python3
"""Render one slide to PNG with its scene frozen at chosen times, the way the deck paints it.

Usage: python3 tools/render.py project/slides/<id>.html [t1 t2 ... | poster]
  times in ms of SCENE time (window.__FREEZE_T); "poster" = the scene's F (its resting frame).
Writes ROOT/renders/<id>-<t>.png (960x540) and prints console errors from the page and its scene.
One Chrome at a time machine-wide (a directory lock), so parallel agents just wait their turn.
"""
import os
import re
import subprocess
import sys
import tempfile
import time
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _deck import ROOT, chrome_path, embed_body, poster_time, slide_page  # noqa: E402

LOCK = os.path.join(ROOT, "renders", ".chrome.lock")


def lock():
    start = time.time()
    while True:
        try:
            os.mkdir(LOCK)
            return
        except FileExistsError:
            if time.time() - os.path.getmtime(LOCK) > 90:
                try:
                    os.rmdir(LOCK)
                except OSError:
                    pass
            time.sleep(0.5)
            if time.time() - start > 600:
                raise SystemExit("gave up waiting for the Chrome lock")


def shoot(doc, png):
    tmp = tempfile.mkdtemp(prefix="deck-render-")
    page = os.path.join(tmp, "page.html")
    open(page, "w", encoding="utf-8").write(doc)
    errlog = os.path.join(tmp, "stderr.txt")
    if os.path.exists(png):
        os.unlink(png)
    lock()
    try:
        with open(errlog, "w") as ef:
            proc = subprocess.Popen([chrome_path(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                                     "--no-first-run", "--no-default-browser-check",
                                     f"--user-data-dir={os.path.join(tmp, 'profile')}",
                                     "--force-device-scale-factor=0.5", "--window-size=1920,1080",
                                     "--virtual-time-budget=2500", "--enable-logging=stderr", "--v=0",
                                     f"--screenshot={png}", "file://" + page],
                                    stdout=subprocess.DEVNULL, stderr=ef, start_new_session=True)
            # Chrome sometimes writes the PNG and then does not exit: stop it once the file is whole.
            deadline, last = time.time() + 45, -1
            while time.time() < deadline and proc.poll() is None:
                time.sleep(0.5)
                if os.path.exists(png):
                    size = os.path.getsize(png)
                    if size > 0 and size == last:
                        break
                    last = size
            if proc.poll() is None:
                try:
                    os.killpg(proc.pid, 15)
                    proc.wait(timeout=5)
                except Exception:
                    try:
                        os.killpg(proc.pid, 9)
                    except Exception:
                        pass
    finally:
        try:
            os.rmdir(LOCK)
        except OSError:
            pass
    logs = [l for l in open(errlog, errors="replace").read().splitlines()
            if "CONSOLE" in l or "Uncaught" in l or "Content Security Policy" in l]
    shutil.rmtree(tmp, ignore_errors=True)
    return logs


def main():
    path = sys.argv[1]
    sid = os.path.splitext(os.path.basename(path))[0]
    raw = open(path, encoding="utf-8").read()
    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)
    for t in sys.argv[2:] or ["poster"]:
        freeze = poster_time(embed_body(raw)) if t == "poster" else int(t)
        pre = "" if freeze is None else f"<script>window.__FREEZE_T={freeze};</script>"
        png = os.path.join(ROOT, "renders", f"{sid}-{t}.png")
        logs = shoot(slide_page(raw, pre), png)
        print(png if os.path.exists(png) else f"NO PNG for t={t}", f"(freeze={freeze})")
        for l in logs[:20]:
            print("  console:", l[-400:])


if __name__ == "__main__":
    main()
