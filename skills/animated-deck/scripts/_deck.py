"""Shared helpers for the animated-deck scripts.

ROOT is the deck's work folder: the parent of the folder these scripts were copied into
(ROOT/tools/*.py), or $DECK_ROOT when set. Config lives in ROOT/deck.config.json.
"""
import json
import os
import re
import shutil

ROOT = os.environ.get("DECK_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSP = ("default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
       "img-src data: blob:; font-src data:; media-src data: blob:; connect-src 'none'; "
       "worker-src 'none'; frame-src 'none'; object-src 'none'; form-action 'none'; base-uri 'none'")


def config():
    path = os.path.join(ROOT, "deck.config.json")
    cfg = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    cfg.setdefault("fontsHref", "")
    cfg.setdefault("backgrounds", [])
    cfg.setdefault("bannedColors", [])
    cfg.setdefault("bannedRgb", [])
    cfg.setdefault("minFontPx", 24)
    cfg.setdefault("holdMs", 2500)
    cfg.setdefault("ambientMs", {})
    cfg.setdefault("ambientTailMs", {})
    return cfg


def chrome_path():
    cfg = config()
    if cfg.get("chrome"):
        return cfg["chrome"]
    for c in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium"]:
        if os.path.exists(c):
            return c
    for name in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"]:
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("Chrome/Chromium not found: set \"chrome\" in deck.config.json")


def order():
    return json.load(open(os.path.join(ROOT, "project/deck.json"), encoding="utf-8"))["order"]


def slide_path(sid):
    return os.path.join(ROOT, "project/slides", sid + ".html")


def embed_body(raw):
    """x-embed is raw text for the Slides parser: its HTML is everything up to </x-embed>."""
    m = re.search(r"<x-embed[^>]*>(.*?)</x-embed>", raw, re.S | re.I)
    return m.group(1) if m else ""


def srcdoc(body, pre=""):
    """The document the Slides runtime builds around an embed (same CSP and reset)."""
    return ('<!doctype html><html><head><meta http-equiv="Content-Security-Policy" content="' + CSP +
            '"><meta name="referrer" content="no-referrer"><style>html,body{margin:0;padding:0;'
            'overflow:hidden}</style></head><body>' + pre + body + "</body></html>")


def slide_page(raw, embed_pre=""):
    """A whole slide as a plain HTML page at 1920x1080, as the deck paints it: the embed becomes a
    sandboxed iframe at its pinned box, flow text paints OVER it (the runtime's order), notes hidden."""
    import html as h

    def swap(mm):
        attrs = mm.group(1) or ""
        st = re.search(r'style="([^"]*)"', attrs)
        st = st.group(1) if st else ""
        doc = srcdoc(mm.group(2), embed_pre)
        return (f'<iframe sandbox="allow-scripts" style="{st};border:0;background:transparent;display:block" '
                f'srcdoc="{h.escape(doc, quote=True)}"></iframe>')

    b = re.sub(r"<x-embed(\s[^>]*)?>(.*?)</x-embed>", swap, raw, flags=re.S | re.I)
    b = re.sub(r"<aside>.*?</aside>", "", b, flags=re.S)
    b = re.sub(r'<section([^>]*)style="', r'<section\1style="position:relative; width:1920px; height:1080px; '
               r'box-sizing:border-box; overflow:hidden; ', b, count=1)
    cfg = config()
    link = f'<link rel="stylesheet" href="{cfg["fontsHref"]}">' if cfg["fontsHref"] else ""
    bg = (cfg["backgrounds"] or ["#777777"])[0]
    return ('<!doctype html><html><head><meta charset="utf-8">' + link +
            f'<style>html,body{{margin:0;padding:0;background:{bg};width:1920px;height:1080px;overflow:hidden}}'
            '*{box-sizing:border-box}h1,h2,h3,p,ul,ol{margin:0}section{display:flex;flex-direction:column}'
            'section>:not(iframe){position:relative}x-icon,x-shape,x-connector{display:block}</style></head><body>'
            + b + "</body></html>")


def end_and_speed(body):
    """END (scene time of the resting state) and SP (scene clock speed) read off an embed's script."""
    m = re.search(r"\bEND\s*=\s*(\d+)", body)
    end = int(m.group(1)) if m else None
    s = re.search(r"\(performance\.now\(\)-T0\)\*([\d.]+)\s*,\s*END", body)
    return end, float(s.group(1)) if s else 1.0


def poster_time(body):
    m = re.search(r"\bF\s*=\s*(\d+)", body) or re.search(r"\bEND\s*=\s*(\d+)", body)
    return int(m.group(1)) if m else None
