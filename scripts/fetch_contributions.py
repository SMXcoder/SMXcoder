"""Scrape the public contribution calendar (no token needed) -> data/contributions.json
Usage: python scripts/fetch_contributions.py [--sample]"""
import json, re, sys, random, datetime as dt
from collections import OrderedDict

cfg = json.load(open("config.json"))
user = cfg["username"]

def fetch():
    import requests
    from bs4 import BeautifulSoup
    r = requests.get(f"https://github.com/users/{user}/contributions",
                     headers={"User-Agent": "Mozilla/5.0 (profile-readme-bot)"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        m = re.match(r"(\d+)\s+contribution", tips.get(td.get("id"), ""))
        days.append({"date": td["data-date"], "count": int(m.group(1)) if m else 0,
                     "level": int(td.get("data-level", 0))})
    if not days:
        raise SystemExit("No contribution cells found - check username / GitHub markup change.")
    return sorted(days, key=lambda d: d["date"])

def sample():
    random.seed(7)
    end = dt.date.today(); start = end - dt.timedelta(days=364)
    days = []
    for i in range(365):
        d = start + dt.timedelta(days=i)
        c = 0 if d.weekday() >= 5 and random.random() < .6 else max(0, int(random.gauss(4, 4)))
        if random.random() < .15: c = 0
        lvl = 0 if c == 0 else 1 if c < 3 else 2 if c < 6 else 3 if c < 10 else 4 if c < 15 else 5
        days.append({"date": d.isoformat(), "count": c, "level": lvl})
    return days

days = sample() if "--sample" in sys.argv else fetch()

cur = longest = run = 0
for d in days:
    run = run + 1 if d["count"] else 0
    longest = max(longest, run)
for d in reversed(days):          # current streak (allow today to be empty)
    if d["count"]: cur += 1
    elif d is days[-1]: continue
    else: break
monthly = OrderedDict()
for d in days:
    monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]
best = max(days, key=lambda d: d["count"])
out = {"username": user, "total": sum(d["count"] for d in days), "current_streak": cur,
       "longest_streak": longest, "best_day": best, "monthly": monthly, "days": days}
json.dump(out, open("data/contributions.json", "w"), indent=1)
print(f"{out['total']} contributions, streak {cur}/{longest}")
