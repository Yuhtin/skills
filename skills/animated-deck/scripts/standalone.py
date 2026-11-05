#!/usr/bin/env python3
"""Pack the deck into one self-contained HTML player (no Artifact needed): out/deck.html.

Usage: python3 tools/standalone.py
Click, space and the forward keys finish a scene that is still playing; once it rests they go to the
next slide. Back keys and Home/End go straight there, F toggles fullscreen. A layer over the stage takes
the clicks, because a click inside an iframe never reaches this page and traps the keyboard in there.
Each slide is rebuilt when it is shown, so its scene plays once from the start every time you arrive —
the same contract as the Slides runtime.
Web fonts load from Google Fonts (needs network); everything else is inside the file.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _deck import ROOT, config, order, scene_ms, slide_page, slide_path  # noqa: E402

# Moves the scene's clock past END on request; the kit's tick then draws the resting frame by itself.
SKIP = ("<script>(function(){var n=performance.now.bind(performance),o=0;performance.now=function(){return n()+o};"
        "addEventListener('message',function(e){if(e.data&&e.data.skip)o=1e9})})();</script>")

cfg = config()
raws = [open(slide_path(sid), encoding="utf-8").read() for sid in order()]
pages = [slide_page(raw, SKIP) for raw in raws]
bg = (cfg["backgrounds"] or ["#111111"])[0]
doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(cfg.get('title') or 'Deck')}</title>
<style>html,body{{margin:0;height:100%;background:{bg};overflow:hidden}}
#stage{{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform-origin:0 0}}
#stage iframe{{border:0;width:1920px;height:1080px;display:block}}
#hit{{position:fixed;inset:0}}
#n{{position:fixed;right:16px;bottom:12px;font:14px system-ui,sans-serif;color:#888}}</style></head>
<body><div id="stage"></div><div id="hit"></div><div id="n"></div><script>
var P={json.dumps(pages)},D={json.dumps([scene_ms(raw) for raw in raws])},i=0,restAt=0,st=document.getElementById('stage');
var R=matchMedia('(prefers-reduced-motion: reduce)').matches;
function fit(){{var s=Math.min(innerWidth/1920,innerHeight/1080);st.style.transform='translate('+(-960*s)+'px,'+(-540*s)+'px) scale('+s+')'}}
function show(k){{i=Math.max(0,Math.min(P.length-1,k));st.innerHTML='';var f=document.createElement('iframe');f.srcdoc=P[i];
 restAt=R||!D[i]?0:Infinity;f.onload=function(){{if(restAt)restAt=performance.now()+D[i]}};st.appendChild(f);
 document.getElementById('n').textContent=(i+1)+' / '+P.length;history.replaceState(null,'','#'+(i+1))}}
function forward(){{if(performance.now()<restAt){{var w=st.firstChild.contentWindow;for(var j=0;j<w.frames.length;j++)w.frames[j].postMessage({{skip:1}},'*');restAt=0}}
 else if(i<P.length-1)show(i+1)}}
addEventListener('keydown',function(e){{if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key))forward();
 else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key))show(i-1);else if(e.key==='Home')show(0);else if(e.key==='End')show(P.length-1);
 else if(e.key==='f')(document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen())}});
addEventListener('click',forward);addEventListener('resize',fit);fit();show((parseInt(location.hash.slice(1))||1)-1);
</script></body></html>"""
os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
out = os.path.join(ROOT, "out", "deck.html")
open(out, "w", encoding="utf-8").write(doc)
print(out, f"{len(doc) // 1024} KB, {len(pages)} slides")
