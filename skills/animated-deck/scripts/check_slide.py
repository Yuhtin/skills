#!/usr/bin/env python3
"""Structural check of one slide against the Slides subset and the deck's own rules.

Usage: python3 tools/check_slide.py project/slides/<id>.html
Exit 0 = RESULT PASS (warnings may print). Exit 1 = errors. Runs `node --check` on the scene's JS.
Deck rules come from deck.config.json: allowed section backgrounds, banned colors, min font size.
"""
import html.parser
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _deck import config, embed_body  # noqa: E402

ALLOWED_TAGS = {"section", "h1", "h2", "h3", "p", "ul", "ol", "li", "div", "img", "svg", "x-embed", "table",
                "tr", "th", "td", "x-shape", "x-connector", "x-icon", "hr", "aside", "b", "i", "u", "a", "span", "br"}
ALLOWED_PROPS = {
    "position", "left", "top", "right", "bottom", "width", "height", "min-width", "min-height", "max-width",
    "max-height", "display", "flex-direction", "flex-wrap", "gap", "align-items", "justify-content",
    "justify-items", "align-self", "justify-self", "flex", "flex-grow", "flex-shrink", "flex-basis",
    "grid-template-columns", "grid-template-rows", "grid-column", "grid-row", "aspect-ratio", "padding",
    "overflow", "font-family", "font-size", "font-weight", "font-style", "font", "line-height", "letter-spacing",
    "text-align", "text-transform", "white-space", "text-decoration", "font-variant-numeric",
    "-webkit-text-stroke", "color", "background", "background-clip", "-webkit-text-fill-color", "border",
    "border-top", "border-right", "border-bottom", "border-left", "border-radius", "box-shadow", "text-shadow",
    "opacity", "transform", "filter", "backdrop-filter", "mix-blend-mode", "object-fit", "box-sizing"}
FORBIDDEN_PROPS = {"margin", "margin-top", "margin-bottom", "margin-left", "margin-right", "z-index", "float",
                   "animation", "transition"}
VOID = ("br", "img", "hr", "x-icon", "x-shape", "x-connector")
errors, warnings = [], []
cfg = config()


def check_style(tag, style, where):
    for decl in style.split(";"):
        if not decl.strip():
            continue
        if ":" not in decl:
            errors.append(f"{where}: malformed style '{decl.strip()}'")
            continue
        prop, val = (x.strip() for x in decl.split(":", 1))
        prop = prop.lower()
        if prop in FORBIDDEN_PROPS:
            errors.append(f"{where}: <{tag}> uses forbidden property '{prop}'")
        elif prop not in ALLOWED_PROPS:
            errors.append(f"{where}: <{tag}> uses '{prop}', outside the subset")
        if re.search(r"\b\d*\.?\d+(em|rem|vw|vh)\b", val) and prop != "letter-spacing":
            errors.append(f"{where}: <{tag}> {prop} uses em/rem/vw/vh")
        if "var(" in val:
            errors.append(f"{where}: <{tag}> {prop} uses var()")
        if prop == "font-size":
            m = re.match(r"([\d.]+)px", val)
            if m and float(m.group(1)) < cfg["minFontPx"]:
                errors.append(f"{where}: <{tag}> font-size {val} is under {cfg['minFontPx']}px")


class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.embeds, self.in_svg, self.count, self.aside = [], [], 0, 0, False

    def handle_starttag(self, tag, attrs):
        a, where = dict(attrs), f"line {self.getpos()[0]}"
        if self.in_svg:
            if tag == "svg":
                self.in_svg += 1
            if tag in ("script", "foreignobject") or any(k.startswith("on") for k in a):
                errors.append(f"{where}: inline <svg> holds <{tag}> or a handler")
            if tag in ("animate", "animatetransform", "animatemotion", "set"):
                errors.append(f"{where}: inline <svg> SMIL never plays in a deck: animate inside an <x-embed>")
            self.stack.append(tag)
            return
        self.count += 1
        if tag not in ALLOWED_TAGS:
            errors.append(f"{where}: <{tag}> is not a tag in the slide format")
        if any(k.startswith("on") for k in a):
            errors.append(f"{where}: event handler on <{tag}>")
        if a.get("style"):
            check_style(tag, a["style"], where)
        if tag == "aside":
            if len(self.stack) != 1:
                errors.append(f"{where}: <aside> must be a direct child of <section>")
            self.aside = True
        if tag == "svg":
            self.in_svg = 1
        if tag == "x-embed":
            self.embeds.append((a, len(self.stack), where))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.in_svg:
            if tag == "svg":
                self.in_svg -= 1
            if self.stack:
                self.stack.pop()
            return
        if tag not in VOID and self.stack:
            self.stack.pop()


