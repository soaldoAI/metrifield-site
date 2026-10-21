#!/usr/bin/env python3
"""Builds the static Metrifield site: index, capabilities, technology, about, contact.
Run: python3 build.py  → writes *.html next to this file, plus body.html (artifact preview copy of index)."""
import pathlib, re

ROOT = pathlib.Path(__file__).parent
SITE = "https://www.metrifield.com"
EMAIL = "info@metrifield.com"

LOGO = '''<svg viewBox="0 0 28 28" aria-hidden="true"><rect x="1.5" y="1.5" width="25" height="25" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M6 19.5 L11 10 L15 16 L18 12 L22 19.5" fill="none" stroke="#E59A1C" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/></svg>'''
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'

NAV = [("index.html","Home"),("capabilities.html","Capabilities"),("technology.html","Technology"),("about.html","About"),("contact.html","Contact")]

def head(title, desc, path):
    return f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{'' if path=='index.html' else path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/hero-poster.jpg">
<meta property="og:type" content="website">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@500;600;700&family=Source+Sans+3:wght@400;500;600&display=swap">
<link rel="stylesheet" href="styles.css">
</head>
<body>
'''

def nav(current, solid=False):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==current else ""}>{t}</a>' for h,t in NAV if h!="contact.html")
    return f'''<header class="nav{' nav-solid' if solid else ''}" id="nav">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Metrifield Dynamics home"><img class="logo logo-dark" src="assets/logo.png" alt="Metrifield Dynamics" width="1227" height="410"><img class="logo logo-light" src="assets/logo-white.png" alt="" width="1227" height="410" aria-hidden="true"></a>
    <nav class="nav-links" aria-label="Main">{links}</nav>
    <a class="btn {'btn-dark' if solid else 'btn-light'} nav-cta" href="contact.html">Talk to us</a>
    <button class="nav-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</header>
'''

def cta(h, p, label="Get in touch"):
    return f'''<section class="cta">
  <div class="wrap">
    <div><h2>{h}</h2><p>{p}</p></div>
    <a class="btn btn-accent" href="contact.html">{label} {ARROW}</a>
  </div>
</section>
'''

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="fcol">
      <a class="brand" href="index.html"><img class="logo" src="assets/logo-white.png" alt="Metrifield Dynamics" width="1227" height="410"></a>
      <p style="max-width:34ch">Lifecycle intelligence for utility-scale solar. Sydney, Australia.</p>
    </div>
    <div class="fcol"><b>Site</b><a href="capabilities.html">Capabilities</a><a href="technology.html">Technology</a><a href="about.html">About</a><a href="contact.html">Contact</a></div>
    <div class="fcol"><b>Contact</b><a href="mailto:{EMAIL}">{EMAIL}</a><span>Sydney, NSW</span></div>
    <div class="legal"><span>© 2026 Metrifield Dynamics Pty Ltd</span><span>metrifield.com</span></div>
  </div>
</footer>
<script>
(function(){{
  var n=document.getElementById('nav'),b=n&&n.querySelector('.nav-toggle');
  if(b){{b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)}})}}
  var Z={{
   1:{{name:"Monsoonal north",color:"#D6A75A",regions:"Top End, far-north and tropical Queensland, the Kimberley",exposure:"Sustained heat and humidity, intense UV, a long wet season, cyclonic wind and driving rain.",material:"Encapsulants, backsheets and edge seals with proven resistance to moisture ingress and UV; corrosion-resistant connectors and frames; mounting rated for cyclonic loads.",risk:"Delamination and moisture ingress, corrosion of interconnects and junction boxes, potential-induced degradation in humid conditions, biological growth and storm damage.",cost:"Moisture-driven mechanisms tend to progress once started, so early subsurface detection has high value. Post-wet-season inspection cadence and cyclone recovery dominate O&amp;M planning."}},
   2:{{name:"Arid interior",color:"#C77D52",regions:"Central Australia, Pilbara and Goldfields, outback South Australia, western inland Queensland and New South Wales",exposure:"Extreme daytime heat, large day–night temperature swings, very high irradiance, dust and low humidity; remote sites with long travel distances.",material:"Interconnect and solder designs tolerant of thermal cycling; glass and coatings that resist abrasion and soiling; high-temperature-rated encapsulants and junction boxes.",risk:"Cell cracking and interconnect fatigue from thermal cycling, hot spots, soiling losses, accelerated encapsulant ageing under heat and UV.",cost:"Cleaning economics and travel cost dominate. Targeted diagnostics that avoid unnecessary site visits, and cleaning scheduled on measured recoverable energy, have the largest effect on lifetime cost."}},
   3:{{name:"Subtropical east",color:"#7FA8C9",regions:"South-east and central Queensland coast, New South Wales north coast",exposure:"Warm, humid summers with severe storms and hail, high rainfall, salt load near the coast.",material:"Hail-rated front glass and frames; moisture-resistant encapsulation; corrosion protection within the coastal belt.",risk:"Hail impact and resulting micro-cracks, moisture ingress after storm damage, PID in humid periods, coastal corrosion.",cost:"Event-triggered screening after storms, and distinguishing cosmetic from performance-affecting hail damage, avoid both missed losses and unnecessary replacement."}},
   4:{{name:"Temperate south-east",color:"#5F8F7A",regions:"Sydney, Hunter, Riverina and tablelands, the ACT, Victoria",exposure:"Moderate climate with frost, winter rain, variable irradiance, occasional heat extremes and bushfire smoke.",material:"Mainstream module constructions perform well; attention to frost tolerance, drainage and seasonal soiling from dust, pollen and smoke.",risk:"Gradual degradation rather than acute failure; seasonal soiling; occasional heatwave stress; smoke and ash deposition.",cost:"Lower exposure means intervention value is driven by gradual drift. Condition tracking over repeat inspections separates slow degradation from seasonal effects and times cleaning where it pays."}},
   5:{{name:"Mediterranean south-west",color:"#9C8E6A",regions:"Perth and the south-west of Western Australia, Adelaide and the South Australian coast",exposure:"Hot, dry summers, cool wet winters, persistent coastal salt and strong winds near the coast.",material:"Corrosion-resistant frames, fasteners and connectors; anti-soiling surfaces for the dry season; robust seals against salt-laden moisture.",risk:"Salt corrosion of metallic components, summer soiling, thermal stress during heatwaves.",cost:"Salt accelerates degradation of exposed metals; the value of cleaning is strongly seasonal. Corrosion checks and dry-season cleaning schedules shape lifetime cost."}},
   6:{{name:"Cool temperate Tasmania",color:"#6E7F99",regions:"Tasmania",exposure:"Lower irradiance, frequent moisture, strong winds and cool temperatures; coastal salt on exposed sites.",material:"Wind-load-rated mounting; seals and junction boxes resistant to persistent moisture; designs that tolerate low-light operation.",risk:"Moisture ingress, mechanical stress from wind, biological growth and soiling in damp conditions.",cost:"A lower energy baseline changes intervention economics: the same defect recovers less energy, so prioritisation by net benefit matters more, not less."}}
  }};
  var sel=document.getElementById('zone-select'),panel=document.getElementById('zone-panel');
  function showZone(k){{var z=Z[k]; if(!z||!panel)return; panel.hidden=false;
    document.getElementById('zp-dot').style.background=z.color; document.getElementById('zp-eyebrow').textContent='Zone '+k;
    document.getElementById('zp-title').textContent=z.name; document.getElementById('zp-regions').textContent=z.regions;
    document.getElementById('zp-exposure').innerHTML=z.exposure; document.getElementById('zp-material').innerHTML=z.material;
    document.getElementById('zp-risk').innerHTML=z.risk; document.getElementById('zp-cost').innerHTML=z.cost;
    document.querySelectorAll('.zone-pin').forEach(function(e){{e.classList.toggle('active',e.getAttribute('data-zone')===String(k))}});
    if(sel&&sel.value!==String(k)){{for(var i=0;i<sel.options.length;i++){{if(sel.options[i].value===String(k)){{sel.selectedIndex=i;break}}}}}}
    panel.scrollIntoView({{behavior:'smooth',block:'nearest'}});
  }}
  if(sel){{sel.addEventListener('change',function(){{if(sel.value)showZone(sel.value)}})}}
  document.querySelectorAll('.zone-pin').forEach(function(e){{
    e.addEventListener('click',function(){{showZone(e.getAttribute('data-zone'))}});
    e.addEventListener('keydown',function(ev){{if(ev.key==='Enter'||ev.key===' '){{ev.preventDefault();showZone(e.getAttribute('data-zone'))}}}});
  }});
  var f=document.getElementById('contact-form');
  if(f){{f.addEventListener('submit',function(e){{
    e.preventDefault();
    var d=new FormData(f),s='Enquiry from '+(d.get('name')||'')+' — '+(d.get('org')||'');
    var body='Name: '+d.get('name')+'\\nOrganisation: '+d.get('org')+'\\nEmail: '+d.get('email')+'\\nI am: '+d.get('type')+'\\n\\n'+d.get('msg');
    f.classList.add('sent');
    try{{window.location.href='mailto:{EMAIL}?subject='+encodeURIComponent(s)+'&body='+encodeURIComponent(body)}}catch(err){{}}
  }})}}
}})();
</script>
</body>
</html>
'''

# ---------------------------------------------------------------- pages
index_body = f'''
{nav("index.html")}
<main>
<section class="hero">
  <div class="hero-media">
    <video autoplay muted loop playsinline poster="assets/hero-poster.jpg" aria-hidden="true">
      <source src="assets/hero.mp4" type="video/mp4">
    </video>
  </div>
  <div class="hero-shade"></div>
  <div class="wrap">
    <p class="eyebrow" style="color:var(--accent)">Solar asset intelligence</p>
    <h1>Intelligent inspection. <em>Spatiotemporal twins.</em></h1>
    <p class="lede">Robotic terahertz diagnostics assess subsurface condition. Digital twins track change across sites and time, guiding decisions to lower lifecycle costs.</p>
    <div class="hero-actions">
      <a class="btn btn-accent" href="technology.html">Explore our technology {ARROW}</a>
      <a class="btn btn-outline" href="contact.html">Talk to our team</a>
    </div>
    <div class="hero-foot">
      <span>Drone <b>RGB · thermal</b></span><span>Robot <b>terahertz, on the panel</b></span>
      <span>Scope <b>module → string → plant</b></span>
      <span>Built for <b>Australian conditions</b></span>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="trio">
      <div>
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M3 10h18M9 4v12M15 4v12M8 20h8"/></svg></div>
        <h3 class="h3">Intelligent robotic inspection</h3>
        <p>Drone-mounted edge AI screens RGB and thermal imagery. Targeted terahertz scans assess subsurface material and interface condition.</p>
      </div>
      <div>
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/></svg></div>
        <h3 class="h3">Spatiotemporal digital twins</h3>
        <p>Models link material condition, environmental exposure and generation history, updating with new evidence to track change across sites and time.</p>
      </div>
      <div>
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19h16M6 16l4-5 4 3 4-7"/><circle cx="18" cy="7" r="1.5"/></svg></div>
        <h3 class="h3">Lifecycle decision support</h3>
        <p>Compare interventions by expected net benefit. Use measured outcomes to refine maintenance, material selection and site-specific design.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band-tint" id="how">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How it works</p>
      <h2 class="h2">From inspection to informed action.</h2>
    </div>
    <div class="steps">
      <div class="step-list">
        <div class="step"><span class="n">01</span><div><h3>Intelligent screening</h3><p>Drone-mounted edge AI checks RGB and thermal image quality, maps observations to individual modules and prioritises anomalies for targeted inspection.</p></div></div>
        <div class="step"><span class="n">02</span><div><h3>Targeted THz diagnostics</h3><p>The wheel–rotor platform scans priority modules and healthy controls, using terahertz to assess encapsulation layers and buried interfaces in compatible module structures.</p></div></div>
        <div class="step"><span class="n">03</span><div><h3>Spatiotemporal modelling</h3><p>Inspection, exposure and electrical data update module–string–plant models. ST-Twins track condition across sites and time, identifying where further measurements could improve decisions.</p></div></div>
        <div class="step"><span class="n">04</span><div><h3>Decisions and feedback</h3><p>Owners compare maintenance and replacement options by expected net benefit. Actual costs and generation responses refine the models, improving future recommendations and inspection priorities.</p></div></div>
      </div>
      <figure class="figure">
        <a class="frame" href="assets/architecture.jpg" target="_blank" rel="noopener" aria-label="Open diagram at full size"><img src="assets/architecture.jpg" width="3600" height="2118" alt="System diagram: field sensing feeds a multimodal asset database and dynamic digital twin, which supports decisions for operating plants, new plants and manufacturers; outcomes and costs flow back to update the model." loading="lazy"></a>
        <figcaption>Field sensing → cloud intelligence → decision support, closed by measured outcomes and costs. Click to enlarge.</figcaption>
      </figure>
      <div class="stages">
        <ol>
          <li><span class="n">01</span><b>Screen</b><h3>Aerial screening</h3><p>Scheduled and event-triggered RGB and thermal surveys identify and locate anomalies. Module-level mapping, terrain and environmental data provide spatial context and reveal changes over time.</p></li>
          <li><span class="n">02</span><b>Diagnose</b><h3>Targeted diagnostics</h3><p>Robotic close-range inspections examine selected anomalies alongside healthy reference modules. Where suitable, terahertz sensing adds subsurface evidence beyond conventional optical and thermal imaging.</p></li>
          <li><span class="n">03</span><b>Model</b><h3>Spatiotemporal digital twin</h3><p>Inspection records, environmental exposure, electrical data and maintenance history are connected through asset IDs and timestamps to track degradation, estimate energy losses and quantify uncertainty.</p></li>
          <li><span class="n">04</span><b>Optimise</b><h3>Decision intelligence</h3><p>Cleaning, reinspection, repair, replacement and deferral are evaluated against recoverable energy, cost and risk. Measured intervention outcomes refine future predictions and operating decisions.</p></li>
        </ol>
        <p class="loopline"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/></svg>Verified outcomes continuously refine the system</p>
      </div>
    </div>
  </div>
</section>

<section class="band band-tint" id="regions">
  <div class="wrap">
    <div class="db-top">
    <div class="section-head" style="margin-bottom:0">
      <p class="eyebrow">Regional exposure &amp; module performance</p>
      <h2 class="h2">Where in Australia are your solar assets?</h2>
      <p class="lede">Find your state or geographic region, from the tropical north to the arid interior and temperate south. Explore how local environmental conditions influence material suitability, degradation risks and lifetime costs.</p>
      <label class="zone-pick" for="zone-select">Choose a state or region
        <select id="zone-select">
          <option value="">Select…</option>
          <option value="1">Northern Territory — Top End</option>
          <option value="1">Queensland — far north &amp; tropical coast</option>
          <option value="1">Western Australia — Kimberley</option>
          <option value="2">Northern Territory — Central Australia</option>
          <option value="2">Western Australia — Pilbara &amp; Goldfields</option>
          <option value="2">South Australia — outback &amp; mid-north</option>
          <option value="2">Queensland &amp; NSW — western inland</option>
          <option value="3">Queensland — south-east &amp; central coast</option>
          <option value="3">New South Wales — north coast</option>
          <option value="4">New South Wales — Sydney, Hunter, Riverina &amp; tablelands</option>
          <option value="4">Australian Capital Territory</option>
          <option value="4">Victoria</option>
          <option value="5">South Australia — Adelaide &amp; coastal south</option>
          <option value="5">Western Australia — Perth &amp; south-west</option>
          <option value="6">Tasmania</option>
        </select>
      </label>
    </div>
    <div class="mapwrap">
      <svg class="aumap" viewBox="0 0 540 470" role="img" aria-labelledby="aumap-title"><title id="aumap-title">Map of Australia marking six climate zones used to stratify sites</title><path d="M374.7 28.6 L387.4 69.4 L407.2 81.8 L415.3 122.5 L424.7 134.9 L452.6 157.1 L468.8 185.5 L495.6 209.0 L497.9 236.2 L503.7 249.8 L495.6 284.4 L482.8 302.9 L475.8 315.2 L472.3 321.4 L463.0 341.2 L461.9 354.8 L450.2 363.4 L432.8 365.9 L420.0 379.5 L408.4 372.1 L402.6 369.6 L386.3 377.0 L364.2 369.6 L354.9 365.9 L342.1 353.5 L334.0 336.2 L328.1 327.6 L318.8 330.1 L310.7 316.5 L297.9 325.1 L278.1 302.9 L272.3 293.0 L240.9 285.6 L216.5 288.1 L182.8 295.5 L158.4 311.5 L135.1 315.2 L107.2 321.4 L88.6 328.8 L56.0 321.4 L54.9 304.1 L64.2 291.8 L61.9 273.2 L50.2 252.2 L36.3 218.9 L38.6 199.1 L44.4 167.0 L61.9 155.9 L75.8 152.2 L96.7 147.2 L122.3 138.6 L138.6 118.8 L154.9 110.2 L157.2 96.6 L171.2 87.9 L188.6 69.4 L207.2 81.8 L224.7 80.5 L232.8 58.3 L238.6 49.6 L252.6 37.3 L259.5 34.8 L279.3 44.7 L297.9 44.7 L309.5 48.4 L296.7 64.5 L299.1 79.3 L310.7 92.9 L337.4 112.6 L354.9 111.4 L363.0 81.8 L365.3 50.9 L374.7 28.6 Z" fill="var(--map-fill)" stroke="var(--map-line)" stroke-width="1.5" stroke-linejoin="round"/><path d="M400.2 399.2 L418.8 404.2 L442.1 401.7 L440.9 421.5 L437.4 430.1 L427.0 435.1 L415.3 432.6 L407.2 419.0 L400.2 405.4 L400.2 399.2 Z" fill="var(--map-fill)" stroke="var(--map-line)" stroke-width="1.5" stroke-linejoin="round"/><circle cx="238.6" cy="49.6" r="26" fill="#D6A75A" opacity=".22"/><g class="zone-pin" data-zone="1" role="button" tabindex="0" aria-label="Zone 1"><circle cx="238.6" cy="49.6" r="13" fill="#D6A75A"/><text x="238.6" y="54.1" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">1</text></g><circle cx="274.7" cy="189.2" r="26" fill="#C77D52" opacity=".22"/><g class="zone-pin" data-zone="2" role="button" tabindex="0" aria-label="Zone 2"><circle cx="274.7" cy="189.2" r="13" fill="#C77D52"/><text x="274.7" y="193.7" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">2</text></g><circle cx="485.1" cy="223.8" r="26" fill="#7FA8C9" opacity=".22"/><g class="zone-pin" data-zone="3" role="button" tabindex="0" aria-label="Zone 3"><circle cx="485.1" cy="223.8" r="13" fill="#7FA8C9"/><text x="485.1" y="228.3" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">3</text></g><circle cx="432.8" cy="347.4" r="26" fill="#5F8F7A" opacity=".22"/><g class="zone-pin" data-zone="4" role="button" tabindex="0" aria-label="Zone 4"><circle cx="432.8" cy="347.4" r="13" fill="#5F8F7A"/><text x="432.8" y="351.9" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">4</text></g><circle cx="72.3" cy="297.9" r="26" fill="#9C8E6A" opacity=".22"/><g class="zone-pin" data-zone="5" role="button" tabindex="0" aria-label="Zone 5"><circle cx="72.3" cy="297.9" r="13" fill="#9C8E6A"/><text x="72.3" y="302.4" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">5</text></g><circle cx="424.7" cy="415.3" r="26" fill="#6E7F99" opacity=".22"/><g class="zone-pin" data-zone="6" role="button" tabindex="0" aria-label="Zone 6"><circle cx="424.7" cy="415.3" r="13" fill="#6E7F99"/><text x="424.7" y="419.8" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">6</text></g></svg>
      <ol class="zones"><li class="zone-pin" data-zone="1" role="button" tabindex="0"><span class="dot" style="background:#D6A75A">1</span><div><b>Monsoonal north</b><span>Heat, humidity, UV, cyclones</span></div></li><li class="zone-pin" data-zone="2" role="button" tabindex="0"><span class="dot" style="background:#C77D52">2</span><div><b>Arid interior</b><span>Extreme heat, dust, thermal cycling</span></div></li><li class="zone-pin" data-zone="3" role="button" tabindex="0"><span class="dot" style="background:#7FA8C9">3</span><div><b>Subtropical east</b><span>Humidity, hail, storms</span></div></li><li class="zone-pin" data-zone="4" role="button" tabindex="0"><span class="dot" style="background:#5F8F7A">4</span><div><b>Temperate south-east</b><span>Frost, rain, moderate UV</span></div></li><li class="zone-pin" data-zone="5" role="button" tabindex="0"><span class="dot" style="background:#9C8E6A">5</span><div><b>Mediterranean south-west</b><span>Salt, dry heat, winter rain</span></div></li><li class="zone-pin" data-zone="6" role="button" tabindex="0"><span class="dot" style="background:#6E7F99">6</span><div><b>Cool temperate Tasmania</b><span>Wind, moisture, low irradiance</span></div></li></ol>
    </div>
    </div>
    <div class="zone-panel" id="zone-panel" hidden>
      <div class="zp-head"><span class="dot" id="zp-dot"></span><div><p class="eyebrow" id="zp-eyebrow">Zone</p><h3 id="zp-title"></h3><p id="zp-regions" class="zp-regions"></p></div></div>
      <div class="zp-grid">
        <div><b>Environmental exposure</b><p id="zp-exposure"></p></div>
        <div><b>Material suitability</b><p id="zp-material"></p></div>
        <div><b>Degradation risks</b><p id="zp-risk"></p></div>
        <div><b>Lifetime cost drivers</b><p id="zp-cost"></p></div>
      </div>
      <p class="zp-note">Indicative guidance by climate zone. Site-specific assessment uses local exposure data and the plant's own inspection and performance records.</p>
    </div>
  </div>
</section>

<section class="band" id="who">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Capabilities</p>
      <h2 class="h2">What we do, at each stage of a solar asset's life</h2>
    </div>
    <div class="cards">
      <a class="card" href="capabilities.html#operators">
        <p class="who">Asset owners &amp; O&amp;M</p>
        <h3>Operating plants</h3>
        <p>Schedule cleaning, repairs and replacements on what they recover, and stop paying for low-value work.</p>
        <span class="more">See how {ARROW}</span>
      </a>
      <a class="card" href="capabilities.html#developers">
        <p class="who">Developers &amp; EPCs</p>
        <h3>Deploying plants</h3>
        <p>Rank layout, tilt, row spacing, mounting height and module choice by whole-of-life cost, not just first-year yield.</p>
        <span class="more">See how {ARROW}</span>
      </a>
      <a class="card" href="capabilities.html#manufacturers">
        <p class="who">Module manufacturers</p>
        <h3>Manufacturing plants</h3>
        <p>Trace field failure modes back to bills of materials, supplier batches and lamination windows before warranty costs arrive.</p>
        <span class="more">See how {ARROW}</span>
      </a>
    </div>
  </div>
</section>

<section class="band band-dark">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Outcomes</p>
      <h2 class="h2">Lower lifecycle cost. More delivered energy. Longer useful life.</h2>
    </div>
    <div class="outcomes">
      <div><h3>Targeted inspections</h3><p>Fleet-wide screening directs detailed diagnostics where they matter most.</p></div>
      <div><h3>Value-driven maintenance</h3><p>Prioritise interventions by recoverable energy, cost and risk.</p></div>
      <div><h3>Evidence-led prevention</h3><p>Trace degradation and intervention outcomes to inform future design and maintenance.</p></div>
    </div>
  </div>
</section>

<section class="band band-tint">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">About Metrifield</p>
      <h2 class="h2">Solar asset intelligence, grounded in engineering.</h2>
      <p class="lede">Founded in Sydney by Harrison Su, Sohan Domingo and Laurens Willems van Beveren, Metrifield Dynamics brings together expertise in materials science, field inspection and edge AI to connect multiscale diagnostics with energy performance and lifecycle economics. <a href="about.html">Meet the team</a>.</p>
    </div>
  </div>
</section>

</main>
'''

capabilities_body = f'''
{nav("capabilities.html", solid=True)}
<main>
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Capabilities</p>
    <h1>Reduce today's losses. Prevent tomorrow's.</h1>
    <p class="lede">What we do for solar assets at each stage of their life: plants already operating, plants being designed and built, and the factories that make the modules. Not every anomaly warrants intervention. We assess the cost of inaction, prioritise by expected net benefit, and verify the outcomes, turning measured results into better decisions and fewer recurring losses.</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sol" id="operators">
      <div class="sol-text">
        <p class="eyebrow">01 / Operating plants</p>
        <h2 class="h2">Recover energy. Avoid unnecessary work.</h2>
        <p>A detected anomaly is not automatically a work order. We combine existing plant data with scalable screening, escalating to detailed diagnostics only when further evidence could change a decision. Interventions are ranked by expected energy recovery, cost and risk, then evaluated against measured outcomes.</p>
        <ul>
          <li>Distinguish actionable losses from environmental and operational effects.</li>
          <li>Match diagnostic effort to the value of the decision.</li>
          <li>Verify recovery and use the results to refine future priorities.</li>
        </ul>
        <p class="decides"><b>Decisions supported</b>Clean · Reinspect · Repair · Replace · Defer</p>
      </div>
      <div class="sol-media"><img src="assets/drone.jpg" alt="Inspection drone flying over rows of solar modules" loading="lazy"></div>
    </div>

    <div class="sol" id="developers">
      <div class="sol-text">
        <p class="eyebrow">02 / Deploying plants</p>
        <h2 class="h2">Avoid costs before they are built in.</h2>
        <p>Losses observed in operating plants reveal risks that conventional yield models may overlook. We translate comparable field evidence into site-specific design scenarios, evaluating material suitability, configuration and maintainability against lifetime energy and cost. Key assumptions remain traceable for validation once the plant is operational.</p>
        <ul>
          <li>Identify degradation risks under local environmental conditions.</li>
          <li>Compare design alternatives by lifetime value, not upfront cost alone.</li>
          <li>Carry design assumptions into commissioning and performance monitoring.</li>
        </ul>
        <p class="decides"><b>Decisions supported</b>Module selection · Layout · Mounting · Maintenance access</p>
      </div>
      <div class="sol-media"><img src="assets/aerial.jpg" alt="Aerial view of a solar farm layout" loading="lazy"></div>
    </div>

    <div class="sol" id="manufacturers">
      <div class="sol-text">
        <p class="eyebrow">03 / Manufacturing plants</p>
        <h2 class="h2">Prevent recurring failures at the source.</h2>
        <p>Recurring field failures can reveal opportunities to improve materials and production. By comparing performance across matched environments and batches, we investigate potential links to material selection and process conditions. Targeted validation then supports changes that can reduce future defects, rework and warranty exposure.</p>
        <ul>
          <li>Separate environmental effects from material and batch variation.</li>
          <li>Focus testing on suspected causes with the greatest economic impact.</li>
          <li>Validate corrective measures before wider production changes.</li>
        </ul>
        <p class="decides"><b>Decisions supported</b>Material specifications · Process optimisation · Batch QA · Product design</p>
      </div>
      <div class="sol-media"><img src="assets/factory.jpg" alt="Solar module lamination line" loading="lazy"></div>
    </div>
  </div>
</section>

</main>
'''

technology_body = f'''
{nav("technology.html", solid=True)}
<main>
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Technology</p>
    <h1>Grounded in physics. Accountable to evidence.</h1>
    <p class="lede">Our hybrid digital twin combines physical modelling with real-world observations to track how assets evolve across space and time. It quantifies performance impacts, evaluates intervention scenarios and tests predictions against measured outcomes.</p>
  </div>
</section>

<section class="band band-tint">
  <div class="wrap">
    <div class="db-top">
    <div class="section-head" style="margin-bottom:0">
      <p class="eyebrow">The evidence chain</p>
      <h2 class="h2">From material origins to measured outcomes.</h2>
      <p class="lede">A continuous evidence chain connects physical conditions, asset performance and verified results, keeping predictions traceable, testable and open to refinement.</p>
    </div>
    <div class="chainwrap"><svg class="chainloop" viewBox="-110 0 820 600" role="img" aria-label="The evidence chain as a loop: material and process context, environmental exposure, condition evolution, performance impact, outcome validation, feeding back to the start">
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>
  <path d="M333.5 92.7 A210 210 0 0 1 486.8 204.1" class="arc" marker-end="url(#arrow)"/><path d="M507.5 267.8 A210 210 0 0 1 448.9 448.1" class="arc" marker-end="url(#arrow)"/><path d="M394.8 487.4 A210 210 0 0 1 205.2 487.4" class="arc" marker-end="url(#arrow)"/><path d="M151.1 448.1 A210 210 0 0 1 92.5 267.8" class="arc" marker-end="url(#arrow)"/><path d="M113.2 204.1 A210 210 0 0 1 266.5 92.7" class="arc arc-back" marker-end="url(#arrow)"/>
  <g class="node"><circle cx="300.0" cy="90.0" r="26"/><text x="300.0" y="96.0" text-anchor="middle" class="num">01</text><text x="300.0" y="26.0" text-anchor="middle" class="lbl">Material &amp; process context</text></g><g class="node"><circle cx="499.7" cy="235.1" r="26"/><text x="499.7" y="241.1" text-anchor="middle" class="num">02</text><text x="554.9" y="211.2" text-anchor="start" class="lbl">Environmental exposure</text></g><g class="node"><circle cx="423.4" cy="469.9" r="26"/><text x="423.4" y="475.9" text-anchor="middle" class="num">03</text><text x="457.5" y="532.8" text-anchor="start" class="lbl">Condition evolution</text></g><g class="node"><circle cx="176.6" cy="469.9" r="26"/><text x="176.6" y="475.9" text-anchor="middle" class="num">04</text><text x="142.5" y="532.8" text-anchor="end" class="lbl">Performance impact</text></g><g class="node"><circle cx="100.3" cy="235.1" r="26"/><text x="100.3" y="241.1" text-anchor="middle" class="num">05</text><text x="45.1" y="211.2" text-anchor="end" class="lbl">Outcome validation</text></g>
  <text x="300" y="290" text-anchor="middle" class="centre">Validated outcomes</text>
  <text x="300" y="316" text-anchor="middle" class="centre2">inform future maintenance,</text>
  <text x="300" y="338" text-anchor="middle" class="centre2">design and manufacturing</text>
</svg></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Sensing</p>
      <h2 class="h2">From surface anomalies to material evidence.</h2>
      <p class="lede">RGB and thermal surveys locate suspected problems across the array. Targeted robotic terahertz measurements investigate subsurface material and interface conditions that conventional imaging cannot directly assess.</p>
    </div>
    <div class="duo">
      <figure><img src="assets/drone.jpg" alt="Inspection drone with RGB and thermal camera over a solar array" loading="lazy"><figcaption>01 — Aerial RGB and thermal screening identifies suspect modules.</figcaption></figure>
      <figure><img src="assets/crawler.jpg" alt="Crawler robot on a solar module carrying a terahertz scanner" loading="lazy"><figcaption>02 — Robotic terahertz sensing investigates selected subsurface conditions.</figcaption></figure>
    </div>
    <div class="grid2">
      <div><h3>Aerial RGB &amp; thermal screening</h3><p>RGB identifies soiling, shading and visible damage; thermal imaging reveals abnormal heating. Together, they rapidly locate suspect modules and focus detailed inspection where it is most valuable.</p></div>
      <div><h3>Robotic terahertz diagnostics</h3><p>Terahertz sensing probes accessible dielectric layers and interfaces, revealing contrasts associated with moisture, material changes and concealed structural irregularities. It adds subsurface evidence beyond optical appearance and surface temperature.</p></div>
      <div><h3>Environmental context</h3><p>Irradiance, temperature, wind and shading provide the context needed to distinguish environmental effects from persistent anomalies, reducing false alarms and unnecessary inspections.</p></div>
      <div><h3>Condition tracking</h3><p>Repeated observations and operating data reveal whether anomalies are temporary, persistent or progressing. Follow-up inspections are prioritised by changes in condition and their potential impact.</p></div>
    </div>
  </div>
</section>

<section class="band band-tint" id="database">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The climate and condition database</p>
      <h2 class="h2">Where every module is, what it is made of, and how it is behaving</h2>
      <p class="lede">Each module is linked to the place it lives. Over time the database becomes a map of how solar hardware ages across Australia's climate zones, and a guide to what to build where. <a href="index.html#regions">Explore the regional map</a>.</p>
    </div>
    <div class="grid2">
      <div><h3>Each module, as a record</h3><p>Manufacturer, model, bill of materials, factory batch and lamination record, install date, string position and mounting. Then every drone image, thermal frame, terahertz scan, work order and replacement, with timestamps.</p></div>
      <div><h3>Linked to its environment</h3><p>Climate zone, long-term weather history, terrain and shading, distance from the coast, salt and dust load, vegetation and fire exposure, plus on-site irradiance, temperature, humidity and wind, down to the microclimate inside the array.</p></div>
      <div><h3>Linked to its performance</h3><p>SCADA and string-level electrical data, weather-normalised, so condition changes can be tied to energy loss at the metering resolution available.</p></div>
      <div><h3>Six climate zones as the proving ground</h3><p>From the monsoonal north to temperate Tasmania, each zone has its own dominant degradation mechanisms. Sites are stratified across them so the same materials can be compared under different exposure.</p></div>
      <div><h3>From database to degradation map</h3><p>Repeat inspections of the same modules, season after season, turn individual findings into degradation rates by material, batch and zone, then into a fleet-wide risk ranking.</p></div>
      <div><h3>From map to deployment guidance</h3><p>Invert the model: given a site's terrain, climate and a proposed module construction, estimate degradation, maintenance cost and premature replacement risk before a single post goes in.</p></div>
    </div>
  </div>
</section>

<section class="band band-dark" id="how-we-work">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How we work</p>
      <h2 class="h2">From site assessment to verified decisions.</h2>
      <p class="lede">A phased approach that begins with broad-area screening and progresses to targeted diagnostics, physics-informed modelling and economic optimisation. Each step adds evidence where it can improve the next decision.</p>
    </div>
    <div class="grid2">
      <div><h3>01 — Screen &amp; establish the baseline</h3><p>Drone RGB and thermal surveys identify and locate anomalies across the array. Existing SCADA, asset and maintenance records establish operating baselines and guide inspection priorities.</p></div>
      <div><h3>02 — Characterise &amp; diagnose</h3><p>Site-specific heat, irradiance, moisture, shading and environmental exposure provide context for observed anomalies. Targeted robotic terahertz scans investigate selected modules and reference samples, adding subsurface material evidence where it can inform decisions.</p></div>
      <div><h3>03 — Model &amp; optimise</h3><p>Multimodal observations feed a physics-informed, multiphysics digital twin linking environmental exposure, material condition and energy performance. Intervention scenarios are evaluated against expected energy recovery, lifecycle cost, risk and uncertainty.</p></div>
      <div><h3>04 — Decide, verify &amp; improve</h3><p>Prioritise cleaning, reinspection, repair, replacement or deferral based on expected net value. Compare actual costs and measured outcomes with predictions to refine future maintenance, plant design and manufacturing decisions.</p></div>
    </div>
    <ul class="qstrip">
      <li><svg viewBox="0 0 24 24"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5"/></svg><b>Screen</b><span>Where?</span></li>
      <li><svg viewBox="0 0 24 24"><circle cx="12" cy="13" r="4"/><path d="M12 3v2M4.9 6.9l1.4 1.4M3 13h2M19 13h2M17.7 8.3l1.4-1.4M7 20h10"/></svg><b>Characterise</b><span>Under what conditions?</span></li>
      <li><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/><circle cx="8" cy="7" r="1.5"/><circle cx="16" cy="12" r="1.5"/><circle cx="10" cy="17" r="1.5"/></svg><b>Diagnose</b><span>What is happening?</span></li>
      <li><svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="M12 7v5M12 12l-6 5M12 12l6 5"/></svg><b>Model</b><span>What is the impact?</span></li>
      <li><svg viewBox="0 0 24 24"><path d="M12 3v18M4 7h16M6 7l-3 7h6zM18 7l-3 7h6z"/></svg><b>Decide</b><span>What is worth doing?</span></li>
      <li><svg viewBox="0 0 24 24"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/></svg><b>Verify</b><span>Did it deliver?</span></li>
    </ul>
    <p class="pathway-line"><span class="eyebrow">Engagement pathway</span><b>Focused pilot</b><i>→</i><b>Validated value</b><i>→</i><b>Scaled deployment</b></p>
  </div>
</section>

</main>
'''

about_body = f'''
{nav("about.html", solid=True)}
<main>
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>Solar asset intelligence, grounded in engineering.</h1>
    <p class="lede">Founded in Sydney by Harrison Su, Sohan Domingo and Laurens Willems van Beveren, Metrifield Dynamics brings together expertise in materials science, field inspection and edge AI to connect multiscale diagnostics with energy performance and lifecycle economics.</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Founders</p>
      <h2 class="h2">The team</h2>
    </div>
    <div class="people">
      <div class="person">
        <div class="photo"><img src="assets/harrison.jpg" alt="Harrison Su" width="800" height="1000" loading="lazy"></div>
        <h3>Harrison Su</h3>
        <p class="role">Co-founder</p>
        <p>PhD in Materials Science and Engineering, and Director of Caelvox Technologies, developing advanced sensing architecture and automated inspection systems. His research spans energy materials, terahertz imaging and advanced characterisation, including collaborations with the Australian Synchrotron and the Australian Centre for Neutron Scattering. Focused on translating materials science into validated diagnostics, industrial applications and asset intelligence.</p>
      </div>
      <div class="person">
        <div class="photo"><img src="assets/laurens.jpg" alt="Laurens Willems van Beveren" width="800" height="1000" loading="lazy"></div>
        <h3>Laurens Willems van Beveren</h3>
        <p class="role">Co-founder</p>
        <p>PhD in Applied Physics and Director of Australian Vacuum Services and Australian Drone Surveys. Former Experimental Scientist at Australia's National Measurement Institute, with extensive experience in precision instrumentation, measurement science and systems engineering. Combines scientific instrumentation expertise with CASA-credentialed drone operations, supporting reliable sensor integration, field inspection and engineering deployment.</p>
      </div>
      <div class="person">
        <div class="photo"><img src="assets/sohan.jpg" alt="Sohan Domingo" width="800" height="1000" loading="lazy"></div>
        <h3>Sohan Domingo</h3>
        <p class="role">Co-founder</p>
        <p>Master of Software Engineering, and Founder of Edgegenix, a Sydney venture studio building computer vision and edge inference systems for councils, utilities, fire agencies and insurers, and of BrightBuddy, bringing companion robots to Australian aged care. Long-standing focus on LiDAR, computer vision and geospatial systems for infrastructure, with hands-on experience across aerial data systems and edge AI deployment.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band-tint">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How we work</p>
      <h2 class="h2">Decisions first, then measurements</h2>
    </div>
    <div class="grid2">
      <div><h3>Start where the money is</h3><p>Engagements begin with cleaning schedules and targeted repair and replacement decisions on operating plants, then extend to manufacturing feedback and new-plant design.</p></div>
      <div><h3>Measure what we claim</h3><p>Value is benchmarked against existing workflows on total expenditure per MW, delivered MWh and net lifecycle cost improvement, including deployment, inspection, computing and model-maintenance costs.</p></div>
      <div><h3>Share models, keep calibration local</h3><p>Model structures and statistical priors are shared across sites; calibration, service costs and site constraints stay local.</p></div>
      <div><h3>Built with Edgegenix</h3><p>Edgegenix contributes the edge AI: training the detection models and deploying them on the field platform.</p></div>
    </div>
  </div>
</section>

</main>
'''

contact_body = f'''
{nav("contact.html", solid=True)}
<main>
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Talk to us</h1>
    <p class="lede">Tell us about your plant, your project or your product and we will come back to you within two business days.</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="contact-grid">
      <div class="contact-info">
        <div class="row"><p class="k">Email</p><p class="v"><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
        <div class="row"><p class="k">Location</p><p class="v">Sydney, NSW, Australia</p></div>
        <div class="row">
          <p class="k">We want to hear from</p>
          <ul>
            <li>Solar asset owners and O&amp;M providers</li>
            <li>Developers and EPCs planning new plants</li>
            <li>Module manufacturers</li>
            <li>Research partners and engineers</li>
          </ul>
        </div>
      </div>
      <form class="form" id="contact-form" novalidate>
        <div class="two">
          <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-org">Organisation</label><input id="f-org" name="org" type="text" autocomplete="organization"></div>
        </div>
        <div class="two">
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="f-type">I am a</label>
            <select id="f-type" name="type">
              <option>Solar asset owner / O&amp;M</option>
              <option>Developer / EPC</option>
              <option>Module manufacturer</option>
              <option>Researcher / partner</option>
              <option>Other</option>
            </select>
          </div>
        </div>
        <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="msg" required></textarea></div>
        <p class="ok">Thanks. Your email app should open with the message ready to send; if it doesn't, email us directly at {EMAIL}.</p>
        <div><button class="btn btn-dark" type="submit">Send message {ARROW}</button></div>
        <p class="note">No mailing lists. We only use your details to reply.</p>
      </form>
    </div>
  </div>
</section>
</main>
'''

PAGES = {
  "index.html": ("Metrifield Dynamics — Solar asset intelligence", "Intelligent robotic inspection and spatiotemporal digital twins: robotic terahertz diagnostics assess subsurface condition, and twins track change across sites and time to lower lifecycle costs.", index_body),
  "capabilities.html": ("Capabilities — Metrifield Dynamics", "What Metrifield Dynamics does for operating plants, plants being deployed, and module manufacturers.", capabilities_body),
  "technology.html": ("Technology — Metrifield Dynamics", "Tiered RGB, thermal and terahertz sensing, a multimodal asset record and a hybrid physics-and-data digital twin that predicts the most economical action.", technology_body),
  "about.html": ("About — Metrifield Dynamics", "Founded in Sydney by Harrison Su, Sohan Domingo and Laurens Willems van Beveren: materials science, field inspection and edge AI for solar asset intelligence.", about_body),
  "contact.html": ("Contact — Metrifield Dynamics", "Get in touch with Metrifield about pilot sites, data partnerships and collaboration.", contact_body),
}

for path,(title,desc,body) in PAGES.items():
    (ROOT/path).write_text(head(title,desc,path)+body+FOOTER, encoding="utf-8")

# Artifact preview copy of index: no doctype/html/head/body wrapper; keep title + links.
idx = (ROOT/"index.html").read_text(encoding="utf-8")
m = re.search(r"<head>(.*?)</head>\s*<body>\s*(.*)</body>\s*</html>\s*$", idx, re.S)
headinner, bodyinner = m.group(1), m.group(2)
keep = "\n".join(l for l in headinner.splitlines() if l.startswith(("<title>", '<link rel="stylesheet"', '<link rel="preconnect"')))
(ROOT/"body.html").write_text(f"{keep}\n<meta name=\"claude:viewport-fit-sides\" content=\"cover\">\n<style>body{{margin:0}}</style>\n{bodyinner}", encoding="utf-8")
(ROOT/"_redirects").write_text("https://metrifield.com/* https://www.metrifield.com/:splat 301\n/solutions.html /capabilities.html 301\n/solutions /capabilities.html 301\n")
print("built", ", ".join(PAGES))
