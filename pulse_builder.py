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
    "2026-03-11": ("for a wednesday kind of mind", "The most interesting minds don't just see the world differently. They make you wonder why you ever saw it any other way.", "for you today"),
    "2026-03-12": ("for a thursday kind of energy", "Friendaversaries, six-month countdowns, keeping score of every 'no' — some people were built to notice everything. Lucky are the ones who get noticed.", "for you today"),
    "2026-03-13": ("for the quiet observers", "Rare is the person who listens not to respond, but to understand. You'll know them by how seen they make you feel.", "for you today"),
    "2026-03-14": ("for a saturday kind of thought", "Art is never finished, only abandoned — but conversation between the right people never truly ends.", "for you today"),
    "2026-03-15": ("for a slow sunday", "Sunday energy: Soft blanket. Something warm in a mug. A thought that arrived uninvited and stayed for hours. Perfect.", "for you today"),
    "2026-03-16": ("for a monday kind of presence", "The people worth keeping are the ones who make silence feel like conversation and distance feel like presence.", "for you today"),
    "2026-03-17": ("for a reflective tuesday", "We are drawn to flawed protagonists not because we excuse them, but because we recognise them. The best stories hold a mirror.", "for you today"),
    "2026-03-18": ("for a wednesday plot twist", "Plot twist: The person who keeps showing up, paying attention, and remembering everything? That's the main character energy right there.", "for you today"),
    "2026-03-19": ("for a thursday worth noting", "To be truly known by someone — not performed for, not managed, just known — that is one of the rarest gifts in a noisy world.", "for you today"),
    "2026-03-20": ("for the first day of spring", "Spring doesn't ask permission to begin again. It just does. There's a lesson in that for the rest of us.", "for you today"),
    "2026-03-21": ("for a saturday conversation", "You ever have a conversation so good it ruins small talk forever? Yeah. That.", "for you today"),
    "2026-03-22": ("for the ones that feel inevitable", "Some connections don't need explaining. They just make sense in a language neither person had to learn.", "for you today"),
    "2026-03-23": ("for a monday that feels like home", "The aunties, the comfort food, the cuddles — home is not always a place. Sometimes it's a feeling you carry and occasionally share.", "for you today"),
    "2026-03-24": ("halfway and still here", "Halfway through March and you're still here, still noticing, still keeping count of things that matter. Honestly? Impressive.", "for you today"),
    "2026-03-25": ("for the ones who reframe everything", "There are people who enter your story and somehow make every chapter before them feel like prologue.", "for you today"),
    "2026-03-26": ("for a thursday kind of courage", "Independent thought is an act of courage disguised as an opinion. Not everyone has the nerve.", "for you today"),
    "2026-03-27": ("even the flowers are dramatic", "Allergy season reminder: Even the flowers are dramatic in spring. You're allowed to be too.", "for you today"),
    "2026-03-28": ("for the observers who wait for real", "Depth is not common. Neither is the patience to find it in someone else. You have both.", "for you today"),
    "2026-03-29": ("for the ones who carry defiance quietly", "Art defies. That's its whole job. And the people who love art deeply — they carry that defiance quietly inside them.", "for you today"),
    "2026-03-30": ("monday report", "Monday report: Still intellectually dangerous. Still noticing everything. Still keeping score. No notes.", "for you today"),
    "2026-03-31": ("last day of march", "March taught us: things that take their time arriving are usually worth the wait.", "for you today"),
    "2026-04-01": ("new month, same curious mind", "New month. Same curious mind. Different questions. That's growth dressed in ordinary clothes.", "for you today"),
    "2026-04-02": ("for the most interesting thursday", "Two chess players, talking philosophy over coffee, keeping count of everything — honestly sounds like the most interesting Tuesday anyone has ever had.", "for you today"),
    "2026-04-03": ("for the ones who speak the same language", "The conversations that last hours are never really about the topic. They're about the recognition — finally, someone who speaks the same language.", "for you today"),
    "2026-04-04": ("for the guarded ones worth waiting for", "Vulnerability is not weakness. It is the decision that connection matters more than the risk of being known.", "for you today"),
    "2026-04-05": ("spring is being extra again", "Spring is basically nature's way of being extra. Colour everywhere, everything blooming at once, dramatic temperature changes. Iconic behaviour honestly.", "for you today"),
    "2026-04-06": ("for someone's highlight", "To be someone's highlight — not their everything, not their anchor, just their highlight — that is a quietly beautiful thing to be.", "for you today"),
    "2026-04-07": ("for the ones who prefer depth over speed", "The most honest relationships are built slowly, with questions, with patience, with the willingness to not rush the knowing.", "for you today"),
    "2026-04-08": ("thirty days of being noticed", "Thirty days of being noticed, thought of, and sent something made just for you. Still keeping count? Because I am.", "for you today"),
}

