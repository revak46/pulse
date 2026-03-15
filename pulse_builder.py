#!/usr/bin/env python3
"""
Pulse Auto-Builder
Builds two pages daily:
  - index.html  → Ideka's card (warm honey)
  - me.html     → Yemi's dashboard (his card dark bold + Ideka's card below)
Runs every morning at 7am via launchd.
"""

import os
import subprocess
from datetime import date

# ============================================================
# IDEKA'S CARDS
# ============================================================

IDEKA_CARDS = {
    "2026-03-10": ("for a honey kind of day", "Some people colour your world without even trying.", "for you today"),
    "2026-03-11": ("for a tuesday kind of mind", "The most interesting minds don't just see the world differently. They make you wonder why you ever saw it any other way.", "for you today"),
    "2026-03-12": ("for a thursday kind of energy", "Some days just have better energy than others. Today feels like one of those days.", "for you today"),
    "2026-03-13": ("for the quiet observers", "Rare is the person who listens not to respond, but to understand. You'll know them by how seen they make you feel.", "for you today"),
    "2026-03-14": ("for a friday kind of thought", "Art is never finished, only abandoned — but conversation between the right people never truly ends.", "for you today"),
    "2026-03-15": ("for a slow saturday", "Saturday energy: Something warm in a mug. A thought that arrived uninvited and stayed for hours. Perfect.", "for you today"),
    "2026-03-16": ("for a sunday kind of presence", "The people worth keeping are the ones who make silence feel like conversation and distance feel like presence.", "for you today"),
    "2026-03-17": ("for a reflective monday", "We are drawn to flawed protagonists not because we excuse them, but because we recognise them. The best stories hold a mirror.", "for you today"),
    "2026-03-18": ("for a tuesday plot twist", "Plot twist: The person who keeps showing up, paying attention, and remembering everything? That's the main character energy right there.", "for you today"),
    "2026-03-19": ("for a thursday worth noting", "To be truly known by someone — not performed for, not managed, just known — that is one of the rarest gifts in a noisy world.", "for you today"),
}

# ============================================================
# YEMI'S CARDS
# ============================================================

YEMI_CARDS = {
    "2026-03-10": ("concern but moderate", "Concern that knows its own name is already halfway to peace. You're more aware than you think.", "for you today"),
    "2026-03-11": ("for the builders", "Every great builder has a season where nothing looks finished. That's not failure. That's foundations.", "for you today"),
    "2026-03-12": ("for the ones becoming", "You are allowed to be a masterpiece and a work in progress at the same time.", "for you today"),
    "2026-03-13": ("for the intentional", "Clarity doesn't always arrive loudly. Sometimes it settles in like morning light — slowly, then all at once.", "for you today"),
    "2026-03-14": ("for the path", "The obstacle is the path. Not around it, not despite it — through it, the path reveals itself.", "for you today"),
    "2026-03-15": ("permission to rest", "Rest is not a reward for finishing. Rest is part of the work. Take it without apology.", "for you today"),
    "2026-03-16": ("for new chapters", "Sunday is not the end of the week. It is the breath before the next chapter begins.", "for you today"),
    "2026-03-17": ("for the direction", "Leadership is not about being in front. It is about knowing which direction is worth walking in.", "for you today"),
    "2026-03-18": ("for the in between", "Not every day has a colour yet. Some days are still deciding. That's fine — so are you.", "for you today"),
    "2026-03-19": ("keep moving", "You don't have to have it all figured out. You just have to keep moving with intention.", "for you today"),
}

# ============================================================
# IDEKA HTML — warm honey design
# ============================================================