def main():
    path = sys.argv[1]
    sid = os.path.splitext(os.path.basename(path))[0]
    raw = open(path, encoding="utf-8").read()
    s = raw.strip()
    if not s.startswith("<section") or not s.endswith("</section>") or s.count("<section") != 1:
        errors.append("the file is exactly one <section>…</section>")
    m = re.match(r'<section\s[^>]*id="([^"]+)"', s)
    if not m or m.group(1) != sid:
        errors.append(f"section id must be '{sid}' (the file name)")
    bgm = re.match(r'<section\s[^>]*style="[^"]*background:\s*(#[0-9A-Fa-f]{6})', s)
    if not bgm:
        errors.append("section style must set background as a #rrggbb")
    elif cfg["backgrounds"] and bgm.group(1).lower() not in [b.lower() for b in cfg["backgrounds"]]:
        errors.append(f"section background {bgm.group(1)} is not one of {cfg['backgrounds']} (deck.config.json)")

    low = raw.lower()
    for h in cfg["bannedColors"]:
        if low.count(h.lower()):
            errors.append(f"banned color {h} appears {low.count(h.lower())}x")
    for trip in cfg["bannedRgb"]:
        n = low.replace(" ", "").count("rgba(" + trip.replace(" ", "")) + low.replace(" ", "").count("rgb(" + trip.replace(" ", ""))
        if n:
            errors.append(f"banned rgb({trip}) appears {n}x")

    outer = re.sub(r"(<x-embed(?:\s[^>]*)?>)(.*?)(</x-embed>)", r"\1\3", raw, flags=re.S | re.I)
    p = P()
    p.feed(outer)
    if p.count > 200:
        errors.append(f"{p.count} elements on the slide (limit 200)")
    if len(p.embeds) > 8:
        errors.append(f"{len(p.embeds)} x-embeds (limit 8)")
    for (attrs, depth, where) in p.embeds:
        st = attrs.get("style", "").replace(" ", "")
        if depth != 1:
            errors.append(f"{where}: <x-embed> must be a direct child of <section>")
        if "position:absolute" not in st:
            errors.append(f"{where}: <x-embed> must be position:absolute")
        for need in ("width", "height"):
            if not re.search(rf"(^|;){need}:", st):
                errors.append(f"{where}: <x-embed> needs {need}")

    for i, body in enumerate(re.findall(r"<x-embed[^>]*>(.*?)</x-embed>", raw, re.S | re.I)):
        tag, n = f"embed #{i + 1}", len(body)
        if n > 16384:
            errors.append(f"{tag}: {n} characters (hard limit 16384)")
        elif n > 15000:
            warnings.append(f"{tag}: {n} characters (budget 15000)")
        if re.search(r"https?://(?!www\.w3\.org/)", body):
            errors.append(f"{tag}: external URL (nothing loads in the sandbox)")
        if "@import" in body or "fonts.googleapis" in body:
            errors.append(f"{tag}: loads a font or stylesheet (only system fonts reach an embed)")
        for fm in re.finditer(r'font-size[=:]\s*"?(\d+(?:\.\d+)?)', body):
            if float(fm.group(1)) < cfg["minFontPx"]:
                errors.append(f"{tag}: font-size {fm.group(1)} under {cfg['minFontPx']} inside the scene")
        if not re.search(r"html,body\{[^}]*background:\s*#", body):
            errors.append(f"{tag}: the scene must paint its page: html,body{{background:<slide bg>}} (the host "
                          "paints an opaque canvas behind the iframe)")
        if "__FREEZE_T" not in body:
            errors.append(f"{tag}: no kit tick() (window.__FREEZE_T missing)")
        if "appifactEmbed" not in body:
            errors.append(f"{tag}: no export hook (appifactEmbed.onUpdate → frame(F)); PDF/thumbnail would catch a random frame")
        if "setTimeout" in body or "setInterval" in body or "@keyframes" in body:
            warnings.append(f"{tag}: timers or CSS keyframes — frame(t) must be a pure function of t")
        if not re.search(r"\bEND\s*=", body):
            warnings.append(f"{tag}: no END — the scene loops (fine only for an ambient cover/closing)")
        for j, sc in enumerate(re.findall(r"<script[^>]*>(.*?)</script>", body, re.S | re.I)):
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
                f.write(sc)
            r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
            os.unlink(f.name)
            if r.returncode:
                errors.append(f"{tag}: script {j + 1} does not parse:\n{r.stderr.strip()[:1200]}")
        print(f"{tag}: {n} chars")

    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print("RESULT", "FAIL" if errors else "PASS", f"({len(errors)} errors, {len(warnings)} warnings)")
    sys.exit(1 if errors else 0)


main()