# ============================================================
# IDEKA — per-day background images (falls back to default)
# ============================================================

IDEKA_IMAGES = {
    "2026-03-15": "i1_table_setting.jpg",
}
DEFAULT_IDEKA_IMAGE = "i5_clutch_perfume.jpg"


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
    "2026-03-20": ("both at once", "Equinox: the one day the world is perfectly balanced between dark and light. Some days you get to be both.", "for you today"),
    "2026-03-21": ("you earned the weekend", "Saturday is just the universe's way of saying — you made it, now exhale.", "for you today"),
    "2026-03-22": ("for the quiet builders", "The work you do in private becomes the life you live in public. Keep going.", "for you today"),
    "2026-03-23": ("two weeks", "Two weeks of showing up. That's not a streak. That's a statement of character.", "for you today"),
    "2026-03-24": ("halfway", "Halfway means you've already proven you can. The second half is just confirming what you already know.", "for you today"),
    "2026-03-25": ("for the ones still becoming", "Every version of you that got you here deserves acknowledgement — even the uncertain ones.", "for you today"),
    "2026-03-26": ("vision and execution", "Vision without execution is just imagination. But execution without vision is just motion. You need both.", "for you today"),
    "2026-03-27": ("you showed up", "Some days the only win is that you showed up despite everything. Today counts.", "for you today"),
    "2026-03-28": ("a gift with a sharp edge", "The fact that you notice things others miss — that's not overthinking. That's a gift with a sharp edge.", "for you today"),
    "2026-03-29": ("your chapter", "The most dangerous thing you can do is compare your chapter three to someone else's chapter twenty.", "for you today"),
    "2026-03-30": ("three weeks in", "Three weeks in. At this point it's not discipline anymore. It's just who you are.", "for you today"),
    "2026-03-31": ("look how far", "You started this month with concern but moderate. Look how far that got you.", "for you today"),
    "2026-04-01": ("new month energy", "April is the universe asking: who do you want to be now that spring has cleared the air?", "for you today"),
    "2026-04-02": ("about to be heard", "You've been building quietly for a while now. April is when quiet starts to echo.", "for you today"),
    "2026-04-03": ("the most honest thing", "Consistency is not glamorous. It is just the most honest thing a person can do.", "for you today"),
    "2026-04-04": ("for the architects", "Every system you build now is future-you saying thank you.", "for you today"),
    "2026-04-05": ("because you decided to", "Three more days. Not because you have to — because you decided to. That's the whole point.", "for you today"),
    "2026-04-06": ("notice that", "The version of you that started this 30 days ago and the version finishing it are not the same person. Notice that.", "for you today"),
    "2026-04-07": ("nobody can take that back", "One more day. What you've built here — in thirty days of showing up — nobody can take that back.", "for you today"),
    "2026-04-08": ("what colour is today", "You said concern but moderate on day one. Thirty days later — what colour is today?", "for you today"),
}

# ============================================================
# IDEKA HTML — warm honey design
# ============================================================

