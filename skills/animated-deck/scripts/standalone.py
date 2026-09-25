#!/usr/bin/env python3
"""Pack the deck into one self-contained HTML player (no Artifact needed): out/deck.html.

Usage: python3 tools/standalone.py
Arrow keys / space / click advance, F toggles fullscreen. Each slide is rebuilt when it is shown, so
its scene plays once from the start every time you arrive — the same contract as the Slides runtime.
Web fonts load from Google Fonts (needs network); everything else is inside the file.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _deck import ROOT, config, order, slide_page, slide_path  # noqa: E402

cfg = config()
pages = [slide_page(open(slide_path(sid), encoding="utf-8").read()) for sid in order()]
bg = (cfg["backgrounds"] or ["#111111"])[0]
doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(cfg.get('title') or 'Deck')}</title>
<style>html,body{{margin:0;height:100%;background:{bg};overflow:hidden}}
#stage{{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform-origin:0 0}}
#stage iframe{{border:0;width:1920px;height:1080px;display:block}}
#n{{position:fixed;right:16px;bottom:12px;font:14px system-ui,sans-serif;color:#888}}</style></head>
<body><div id="stage"></div><div id="n"></div><script>
var P={json.dumps(pages)},i=0,st=document.getElementById('stage');
function fit(){{var s=Math.min(innerWidth/1920,innerHeight/1080);st.style.transform='translate('+(-960*s)+'px,'+(-540*s)+'px) scale('+s+')'}}
function show(k){{i=Math.max(0,Math.min(P.length-1,k));st.innerHTML='';var f=document.createElement('iframe');f.srcdoc=P[i];st.appendChild(f);
 document.getElementById('n').textContent=(i+1)+' / '+P.length;history.replaceState(null,'','#'+(i+1))}}
addEventListener('keydown',function(e){{if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key))show(i+1);
 else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key))show(i-1);else if(e.key==='Home')show(0);else if(e.key==='End')show(P.length-1);
 else if(e.key==='f')(document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen())}});
addEventListener('click',function(){{show(i+1)}});addEventListener('resize',fit);fit();show((parseInt(location.hash.slice(1))||1)-1);
</script></body></html>"""
os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
out = os.path.join(ROOT, "out", "deck.html")
open(out, "w", encoding="utf-8").write(doc)
print(out, f"{len(doc) // 1024} KB, {len(pages)} slides")
