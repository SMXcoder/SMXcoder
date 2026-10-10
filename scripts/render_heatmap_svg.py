"""Render data/contributions.json -> contrib-heatmap.svg (53x7 rounded boxes, diagonal reveal once)."""
import os, json, datetime as dt
D = json.load(open("data/contributions.json"))
STATIC = os.environ.get("STATIC") == "1"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP = 12, 3
PITCH = CELL + GAP
LEFT, TOP = 40, 56
W = 860
F = "font-family=\"Menlo,Consolas,'DejaVu Sans Mono',monospace\""

days = D["days"]
first = dt.date.fromisoformat(days[0]["date"])
off = (first.weekday() + 1) % 7                 # Sunday = 0
nweeks = (off + len(days) - 1) // 7 + 1
H = TOP + 7 * PITCH + 70

P = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     '<style>.c{opacity:%s;animation:in .45s ease-out forwards}'
     '@keyframes in{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}</style>' % ("1" if STATIC else "0"),
     f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>',
     f'<text x="{LEFT}" y="26" {F} font-size="13" fill="#7ee787">$ ./contributions.sh --user {D["username"]}</text>']
for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    P.append(f'<text x="{LEFT-8}" y="{TOP+r*PITCH+CELL-2}" text-anchor="end" {F} font-size="9" fill="#8b949e">{name}</text>')
last_m = None
for i, d in enumerate(days):
    date = dt.date.fromisoformat(d["date"])
    k = i + off
    wk, dy = k // 7, k % 7
    x, y = LEFT + wk * PITCH, TOP + dy * PITCH
    if date.month != last_m and dy < 7 and wk < nweeks - 1 and date.day <= 7:
        P.append(f'<text x="{x}" y="{TOP-8}" {F} font-size="9" fill="#8b949e">{date.strftime("%b")}</text>')
    last_m = date.month
    delay = (wk + dy) * 0.018
    cnt = d["count"]
    P.append(f'<rect class="c" style="animation-delay:{delay:.2f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
             f'fill="{PALETTE[min(d["level"],5)]}"><title>{cnt} on {d["date"]}</title></rect>')
fy = TOP + 7 * PITCH + 24
bd = D["best_day"]
P.append(f'<text x="{LEFT}" y="{fy}" {F} font-size="12" fill="#c9d1d9">{D["total"]:,} contributions in the last year'
         f'  ·  streak {D["current_streak"]}d (best {D["longest_streak"]}d)  ·  best day {bd["count"]} ({bd["date"]})</text>')
lx = W - 40 - 6 * 17 - 70
P.append(f'<text x="{lx-8}" y="{fy+9-12}" text-anchor="end" {F} font-size="10" fill="#8b949e">Less</text>')
for j, c in enumerate(PALETTE):
    P.append(f'<rect x="{lx+j*17}" y="{fy-12}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
P.append(f'<text x="{lx+6*17+4}" y="{fy-3}" {F} font-size="10" fill="#8b949e">More</text>')
P.append("</svg>")
open("contrib-heatmap.svg", "w").write("\n".join(P))
print("wrote contrib-heatmap.svg")
