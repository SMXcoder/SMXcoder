"""Neofetch-style info card SVG, lines fade in one by one. Reads config.json."""
import os, json
from xml.sax.saxutils import escape
cfg = json.load(open("config.json"))
STATIC = os.environ.get("STATIC") == "1"
W, LH, TOP = 490, 26, 70
rows = cfg["card"]
H = TOP + len(rows) * LH + 50
F = "font-family=\"Menlo,Consolas,'DejaVu Sans Mono',monospace\""
P = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>',
     f'<rect width="{W}" height="32" rx="8" fill="#161b22"/><rect y="20" width="{W}" height="12" fill="#161b22"/>',
     '<circle cx="18" cy="16" r="5" fill="#ff5f56"/><circle cx="36" cy="16" r="5" fill="#ffbd2e"/><circle cx="54" cy="16" r="5" fill="#27c93f"/>',
     f'<text x="{W/2}" y="20" text-anchor="middle" {F} font-size="11" fill="#8b949e">neofetch</text>']

def line(i, inner):
    t = 0.4 + i * 0.35
    if STATIC:
        return f'<g>{inner}</g>'
    return (f'<g opacity="0">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{t:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="-12 0" to="0 0" dur="0.4s" begin="{t:.2f}s" fill="freeze"/></g>')

title = escape(cfg.get("card_title", "user@github"))
P.append(line(0, f'<text x="24" y="{TOP-18}" {F} font-size="15" font-weight="bold" fill="#7ee787">{title}</text>'))
P.append(line(1, f'<text x="24" y="{TOP-4}" {F} font-size="12" fill="#30363d">{"─"*max(8,len(title))}</text>'))
for i, (k, v, c) in enumerate(rows):
    y = TOP + 18 + i * LH
    inner = (f'<text x="24" y="{y}" {F} font-size="13" font-weight="bold" fill="{c}">{escape(k)}</text>'
             f'<text x="120" y="{y}" {F} font-size="13" fill="#c9d1d9">{escape(v)}</text>')
    P.append(line(i + 2, inner))
by = H - 22
sw = "".join(f'<rect x="{24+j*22}" y="{by}" width="18" height="10" fill="{col}"/>' for j, col in
              enumerate(["#ff7b72","#ffa657","#e3b341","#7ee787","#79c0ff","#d2a8ff","#c9d1d9"]))
P.append(line(len(rows) + 2, sw))
P.append("</svg>")
open("info-card.svg", "w").write("\n".join(P))
print("wrote info-card.svg")
