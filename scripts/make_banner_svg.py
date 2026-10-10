"""Simple ASCII-banner terminal SVG (types in once). Reads config.json. Needs: pip install pyfiglet"""
import os, json
import pyfiglet
from xml.sax.saxutils import escape
cfg = json.load(open("config.json"))
STATIC = os.environ.get("STATIC") == "1"
W, H = 370, 250
F = "font-family=\"Menlo,Consolas,'DejaVu Sans Mono',monospace\""
art = [l.rstrip() for l in pyfiglet.figlet_format(cfg.get("banner_text", "SMX"), font=cfg.get("banner_font", "standard"), width=200).split("\n") if l.strip()]
cols = max(len(l) for l in art)
cw = min((W - 40) / cols, 9.0)
fs, ch = cw * 1.25, cw * 1.9
P = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>',
     f'<rect width="{W}" height="32" rx="8" fill="#161b22"/><rect y="20" width="{W}" height="12" fill="#161b22"/>',
     '<circle cx="18" cy="16" r="5" fill="#ff5f56"/><circle cx="36" cy="16" r="5" fill="#ffbd2e"/><circle cx="54" cy="16" r="5" fill="#27c93f"/>',
     f'<text x="{W/2}" y="20" text-anchor="middle" {F} font-size="11" fill="#8b949e">~/{escape(cfg["username"])}</text>']
y0 = 46
for i, l in enumerate(art):
    y, t = y0 + i * ch, 0.3 + i * 0.18
    txt = f'<text x="20" y="{y+ch-4:.1f}" xml:space="preserve" {F} font-size="{fs:.1f}" fill="#7ee787" textLength="{len(l)*cw:.1f}" lengthAdjust="spacing" {{c}}>{escape(l)}</text>'
    if STATIC: P.append(txt.replace(" {c}", "")); continue
    P.append(f'<clipPath id="r{i}"><rect x="0" y="{y:.1f}" width="0" height="{ch+2:.1f}"><animate attributeName="width" from="0" to="{W}" dur="0.5s" begin="{t:.2f}s" fill="freeze"/></rect></clipPath>')
    P.append(txt.replace("{c}", f'clip-path="url(#r{i})"'))
lines = cfg.get("banner_lines", [["$ whoami", "#8b949e"], [cfg["name"], "#c9d1d9"], ["$ cat focus.txt", "#8b949e"], ["DSA · Web · AI", "#79c0ff"]])
ly = y0 + len(art) * ch + 24
for j, (s, col) in enumerate(lines):
    t = 0.3 + len(art) * 0.18 + 0.3 + j * 0.35
    inner = f'<text x="20" y="{ly + j*20:.0f}" {F} font-size="12" fill="{col}">{escape(s)}</text>'
    P.append(inner if STATIC else f'<g opacity="0">{inner}<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{t:.2f}s" fill="freeze"/></g>')
# blinking cursor after last line
cx = 20 + 7.2 * len(lines[-1][0]) + 4
P.append(f'<rect x="{cx:.0f}" y="{ly+(len(lines)-1)*20-11:.0f}" width="7" height="14" fill="#7ee787"><animate attributeName="opacity" values="1;0;1" dur="1s" begin="3s" repeatCount="indefinite"/></rect>' if not STATIC else "")
P.append("</svg>")
open("ascii-banner.svg", "w").write("\n".join(P))
print(f"wrote ascii-banner.svg ({cols} cols)")