def build_ideka_html(label, quote, attribution, date_str):
    d = date.fromisoformat(date_str)
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
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
    min-height: 100vh; min-height: 100dvh;
    display: flex; flex-direction: column;
    align-items: center; justify-content: space-between;
    padding: 52px 36px 48px;
    position: relative; overflow: hidden; text-align: center;
  }}
  body::before {{ content: ''; position: absolute; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(200,146,42,0.12) 0%, transparent 70%); top: -100px; right: -100px; pointer-events: none; }}
  body::after {{ content: ''; position: absolute; width: 300px; height: 300px; border-radius: 50%; background: radial-gradient(circle, rgba(232,184,75,0.08) 0%, transparent 70%); bottom: -80px; left: -60px; pointer-events: none; }}
  .top-line {{ position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #c8922a, #e8b84b, #c8922a, transparent); }}
  .bottom-line {{ position: absolute; bottom: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(200,146,42,0.4), transparent); }}
  .center {{ width: 100%; display: flex; flex-direction: column; align-items: center; opacity: 0; animation: fadeUp 1.2s ease forwards; animation-delay: 0.3s; }}
  .label {{ font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 400; letter-spacing: 5px; color: #c8922a; text-transform: uppercase; margin-bottom: 40px; opacity: 0.9; }}
  .deco {{ width: 32px; height: 1px; background: linear-gradient(90deg, transparent, #e8b84b, transparent); margin-bottom: 36px; }}
  .quote-mark {{ font-size: 80px; line-height: 0.6; color: #c8922a; opacity: 0.35; margin-bottom: 12px; font-style: italic; }}
  .quote {{ font-size: 32px; font-weight: 300; font-style: italic; line-height: 1.6; color: #f5e6c8; letter-spacing: 0.3px; margin-bottom: 40px; }}
  .divider {{ width: 48px; height: 1px; background: linear-gradient(90deg, transparent, #c8922a, transparent); margin-bottom: 20px; }}
  .attribution {{ font-family: 'Montserrat', sans-serif; font-size: 10px; font-weight: 300; letter-spacing: 3px; color: #c8922a; opacity: 0.75; text-transform: uppercase; }}
  .bottom {{ display: flex; flex-direction: column; align-items: center; gap: 16px; opacity: 0; animation: fadeUp 0.8s ease forwards; animation-delay: 0.8s; }}
  .honey-dot {{ width: 5px; height: 5px; border-radius: 50%; background: #e8b84b; opacity: 0.6; animation: glow 3s ease-in-out infinite; }}
  @keyframes glow {{ 0%, 100% {{ opacity: 0.6; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.5); }} }}
  .date-chip {{ font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 300; letter-spacing: 3px; color: #f5e6c8; opacity: 0.25; text-transform: uppercase; }}
  @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
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
# YEMI DASHBOARD HTML — his card (dark bold) + Ideka's below
# ============================================================

def build_yemi_html(y_label, y_quote, y_attribution, i_label, i_quote, i_attribution, date_str):
    d = date.fromisoformat(date_str)
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    pretty_date = f"{months[d.month-1]} {d.day} · {d.year}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Pulse — My View</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Montserrat:wght@200;300;400&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 100%; }}
  body {{ font-family: 'Cormorant Garamond', serif; background: #0a0a0a; }}

  /* ── YEMI SECTION — dark bold ── */
  .yemi-section {{
    min-height: 100vh; min-height: 100dvh;
    background: linear-gradient(160deg, #0d0d1a 0%, #0a0a0a 100%);
    display: flex; flex-direction: column;
    align-items: center; justify-content: space-between;
    padding: 52px 36px 48px;
    position: relative; overflow: hidden; text-align: center;
  }}
  .yemi-section::before {{ content: ''; position: absolute; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(89,141,255,0.08) 0%, transparent 70%); top: -100px; right: -100px; pointer-events: none; }}
  .y-top-line {{ position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #3a5fc8, #5a82ff, #3a5fc8, transparent); }}
  .y-center {{ width: 100%; display: flex; flex-direction: column; align-items: center; opacity: 0; animation: fadeUp 1.2s ease forwards; animation-delay: 0.3s; }}
  .y-tag {{ font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 400; letter-spacing: 5px; color: #5a82ff; text-transform: uppercase; margin-bottom: 40px; opacity: 0.9; }}
  .y-deco {{ width: 32px; height: 1px; background: linear-gradient(90deg, transparent, #5a82ff, transparent); margin-bottom: 36px; }}
  .y-quote-mark {{ font-size: 80px; line-height: 0.6; color: #5a82ff; opacity: 0.25; margin-bottom: 12px; font-style: italic; }}
  .y-quote {{ font-size: 32px; font-weight: 300; font-style: italic; line-height: 1.6; color: #e8e8ff; letter-spacing: 0.3px; margin-bottom: 40px; }}
  .y-divider {{ width: 48px; height: 1px; background: linear-gradient(90deg, transparent, #5a82ff, transparent); margin-bottom: 20px; }}
  .y-attribution {{ font-family: 'Montserrat', sans-serif; font-size: 10px; font-weight: 300; letter-spacing: 3px; color: #5a82ff; opacity: 0.75; text-transform: uppercase; }}
  .y-bottom {{ display: flex; flex-direction: column; align-items: center; gap: 16px; opacity: 0; animation: fadeUp 0.8s ease forwards; animation-delay: 0.8s; }}
  .y-dot {{ width: 5px; height: 5px; border-radius: 50%; background: #5a82ff; opacity: 0.6; animation: glow 3s ease-in-out infinite; }}
  .y-date {{ font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 300; letter-spacing: 3px; color: #e8e8ff; opacity: 0.2; text-transform: uppercase; }}

  /* ── DIVIDER BETWEEN SECTIONS ── */
  .section-divider {{
    background: #0a0a0a;
    padding: 24px 36px;
    display: flex; align-items: center; gap: 16px;
  }}
  .section-divider::before, .section-divider::after {{
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  }}
  .divider-label {{
    font-family: 'Montserrat', sans-serif;
    font-size: 8px; letter-spacing: 4px;
    color: rgba(255,255,255,0.2); text-transform: uppercase;
    white-space: nowrap;
  }}

  /* ── SEND BUTTON ── */
  .send-section {{
    background: #0a0a0a;
    padding: 0 36px 24px;
    display: flex; justify-content: center;
  }}
  .send-btn {{
    font-family: 'Montserrat', sans-serif;
    font-size: 9px; font-weight: 400;
    letter-spacing: 4px; text-transform: uppercase;
    color: #c8922a;
    background: rgba(200,146,42,0.08);
    border: 1px solid rgba(200,146,42,0.3);
    border-radius: 2px;
    padding: 12px 28px;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    transition: all 0.2s ease;
  }}
  .send-btn:active {{ background: rgba(200,146,42,0.2); }}

  /* ── IDEKA SECTION — warm honey ── */
  .ideka-section {{
    min-height: 100vh; min-height: 100dvh;
    background: linear-gradient(160deg, #2c1a00 0%, #1a0f00 100%);
    display: flex; flex-direction: column;
    align-items: center; justify-content: space-between;
    padding: 52px 36px 48px;
    position: relative; overflow: hidden; text-align: center;
  }}
  .ideka-section::before {{ content: ''; position: absolute; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(200,146,42,0.12) 0%, transparent 70%); top: -100px; right: -100px; pointer-events: none; }}
  .ideka-section::after {{ content: ''; position: absolute; width: 300px; height: 300px; border-radius: 50%; background: radial-gradient(circle, rgba(232,184,75,0.08) 0%, transparent 70%); bottom: -80px; left: -60px; pointer-events: none; }}
  .i-top-line {{ position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #c8922a, #e8b84b, #c8922a, transparent); }}
  .i-bottom-line {{ position: absolute; bottom: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(200,146,42,0.4), transparent); }}
  .i-center {{ width: 100%; display: flex; flex-direction: column; align-items: center; }}
  .i-label {{ font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 400; letter-spacing: 5px; color: #c8922a; text-transform: uppercase; margin-bottom: 40px; opacity: 0.9; }}
  .i-deco {{ width: 32px; height: 1px; background: linear-gradient(90deg, transparent, #e8b84b, transparent); margin-bottom: 36px; }}
  .i-quote-mark {{ font-size: 80px; line-height: 0.6; color: #c8922a; opacity: 0.35; margin-bottom: 12px; font-style: italic; }}
  .i-quote {{ font-size: 32px; font-weight: 300; font-style: italic; line-height: 1.6; color: #f5e6c8; letter-spacing: 0.3px; margin-bottom: 40px; }}
  .i-divider {{ width: 48px; height: 1px; background: linear-gradient(90deg, transparent, #c8922a, transparent); margin-bottom: 20px; }}
  .i-attribution {{ font-family: 'Montserrat', sans-serif; font-size: 10px; font-weight: 300; letter-spacing: 3px; color: #c8922a; opacity: 0.75; text-transform: uppercase; }}
  .i-bottom {{ display: flex; flex-direction: column; align-items: center; gap: 16px; }}
  .i-dot {{ width: 5px; height: 5px; border-radius: 50%; background: #e8b84b; opacity: 0.6; animation: glow 3s ease-in-out infinite; }}
  .i-date {{ font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 300; letter-spacing: 3px; color: #f5e6c8; opacity: 0.25; text-transform: uppercase; }}

  /* ── SCROLL HINT ── */
  .scroll-hint {{
    position: absolute; bottom: 80px; left: 50%; transform: translateX(-50%);
    font-family: 'Montserrat', sans-serif;
    font-size: 8px; letter-spacing: 3px; text-transform: uppercase;
    color: rgba(255,255,255,0.2);
    animation: bounce 2s ease-in-out infinite;
  }}
  @keyframes bounce {{ 0%, 100% {{ transform: translateX(-50%) translateY(0); }} 50% {{ transform: translateX(-50%) translateY(6px); }} }}

  @keyframes glow {{ 0%, 100% {{ opacity: 0.6; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.5); }} }}
  @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
</style>
</head>
<body>

<!-- YEMI'S CARD -->
<div class="yemi-section">
  <div class="y-top-line"></div>
  <div class="y-center">
    <div class="y-tag">{y_label}</div>
    <div class="y-deco"></div>
    <div class="y-quote-mark">"</div>
    <p class="y-quote">{y_quote}</p>
    <div class="y-divider"></div>
    <div class="y-attribution">{y_attribution}</div>
  </div>
  <div class="y-bottom">
    <div class="y-dot"></div>
    <div class="y-date">{pretty_date}</div>
  </div>
  <div class="scroll-hint">↓ her card</div>
</div>

<!-- SECTION DIVIDER + SEND BUTTON -->
<div class="section-divider">
  <span class="divider-label">her card today</span>
</div>
<div class="send-section">
  <a class="send-btn" href="https://pulse-ruddy-three.vercel.app" target="_blank">↗ open to send</a>
</div>

<!-- IDEKA'S CARD PREVIEW -->
<div class="ideka-section">
  <div class="i-top-line"></div>
  <div class="i-center">
    <div class="i-label">{i_label}</div>
    <div class="i-deco"></div>
    <div class="i-quote-mark">"</div>
    <p class="i-quote">{i_quote}</p>
    <div class="i-divider"></div>
    <div class="i-attribution">{i_attribution}</div>
  </div>
  <div class="i-bottom">
    <div class="i-dot"></div>
    <div class="i-date">{pretty_date}</div>
  </div>
  <div class="i-bottom-line"></div>
</div>

</body>
</html>"""

# ============================================================
# MAIN
# ============================================================

def main():
    today = date.today().isoformat()
    pulse_dir = os.path.expanduser("~/Pulse")

    if today not in IDEKA_CARDS or today not in YEMI_CARDS:
        print(f"No cards scheduled for {today}.")
        return

    i_label, i_quote, i_attribution = IDEKA_CARDS[today]
    y_label, y_quote, y_attribution = YEMI_CARDS[today]

    # Build Ideka's page
    ideka_html = build_ideka_html(i_label, i_quote, i_attribution, today)
    with open(os.path.join(pulse_dir, "index.html"), "w") as f:
        f.write(ideka_html)

    # Build Yemi's dashboard
    yemi_html = build_yemi_html(y_label, y_quote, y_attribution, i_label, i_quote, i_attribution, today)
    with open(os.path.join(pulse_dir, "me.html"), "w") as f:
        f.write(yemi_html)

    print(f"✅ Both cards built for {today}")

    # Git push
    os.chdir(pulse_dir)
    subprocess.run(["git", "add", "."], check=True)
    commit = subprocess.run(["git", "commit", "-m", f"Pulse {today}"])
    if commit.returncode == 0:
        subprocess.run(["git", "push"], check=True)
        print(f"✅ Pushed to GitHub")
    else:
        print(f"ℹ️  Nothing new to push — cards already live")

    print(f"🔗 Your card:   https://pulse-ruddy-three.vercel.app/me")
    print(f"🔗 Her card:    https://pulse-ruddy-three.vercel.app")

if __name__ == "__main__":
    main()
