#!/usr/bin/env python3
"""
Pulse Auto-Builder
Reads today's card from the schedule, builds HTML, pushes to GitHub.
Run manually or schedule via launchd to run every morning at 7am.
"""

import os
import subprocess
from datetime import date

# ============================================================
# CARD SCHEDULE — Ideka's cards, days 1-30
# ============================================================

CARDS = {
    # date: (label, quote, attribution)
    "2026-03-10": (
        "for a honey kind of day",
        "Some people colour your world without even trying.",
        "for you today"
    ),
    "2026-03-11": (
        "for a tuesday kind of mind",
        "The most interesting minds don't just see the world differently. They make you wonder why you ever saw it any other way.",
        "for you today"
    ),
    "2026-03-12": (
        "for a wednesday kind of energy",
        "Some days just have better energy than others. Today feels like one of those days.",
        "for you today"
    ),
    "2026-03-13": (
        "for the quiet observers",
        "Rare is the person who listens not to respond, but to understand. You'll know them by how seen they make you feel.",
        "for you today"
    ),
    "2026-03-14": (
        "for a friday kind of thought",
        "Art is never finished, only abandoned — but conversation between the right people never truly ends.",
        "for you today"
    ),
    "2026-03-15": (
        "for a slow saturday",
        "Saturday energy: Something warm in a mug. A thought that arrived uninvited and stayed for hours. Perfect.",
        "for you today"
    ),
    "2026-03-16": (
        "for a sunday kind of presence",
        "The people worth keeping are the ones who make silence feel like conversation and distance feel like presence.",
        "for you today"
    ),
    "2026-03-17": (
        "for a reflective monday",
        "We are drawn to flawed protagonists not because we excuse them, but because we recognise them. The best stories hold a mirror.",
        "for you today"
    ),
    "2026-03-18": (
        "for a tuesday plot twist",
        "Plot twist: The person who keeps showing up, paying attention, and remembering everything? That's the main character energy right there.",
        "for you today"
    ),
    "2026-03-19": (
        "for a wednesday worth noting",
        "To be truly known by someone — not performed for, not managed, just known — that is one of the rarest gifts in a noisy world.",
        "for you today"
    ),
}

# ============================================================
# HTML TEMPLATE
# ============================================================

def build_html(label, quote, attribution, date_str):
    # Format date nicely e.g. "March 10 · 2026"
    d = date.fromisoformat(date_str)
    months = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]
    pretty_date = f"{months[d.month-1]} {d.day} · {d.year}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Pulse</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Montserrat:wght@200;300;400&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 100%; height: 100%; overflow: hidden; }}
  body {{
    font-family: 'Cormorant Garamond', serif;
    background: linear-gradient(160deg, #2c1a00 0%, #1a0f00 100%);
    min-height: 100vh;
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 52px 36px 48px;
    position: relative;
    overflow: hidden;
    text-align: center;
  }}
  body::before {{
    content: '';
    position: absolute;
    width: 400px; height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(200,146,42,0.12) 0%, transparent 70%);
    top: -100px; right: -100px;
    pointer-events: none;
  }}
  body::after {{
    content: '';
    position: absolute;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(232,184,75,0.08) 0%, transparent 70%);
    bottom: -80px; left: -60px;
    pointer-events: none;
  }}
  .top-line {{
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #c8922a, #e8b84b, #c8922a, transparent);
  }}
  .bottom-line {{
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(200,146,42,0.4), transparent);
  }}
  .center {{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    opacity: 0;
    animation: fadeUp 1.2s ease forwards;
    animation-delay: 0.3s;
  }}
  .label {{
    font-family: 'Montserrat', sans-serif;
    font-size: 9px;
    font-weight: 400;
    letter-spacing: 5px;
    color: #c8922a;
    text-transform: uppercase;
    margin-bottom: 40px;
    opacity: 0.9;
  }}
  .deco {{
    width: 32px; height: 1px;
    background: linear-gradient(90deg, transparent, #e8b84b, transparent);
    margin-bottom: 36px;
  }}
  .quote-mark {{
    font-size: 80px;
    line-height: 0.6;
    color: #c8922a;
    opacity: 0.35;
    margin-bottom: 12px;
    font-style: italic;
  }}
  .quote {{
    font-size: 32px;
    font-weight: 300;
    font-style: italic;
    line-height: 1.6;
    color: #f5e6c8;
    letter-spacing: 0.3px;
    margin-bottom: 40px;
  }}
  .divider {{
    width: 48px; height: 1px;
    background: linear-gradient(90deg, transparent, #c8922a, transparent);
    margin-bottom: 20px;
  }}
  .attribution {{
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    font-weight: 300;
    letter-spacing: 3px;
    color: #c8922a;
    opacity: 0.75;
    text-transform: uppercase;
  }}
  .bottom {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    opacity: 0;
    animation: fadeUp 0.8s ease forwards;
    animation-delay: 0.8s;
  }}
  .honey-dot {{
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #e8b84b;
    opacity: 0.6;
    animation: glow 3s ease-in-out infinite;
  }}
  @keyframes glow {{
    0%, 100% {{ opacity: 0.6; transform: scale(1); }}
    50% {{ opacity: 1; transform: scale(1.5); }}
  }}
  .date-chip {{
    font-family: 'Montserrat', sans-serif;
    font-size: 9px;
    font-weight: 300;
    letter-spacing: 3px;
    color: #f5e6c8;
    opacity: 0.25;
    text-transform: uppercase;
  }}
  @keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}
</style>
</head>
<body>
<div class="top-line"></div>
<div class="center">
  <div class="label">{label}</div>
  <div class="deco"></div>
  <div class="quote-mark">"</div>
  <p class="quote">{quote}</p>
  <div class="divider"></div>
  <div class="attribution">{attribution}</div>
</div>
<div class="bottom">
  <div class="honey-dot"></div>
  <div class="date-chip">{pretty_date}</div>
</div>
<div class="bottom-line"></div>
</body>
</html>"""

# ============================================================
# MAIN — build today's card and push
# ============================================================

def main():
    today = date.today().isoformat()
    pulse_dir = os.path.expanduser("~/Pulse")

    if today not in CARDS:
        print(f"No card scheduled for {today}.")
        return

    label, quote, attribution = CARDS[today]
    html = build_html(label, quote, attribution, today)

    # Write index.html
    output_path = os.path.join(pulse_dir, "index.html")
    with open(output_path, "w") as f:
        f.write(html)
    print(f"✅ Card built for {today}")

    # Git push
    os.chdir(pulse_dir)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"Pulse {today}"], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"✅ Pushed to GitHub — Vercel deploying now")
    print(f"🔗 https://pulse-ruddy-three.vercel.app")

if __name__ == "__main__":
    main()