def build_ideka_html(label, quote, attribution, date_str, image="i5_clutch_perfume.jpg"):
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
    background:
      linear-gradient(180deg,
        rgba(28,14,4,0.54) 0%,
        rgba(18,10,2,0.22) 28%,
        rgba(18,10,2,0.56) 62%,
        rgba(10,5,1,0.94) 100%),
      url('images/{image}') center / cover no-repeat;
    min-height: 100vh; min-height: 100dvh;
    display: flex; flex-direction: column;
    align-items: center; justify-content: space-between;
    padding: 52px 36px 48px;
    position: relative; overflow: hidden; text-align: center;
  }}
  body::before {{ content: ''; position: absolute; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(200,146,42,0.10) 0%, transparent 70%); top: -100px; right: -100px; pointer-events: none; }}
  body::after {{ content: ''; position: absolute; width: 300px; height: 300px; border-radius: 50%; background: radial-gradient(circle, rgba(232,184,75,0.07) 0%, transparent 70%); bottom: -80px; left: -60px; pointer-events: none; }}
  .top-line {{ position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #c8922a, #e8b84b, #c8922a, transparent); }}
  .bottom-line {{ position: absolute; bottom: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(200,146,42,0.4), transparent); }}
  .center {{ width: 100%; display: flex; flex-direction: column; align-items: center; opacity: 0; animation: fadeUp 1.2s ease forwards; animation-delay: 0.3s; }}
  .label {{ font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 400; letter-spacing: 5px; color: #c8922a; text-transform: uppercase; margin-bottom: 40px; opacity: 0.9; }}
  .deco {{ width: 32px; height: 1px; background: linear-gradient(90deg, transparent, #e8b84b, transparent); margin-bottom: 36px; }}
  .quote-mark {{ font-size: 80px; line-height: 0.6; color: #c8922a; opacity: 0.35; margin-bottom: 12px; font-style: italic; }}
  .quote {{ font-size: 32px; font-weight: 300; font-style: italic; line-height: 1.6; color: #f5e6c8; letter-spacing: 0.3px; margin-bottom: 40px; text-shadow: 0 2px 20px rgba(0,0,0,0.95); }}
  .divider {{ width: 48px; height: 1px; background: linear-gradient(90deg, transparent, #c8922a, transparent); margin-bottom: 20px; }}
  .attribution {{ font-family: 'Montserrat', sans-serif; font-size: 10px; font-weight: 300; letter-spacing: 3px; color: #c8922a; opacity: 0.75; text-transform: uppercase; }}
  .bottom {{ display: flex; flex-direction: column; align-items: center; gap: 16px; opacity: 0; animation: fadeUp 0.8s ease forwards; animation-delay: 0.8s; }}
  .honey-dot {{ width: 5px; height: 5px; border-radius: 50%; background: #e8b84b; opacity: 0.6; animation: glow 3s ease-in-out infinite; }}
  @keyframes glow {{ 0%, 100% {{ opacity: 0.6; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.5); }} }}
  .date-chip {{ font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 300; letter-spacing: 3px; color: #f5e6c8; opacity: 0.25; text-transform: uppercase; }}
  @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}

  /* ── SHIMMER SWEEP ── */
  .shimmer-stripe {{
    position: absolute; top: 0; left: 0;
    width: 38%; height: 100%;
    background: linear-gradient(90deg,
      transparent 0%,
      rgba(255,248,180,0.22) 28%,
      rgba(255,255,240,0.44) 50%,
      rgba(255,248,180,0.22) 72%,
      transparent 100%
    );
    mix-blend-mode: overlay;
    transform: translateX(-100%);
    animation: shimmerSlide 2.6s cubic-bezier(0.4,0,0.2,1) 1.6s 1 forwards;
    pointer-events: none;
    z-index: 3;
  }}
  @keyframes shimmerSlide {{
    0%   {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(370%); }}
  }}

  /* ── AMBIENT PARTICLES ── */
  #particles  {{ position: absolute; inset: 0; pointer-events: none; overflow: hidden;  z-index: 1; }}
  #wordglitter {{ position: absolute; inset: 0; pointer-events: none; overflow: visible; z-index: 5; }}
  @keyframes particleDrift {{
    0%   {{ transform: translateY(0) scale(1);   opacity: 0; }}
    10%  {{ opacity: 1; }}
    85%  {{ opacity: 0.9; }}
    100% {{ transform: translateY(-100px) scale(0.15); opacity: 0; }}
  }}
  @keyframes particleSparkle {{
    0%, 100% {{ opacity: 0.1; transform: scale(0.6); }}
    50%       {{ opacity: 1;   transform: scale(1.6); }}
  }}
  .center {{ z-index: 2; position: relative; }}
  .bottom {{ z-index: 2; position: relative; }}
  .top-line, .bottom-line {{ z-index: 4; }}

  /* ── TEXT GLITTER ── */
  .quote {{
    background: linear-gradient(90deg,
      #c8922a  0%,
      #f5e6c8 10%,
      #fffbe6 18%,
      #ffd700 25%,
      #fff4b0 32%,
      #f5e6c8 42%,
      #e8b84b 52%,
      #fffbe6 60%,
      #ffd700 67%,
      #fff4b0 74%,
      #f5e6c8 84%,
      #ffe08a 92%,
      #c8922a 100%
    );
    background-size: 260% 100%;
    background-position: 160% center;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    filter: drop-shadow(0 0 12px rgba(232,184,75,0.45));
    animation: textGlitter 5s linear 1.4s infinite;
  }}
  @keyframes textGlitter {{
    0%   {{ background-position: 160% center; }}
    100% {{ background-position: -60% center; }}
  }}
</style>
</head>
<body>
<div id="particles"></div>
<div id="wordglitter"></div>
<div class="shimmer-stripe"></div>
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
<script>
(function(){{
  var pc=document.getElementById('particles');
  var driftCols=['rgba(255,210,50,0.95)','rgba(232,184,75,0.92)','rgba(255,235,120,0.88)','rgba(255,200,40,0.85)','rgba(248,220,90,0.80)'];
  for(var i=0;i<26;i++){{
    var p=document.createElement('div');
    var sz=(Math.random()*3+1.5).toFixed(2);
    var glow=parseFloat(sz)*2.5;
    var col=driftCols[Math.floor(Math.random()*driftCols.length)];
    var glowCol=col.replace(/[\d.]+\)$/,'0.6)');
    p.style.cssText=['position:absolute','width:'+sz+'px','height:'+sz+'px','left:'+(Math.random()*90+5).toFixed(1)+'%','top:'+(Math.random()*88+6).toFixed(1)+'%','background:'+col,'border-radius:50%','box-shadow:0 0 '+glow+'px '+glow+'px '+glowCol,'animation:particleDrift '+(Math.random()*8+6).toFixed(1)+'s ease-in-out '+(Math.random()*18).toFixed(1)+'s infinite','pointer-events:none'].join(';');
    pc.appendChild(p);
  }}
  var sparkCols=['rgba(255,220,60,1)','rgba(255,245,160,1)','rgba(232,184,75,1)'];
  for(var j=0;j<12;j++){{
    var s=document.createElement('div');
    var ssz=(Math.random()*2+1.8).toFixed(2);
    var sglow=parseFloat(ssz)*3;
    var scol=sparkCols[Math.floor(Math.random()*sparkCols.length)];
    s.style.cssText=['position:absolute','width:'+ssz+'px','height:'+ssz+'px','left:'+(Math.random()*90+5).toFixed(1)+'%','top:'+(Math.random()*88+6).toFixed(1)+'%','background:'+scol,'border-radius:50%','box-shadow:0 0 '+sglow+'px '+sglow+'px rgba(255,200,50,0.7)','animation:particleSparkle '+(Math.random()*3+2).toFixed(1)+'s ease-in-out '+(Math.random()*6).toFixed(1)+'s infinite','pointer-events:none'].join(';');
    pc.appendChild(s);
  }}
}})();
(function(){{
  var wg=document.getElementById('wordglitter');
  var gc=['rgba(255,215,50,1)','rgba(255,235,120,0.97)','rgba(232,184,75,0.95)','rgba(255,255,160,0.92)','rgba(248,210,60,0.98)'];
  function spawnFaller(){{
    var p=document.createElement('div');
    var W=window.innerWidth,H=window.innerHeight;
    var sz=(Math.random()*3.5+1.2).toFixed(1);
    var gl=parseFloat(sz)*2.8;
    var col=gc[Math.floor(Math.random()*gc.length)];
    var sx=(0.10+Math.random()*0.80)*W;
    var sy=(0.32+Math.random()*0.26)*H;
    var fall=Math.random()*140+90;
    var drift=(Math.random()-0.5)*80;
    var rot=(Math.random()>0.5?1:-1)*(Math.random()*360+180);
    var dur=Math.random()*2000+2200;
    var radius=Math.random()>0.35?'50%':'30%';
    var aspect=Math.random()>0.35?sz:(parseFloat(sz)*0.55).toFixed(1);
    p.style.cssText=['position:absolute','width:'+sz+'px','height:'+aspect+'px','left:'+sx.toFixed(0)+'px','top:'+sy.toFixed(0)+'px','background:'+col,'border-radius:'+radius,'box-shadow:0 0 '+gl+'px '+gl+'px rgba(255,200,50,0.65)','pointer-events:none'].join(';');
    wg.appendChild(p);
    var anim=p.animate([{{transform:'translateY(0px) translateX(0px) rotate(0deg)',opacity:1}},{{transform:'translateY('+fall+'px) translateX('+drift+'px) rotate('+rot+'deg)',opacity:0}}],{{duration:dur,easing:'ease-in',fill:'forwards'}});
    anim.onfinish=function(){{if(wg.contains(p))wg.removeChild(p);}};
  }}
  for(var k=0;k<12;k++){{setTimeout(spawnFaller,1400+k*150);}}
  setInterval(spawnFaller,500);
}})();
</script>
</body>
</html>"""

# ============================================================
# YEMI DASHBOARD HTML — his card (dark bold) + Ideka's below
# ============================================================

def build_yemi_html(y_label, y_quote, y_attribution, i_label, i_quote, i_attribution, date_str, i_image="i5_clutch_perfume.jpg"):
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

  /* ── IDEKA SECTION — warm honey + glitter ── */
  .ideka-section {{
    min-height: 100vh; min-height: 100dvh;
    background:
      linear-gradient(180deg,
        rgba(28,14,4,0.54) 0%,
        rgba(18,10,2,0.22) 28%,
        rgba(18,10,2,0.56) 62%,
        rgba(10,5,1,0.94) 100%),
      url('images/{i_image}') center / cover no-repeat;
    display: flex; flex-direction: column;
    align-items: center; justify-content: space-between;
    padding: 52px 36px 48px;
    position: relative; overflow: hidden; text-align: center;
  }}
  .ideka-section::before {{ content: ''; position: absolute; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(200,146,42,0.10) 0%, transparent 70%); top: -100px; right: -100px; pointer-events: none; }}
  .ideka-section::after {{ content: ''; position: absolute; width: 300px; height: 300px; border-radius: 50%; background: radial-gradient(circle, rgba(232,184,75,0.07) 0%, transparent 70%); bottom: -80px; left: -60px; pointer-events: none; }}
  .i-top-line {{ position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #c8922a, #e8b84b, #c8922a, transparent); }}
  .i-bottom-line {{ position: absolute; bottom: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(200,146,42,0.4), transparent); }}
  .i-center {{ width: 100%; display: flex; flex-direction: column; align-items: center; }}
  .i-label {{ font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 400; letter-spacing: 5px; color: #c8922a; text-transform: uppercase; margin-bottom: 40px; opacity: 0.9; }}
  .i-deco {{ width: 32px; height: 1px; background: linear-gradient(90deg, transparent, #e8b84b, transparent); margin-bottom: 36px; }}
  .i-quote-mark {{ font-size: 80px; line-height: 0.6; color: #c8922a; opacity: 0.35; margin-bottom: 12px; font-style: italic; }}
  .i-quote {{
    font-size: 32px; font-weight: 300; font-style: italic; line-height: 1.6; letter-spacing: 0.3px; margin-bottom: 40px;
    background: linear-gradient(90deg,
      #c8922a  0%, #f5e6c8 10%, #fffbe6 18%, #ffd700 25%,
      #fff4b0 32%, #f5e6c8 42%, #e8b84b 52%, #fffbe6 60%,
      #ffd700 67%, #fff4b0 74%, #f5e6c8 84%, #ffe08a 92%, #c8922a 100%
    );
    background-size: 260% 100%;
    background-position: 160% center;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    filter: drop-shadow(0 0 12px rgba(232,184,75,0.45));
    animation: iTextGlitter 5s linear 1.4s infinite;
  }}
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

  /* ── IDEKA SECTION SHIMMER & PARTICLES ── */
  .i-shimmer-stripe {{
    position: absolute; top: 0; left: 0;
    width: 38%; height: 100%;
    background: linear-gradient(90deg,
      transparent 0%,
      rgba(255,248,180,0.22) 28%,
      rgba(255,255,240,0.44) 50%,
      rgba(255,248,180,0.22) 72%,
      transparent 100%
    );
    mix-blend-mode: overlay;
    transform: translateX(-100%);
    animation: shimmerSlide 2.6s cubic-bezier(0.4,0,0.2,1) 1.6s 1 forwards;
    pointer-events: none;
    z-index: 3;
  }}
  @keyframes shimmerSlide {{
    0%   {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(370%); }}
  }}
  #i-particles  {{ position: absolute; inset: 0; pointer-events: none; overflow: hidden; z-index: 1; }}
  #i-wordglitter {{ position: absolute; inset: 0; pointer-events: none; overflow: visible; z-index: 5; }}
  .i-center {{ z-index: 2; position: relative; }}
  .i-bottom {{ z-index: 2; position: relative; }}
  .i-top-line {{ z-index: 4; position: relative; }}
  .i-bottom-line {{ z-index: 4; position: relative; }}
  @keyframes iParticleDrift {{
    0%   {{ transform: translateY(0) scale(1);   opacity: 0; }}
    10%  {{ opacity: 1; }}
    85%  {{ opacity: 0.9; }}
    100% {{ transform: translateY(-100px) scale(0.15); opacity: 0; }}
  }}
  @keyframes iParticleSparkle {{
    0%, 100% {{ opacity: 0.1; transform: scale(0.6); }}
    50%       {{ opacity: 1;   transform: scale(1.6); }}
  }}
  @keyframes iTextGlitter {{
    0%   {{ background-position: 160% center; }}
    100% {{ background-position: -60% center; }}
  }}
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
  <div id="i-particles"></div>
  <div id="i-wordglitter"></div>
  <div class="i-shimmer-stripe"></div>
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

<script>
(function(){{
  var ipc=document.getElementById('i-particles');
  var driftCols=['rgba(255,210,50,0.95)','rgba(232,184,75,0.92)','rgba(255,235,120,0.88)','rgba(255,200,40,0.85)','rgba(248,220,90,0.80)'];
  for(var i=0;i<26;i++){{
    var p=document.createElement('div');
    var sz=(Math.random()*3+1.5).toFixed(2);
    var glow=parseFloat(sz)*2.5;
    var col=driftCols[Math.floor(Math.random()*driftCols.length)];
    var glowCol=col.replace(/[\d.]+\)$/,'0.6)');
    p.style.cssText=['position:absolute','width:'+sz+'px','height:'+sz+'px','left:'+(Math.random()*90+5).toFixed(1)+'%','top:'+(Math.random()*88+6).toFixed(1)+'%','background:'+col,'border-radius:50%','box-shadow:0 0 '+glow+'px '+glow+'px '+glowCol,'animation:iParticleDrift '+(Math.random()*8+6).toFixed(1)+'s ease-in-out '+(Math.random()*18).toFixed(1)+'s infinite','pointer-events:none'].join(';');
    ipc.appendChild(p);
  }}
  var sparkCols=['rgba(255,220,60,1)','rgba(255,245,160,1)','rgba(232,184,75,1)'];
  for(var j=0;j<12;j++){{
    var s=document.createElement('div');
    var ssz=(Math.random()*2+1.8).toFixed(2);
    var sglow=parseFloat(ssz)*3;
    var scol=sparkCols[Math.floor(Math.random()*sparkCols.length)];
    s.style.cssText=['position:absolute','width:'+ssz+'px','height:'+ssz+'px','left:'+(Math.random()*90+5).toFixed(1)+'%','top:'+(Math.random()*88+6).toFixed(1)+'%','background:'+scol,'border-radius:50%','box-shadow:0 0 '+sglow+'px '+sglow+'px rgba(255,200,50,0.7)','animation:iParticleSparkle '+(Math.random()*3+2).toFixed(1)+'s ease-in-out '+(Math.random()*6).toFixed(1)+'s infinite','pointer-events:none'].join(';');
    ipc.appendChild(s);
  }}
}})();
(function(){{
  var iwg=document.getElementById('i-wordglitter');
  var gc=['rgba(255,215,50,1)','rgba(255,235,120,0.97)','rgba(232,184,75,0.95)','rgba(255,255,160,0.92)','rgba(248,210,60,0.98)'];
  function spawnIFaller(){{
    var p=document.createElement('div');
    var sz=(Math.random()*3.5+1.2).toFixed(1);
    var gl=parseFloat(sz)*2.8;
    var col=gc[Math.floor(Math.random()*gc.length)];
    var sx=(10+Math.random()*80).toFixed(1)+'%';
    var sy=(32+Math.random()*26).toFixed(1)+'%';
    var fall=Math.random()*140+90;
    var drift=(Math.random()-0.5)*80;
    var rot=(Math.random()>0.5?1:-1)*(Math.random()*360+180);
    var dur=Math.random()*2000+2200;
    var radius=Math.random()>0.35?'50%':'30%';
    var aspect=Math.random()>0.35?sz:(parseFloat(sz)*0.55).toFixed(1);
    p.style.cssText=['position:absolute','width:'+sz+'px','height:'+aspect+'px','left:'+sx,'top:'+sy,'background:'+col,'border-radius:'+radius,'box-shadow:0 0 '+gl+'px '+gl+'px rgba(255,200,50,0.65)','pointer-events:none'].join(';');
    iwg.appendChild(p);
    var anim=p.animate([{{transform:'translateY(0px) translateX(0px) rotate(0deg)',opacity:1}},{{transform:'translateY('+fall+'px) translateX('+drift+'px) rotate('+rot+'deg)',opacity:0}}],{{duration:dur,easing:'ease-in',fill:'forwards'}});
    anim.onfinish=function(){{if(iwg.contains(p))iwg.removeChild(p);}};
  }}
  for(var k=0;k<12;k++){{setTimeout(spawnIFaller,1400+k*150);}}
  setInterval(spawnIFaller,500);
}})();
</script>
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
    today_image = IDEKA_IMAGES.get(today, DEFAULT_IDEKA_IMAGE)

    # Build Ideka's page
    ideka_html = build_ideka_html(i_label, i_quote, i_attribution, today, today_image)
    with open(os.path.join(pulse_dir, "index.html"), "w") as f:
        f.write(ideka_html)

    # Build Yemi's dashboard
    yemi_html = build_yemi_html(y_label, y_quote, y_attribution, i_label, i_quote, i_attribution, today, today_image)
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
