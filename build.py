#!/usr/bin/env python3
"""Builds the static Metrifield site: index, solutions, technology, about, contact.
Run: python3 build.py  → writes *.html next to this file, plus body.html (artifact preview copy of index)."""
import pathlib, re

ROOT = pathlib.Path(__file__).parent
SITE = "https://www.metrifield.com"
EMAIL = "info@metrifield.com"

LOGO = '''<svg viewBox="0 0 28 28" aria-hidden="true"><rect x="1.5" y="1.5" width="25" height="25" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M6 19.5 L11 10 L15 16 L18 12 L22 19.5" fill="none" stroke="#E59A1C" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/></svg>'''
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'

NAV = [("index.html","Home"),("solutions.html","Solutions"),("technology.html","Technology"),("about.html","About"),("contact.html","Contact")]

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

def cta(h, p):
    return f'''<section class="cta">
  <div class="wrap">
    <div><h2>{h}</h2><p>{p}</p></div>
    <a class="btn btn-accent" href="contact.html">Get in touch {ARROW}</a>
  </div>
</section>
'''

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="fcol">
      <a class="brand" href="index.html"><img class="logo" src="assets/logo-white.png" alt="Metrifield Dynamics" width="1227" height="410"></a>
      <p style="max-width:34ch">Lifecycle intelligence for utility-scale solar. Sydney, Australia.</p>
    </div>
    <div class="fcol"><b>Site</b><a href="solutions.html">Solutions</a><a href="technology.html">Technology</a><a href="about.html">About</a><a href="contact.html">Contact</a></div>
    <div class="fcol"><b>Contact</b><a href="mailto:{EMAIL}">{EMAIL}</a><span>Sydney, NSW</span></div>
    <div class="legal"><span>© 2026 Metrifield Dynamics Pty Ltd</span><span>metrifield.com</span></div>
  </div>
</footer>
<script>
(function(){{
  var n=document.getElementById('nav'),b=n&&n.querySelector('.nav-toggle');
  if(b){{b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)}})}}
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
    <p class="eyebrow" style="color:var(--accent)">Metrifield Dynamics</p>
    <h1>Find the defect from the air. <em>Diagnose it</em> on the panel.</h1>
    <p class="lede">Drones screen the array with RGB and thermal imaging. A robot then goes onto the flagged modules with a terahertz scanner to see what is happening inside the glass. Metrifield links every result to the module's materials, exposure and energy performance, so each repair, replacement and design decision is made on lifecycle cost.</p>
    <div class="hero-actions">
      <a class="btn btn-accent" href="solutions.html">Explore solutions {ARROW}</a>
      <a class="btn btn-outline" href="technology.html">How it works</a>
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
        <h3 class="h3">A climate and condition database</h3>
        <p>Every module recorded with its materials and batch, linked to where it sits: climate zone, terrain, coast, dust and fire exposure, plus every inspection and its energy performance. Over time, a map of how solar ages across Australia.</p>
      </div>
      <div>
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/></svg></div>
        <h3 class="h3">Drone finds it, robot confirms it</h3>
        <p>Drone RGB and thermal screening flags suspect modules. A panel-crawling robot then scans them with terahertz to confirm what is happening inside the encapsulation.</p>
      </div>
      <div>
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19h16M6 16l4-5 4 3 4-7"/><circle cx="18" cy="7" r="1.5"/></svg></div>
        <h3 class="h3">Every action ranked by net benefit</h3>
        <p>Clean, repair, replace or defer: the digital twin predicts recoverable energy, failure risk and cost for each option before a work order is raised, then learns from the outcome.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band-tint" id="how">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How it works</p>
      <h2 class="h2">From field observation to a decision with the cost comparison attached</h2>
    </div>
    <div class="steps">
      <div class="step-list">
        <div class="step"><span class="n">01</span><div><h3>Drone screening</h3><p>Drones fly scheduled and event-triggered RGB and thermal surveys over the array. Edge AI checks image quality, locates each module and grades anomalies on site. Terrain, shading, climate and on-site exposure data separate regional conditions from microclimates inside the array.</p></div></div>
        <div class="step"><span class="n">02</span><div><h3>Robot terahertz diagnosis</h3><p>A robot moves onto the flagged modules, and onto representative healthy ones, and scans them at close range with terahertz. This gives evidence of material layers and interface condition inside the encapsulation that surface imagery and thermal cannot show.</p></div></div>
        <div class="step"><span class="n">03</span><div><h3>Cloud intelligence</h3><p>Inspections, healthy controls, SCADA and electrical data, work orders and actual expenditure are linked through module IDs, locations, timestamps and manufacturing batches, then coupled with yield, thermal, degradation and cost models to form module, string and plant digital twins.</p></div></div>
        <div class="step"><span class="n">04</span><div><h3>Decision support and feedback</h3><p>Cleaning, reinspection, repair and replacement are prioritised by recoverable energy, expected loss and intervention cost. Each action's cost, condition change and generation response feeds back into the models.</p></div></div>
      </div>
      <figure class="figure">
        <a class="frame" href="assets/architecture.jpg" target="_blank" rel="noopener" aria-label="Open diagram at full size"><img src="assets/architecture.jpg" width="3600" height="2118" alt="System diagram: field sensing feeds a multimodal asset database and dynamic digital twin, which supports decisions for operating plants, new plants and manufacturers; outcomes and costs flow back to update the model." loading="lazy"></a>
        <figcaption>Field sensing → cloud intelligence → decision support, closed by measured outcomes and costs. Click to enlarge.</figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="photo-band">
  <img src="assets/crawler.jpg" alt="" loading="lazy">
  <div class="wrap">
    <p class="eyebrow" style="color:var(--accent)">Why it matters</p>
    <blockquote>Modules from the same factory can look identical on day one and age very differently in the field. The difference is traceable, if the data is connected.</blockquote>
  </div>
</section>

<section class="band" id="who">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Who we work with</p>
      <h2 class="h2">Three decision-makers, one condition and degradation database</h2>
    </div>
    <div class="cards">
      <a class="card" href="solutions.html#operators">
        <p class="who">Asset owners &amp; O&amp;M</p>
        <h3>Operating plants</h3>
        <p>Schedule cleaning, repairs and replacements on what they recover, and stop paying for low-value work.</p>
        <span class="more">Learn more {ARROW}</span>
      </a>
      <a class="card" href="solutions.html#developers">
        <p class="who">Developers &amp; EPCs</p>
        <h3>Planned plants</h3>
        <p>Rank layout, tilt, row spacing, mounting height and module choice by whole-of-life cost, not just first-year yield.</p>
        <span class="more">Learn more {ARROW}</span>
      </a>
      <a class="card" href="solutions.html#manufacturers">
        <p class="who">Module manufacturers</p>
        <h3>Factory feedback</h3>
        <p>Trace field failure modes back to bills of materials, supplier batches and lamination windows before warranty costs arrive.</p>
        <span class="more">Learn more {ARROW}</span>
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
      <div><h3>Fewer site visits</h3><p>Tiered screening and on-demand terahertz inspection cut repeat visits and specialist labour.</p></div>
      <div><h3>Less wasted work</h3><p>Work orders prioritised by economic value reduce low-value cleaning, unnecessary replacements and fault-related downtime.</p></div>
      <div><h3>Fewer surprises</h3><p>Connected records from factory release to operation remove duplicate data collection and make defect responsibility clear.</p></div>
    </div>
  </div>
</section>

<section class="band band-tint">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">About Metrifield</p>
      <h2 class="h2">Founded in Sydney by engineers who have built field sensing and edge AI for infrastructure</h2>
      <p class="lede">Metrifield Dynamics was founded by Harrison, Sohan Domingo and Lauren to bring materials-level diagnostics and lifecycle economics together for solar. <a href="about.html">Meet the team</a>.</p>
    </div>
  </div>
</section>

{cta("Running, building or manufacturing for solar in Australia?", "We are looking for asset owners, O&amp;M providers, developers and module manufacturers to work with as early sites and data partners.")}
</main>
'''

solutions_body = f'''
{nav("solutions.html", solid=True)}
<main>
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Solutions</p>
    <h1>Built around the decisions, not the data</h1>
    <p class="lede">The same condition and degradation database serves three very different decisions: what to do on an operating plant this month, how to design the next one, and what to change in the factory.</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sol" id="operators">
      <div class="sol-text">
        <p class="eyebrow">Operating plants</p>
        <h2 class="h2">Prioritise work by what it recovers</h2>
        <p>Cleaning, reinspection, repairs and replacements are scheduled on recoverable energy, expected losses from failure and intervention cost. Before a human-reviewed work order is raised, the system records the predicted net benefit, timeframe and prediction interval for each option, including doing nothing yet.</p>
        <ul>
          <li>Event-triggered and scheduled screening with anomaly grading on site</li>
          <li>Weather-normalised, controlled comparisons between cleaning zones to confirm response</li>
          <li>Energy loss attributed at the metering resolution available, separating equipment, weather and curtailment</li>
          <li>Reassessment triggered by new sites, unrepresented materials or prediction drift</li>
        </ul>
        <p class="decides"><b>Decisions supported</b>Clean · reinspect · repair · replace · defer</p>
      </div>
      <div class="sol-media"><img src="assets/drone.jpg" alt="Inspection drone flying over rows of solar modules" loading="lazy"></div>
    </div>

    <div class="sol" id="developers">
      <div class="sol-text">
        <p class="eyebrow">Planned plants</p>
        <h2 class="h2">Rank design options by lifecycle cost, not just yield</h2>
        <p>Existing irradiance and shading simulations already tell you how orientation and tilt affect energy. Metrifield adds site-specific degradation, failure risk and maintenance cost, with their uncertainties, so design options can be compared on delivered energy and whole-of-life cost together.</p>
        <ul>
          <li>Orientation, tilt, row spacing, mounting height and module configuration ranked jointly</li>
          <li>Serviceability and maintenance access priced into the layout</li>
          <li>Material choice matched to hot, humid, saline or high-UV sites</li>
          <li>Design scenario models become operational twins once the plant is accepted</li>
        </ul>
        <p class="decides"><b>Decisions supported</b>Layout · tilt · row spacing · mounting height · module choice</p>
      </div>
      <div class="sol-media"><img src="assets/hero-poster.jpg" alt="Aerial view of a solar farm layout" loading="lazy"></div>
    </div>

    <div class="sol" id="manufacturers">
      <div class="sol-text">
        <p class="eyebrow">Module manufacturers</p>
        <h2 class="h2">Trace field failure back to the factory</h2>
        <p>Field failure modes and progression rates are linked to bills of materials, supplier batches, lamination processes and factory test records. Combined with your accelerated ageing results, the data identifies unsuitable material combinations and batch-specific process deviations earlier, narrowing material trials and reducing rework and warranty cost.</p>
        <ul>
          <li>Same batches compared across environments; different batches within comparable environments</li>
          <li>Encapsulant, backsheet or rear glass, and edge seal combinations ranked by environmental suitability</li>
          <li>Lamination process windows (temperature, time, vacuum) flagged for controlled factory trials</li>
          <li>Targeted inspection of at-risk batches already in the field</li>
        </ul>
        <p class="decides"><b>Decisions supported</b>Material selection · lamination windows · batch QA · product configuration by region</p>
      </div>
      <div class="sol-media"><img src="assets/factory.jpg" alt="Solar module lamination line" loading="lazy"></div>
    </div>
  </div>
</section>

{cta("Not sure which fits?", "Most engagements start on an operating plant with cleaning and targeted repair decisions, then extend to design and manufacturing feedback.")}
</main>
'''

technology_body = f'''
{nav("technology.html", solid=True)}
<main>
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Technology</p>
    <h1>A hybrid digital twin that predicts which action is most economical, and when</h1>
    <p class="lede">Physics and data combined to optimise the economic value of interventions while continuously updating asset condition. Models track specific assets, compare intervention outcomes and make predictions that later observations can falsify.</p>
  </div>
</section>

<section class="band band-tint">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The evidence chain</p>
      <h2 class="h2">Every link is recorded, so field observations become lifecycle decisions</h2>
    </div>
    <ol class="chain">
      <li>Materials and processes</li>
      <li>Environmental exposure</li>
      <li>Condition evolution</li>
      <li>Energy losses</li>
      <li>Intervention outcomes</li>
    </ol>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Sensing</p>
      <h2 class="h2">The drone finds candidates. The robot confirms them.</h2>
    </div>
    <div class="duo">
      <figure><img src="assets/drone.jpg" alt="Inspection drone with RGB and thermal camera over a solar array" loading="lazy"><figcaption>01 — Drone RGB and thermal survey flags suspect modules</figcaption></figure>
      <figure><img src="assets/crawler.jpg" alt="Crawler robot on a solar module carrying a terahertz scanner" loading="lazy"><figcaption>02 — Robot on the panel scans them with terahertz</figcaption></figure>
    </div>
    <div class="grid2">
      <div><h3>Drone RGB and thermal screening</h3><p>Drones run scheduled and event-triggered surveys. Edge computing performs image quality checks, module localisation and anomaly grading before data leaves the site, with offline caching for remote plants.</p></div>
      <div><h3>Robot terahertz, on the panel</h3><p>A robot moves onto flagged modules and scans at close range. Scans of high-risk locations and stratified healthy samples give identifiable evidence of interface and dielectric state within compatible encapsulation structures. Scans are allocated where the extra information changes the intervention choice and expected avoided loss exceeds the cost.</p></div>
      <div><h3>Site and microclimate context</h3><p>Terrain, shading and long-term regional climate are combined with on-site irradiance, module and ambient temperature, humidity, wind, salt and dust, to separate regional conditions from microenvironments within the array.</p></div>
      <div><h3>Fast and slow states</h3><p>Operating states follow existing SCADA updates. Slower material states update through inspections, accumulated exposure and extreme events, so each modality updates the same asset's state distribution through calibrated observation models.</p></div>
    </div>
  </div>
</section>

<section class="band band-tint" id="database">
  <div class="wrap">
    <div class="db-top">
    <div class="section-head" style="margin-bottom:0">
      <p class="eyebrow">The climate and condition database</p>
      <h2 class="h2">Where every module is, what it is made of, and how it is behaving</h2>
      <p class="lede">The core asset is a database that links each module to the place it lives. Over time it becomes a map of how solar hardware ages across Australia's climate zones, and a guide to what to build where.</p>
    </div>
    <div class="mapwrap">
      <svg class="aumap" viewBox="0 0 540 470" role="img" aria-labelledby="aumap-title"><title id="aumap-title">Map of Australia marking six climate zones used to stratify sites</title><path d="M374.7 28.6 L387.4 69.4 L407.2 81.8 L415.3 122.5 L424.7 134.9 L452.6 157.1 L468.8 185.5 L495.6 209.0 L497.9 236.2 L503.7 249.8 L495.6 284.4 L482.8 302.9 L475.8 315.2 L472.3 321.4 L463.0 341.2 L461.9 354.8 L450.2 363.4 L432.8 365.9 L420.0 379.5 L408.4 372.1 L402.6 369.6 L386.3 377.0 L364.2 369.6 L354.9 365.9 L342.1 353.5 L334.0 336.2 L328.1 327.6 L318.8 330.1 L310.7 316.5 L297.9 325.1 L278.1 302.9 L272.3 293.0 L240.9 285.6 L216.5 288.1 L182.8 295.5 L158.4 311.5 L135.1 315.2 L107.2 321.4 L88.6 328.8 L56.0 321.4 L54.9 304.1 L64.2 291.8 L61.9 273.2 L50.2 252.2 L36.3 218.9 L38.6 199.1 L44.4 167.0 L61.9 155.9 L75.8 152.2 L96.7 147.2 L122.3 138.6 L138.6 118.8 L154.9 110.2 L157.2 96.6 L171.2 87.9 L188.6 69.4 L207.2 81.8 L224.7 80.5 L232.8 58.3 L238.6 49.6 L252.6 37.3 L259.5 34.8 L279.3 44.7 L297.9 44.7 L309.5 48.4 L296.7 64.5 L299.1 79.3 L310.7 92.9 L337.4 112.6 L354.9 111.4 L363.0 81.8 L365.3 50.9 L374.7 28.6 Z" fill="var(--map-fill)" stroke="var(--map-line)" stroke-width="1.5" stroke-linejoin="round"/><path d="M400.2 399.2 L418.8 404.2 L442.1 401.7 L440.9 421.5 L437.4 430.1 L427.0 435.1 L415.3 432.6 L407.2 419.0 L400.2 405.4 L400.2 399.2 Z" fill="var(--map-fill)" stroke="var(--map-line)" stroke-width="1.5" stroke-linejoin="round"/><circle cx="238.6" cy="49.6" r="26" fill="#D6A75A" opacity=".22"/><circle cx="238.6" cy="49.6" r="13" fill="#D6A75A"/><text x="238.6" y="54.1" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">1</text><circle cx="274.7" cy="189.2" r="26" fill="#C77D52" opacity=".22"/><circle cx="274.7" cy="189.2" r="13" fill="#C77D52"/><text x="274.7" y="193.7" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">2</text><circle cx="485.1" cy="223.8" r="26" fill="#7FA8C9" opacity=".22"/><circle cx="485.1" cy="223.8" r="13" fill="#7FA8C9"/><text x="485.1" y="228.3" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">3</text><circle cx="432.8" cy="347.4" r="26" fill="#5F8F7A" opacity=".22"/><circle cx="432.8" cy="347.4" r="13" fill="#5F8F7A"/><text x="432.8" y="351.9" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">4</text><circle cx="72.3" cy="297.9" r="26" fill="#9C8E6A" opacity=".22"/><circle cx="72.3" cy="297.9" r="13" fill="#9C8E6A"/><text x="72.3" y="302.4" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">5</text><circle cx="424.7" cy="415.3" r="26" fill="#6E7F99" opacity=".22"/><circle cx="424.7" cy="415.3" r="13" fill="#6E7F99"/><text x="424.7" y="419.8" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">6</text></svg>
      <ol class="zones"><li><span class="dot" style="background:#D6A75A">1</span><div><b>Monsoonal north</b><span>Heat, humidity, UV, cyclones</span></div></li><li><span class="dot" style="background:#C77D52">2</span><div><b>Arid interior</b><span>Extreme heat, dust, thermal cycling</span></div></li><li><span class="dot" style="background:#7FA8C9">3</span><div><b>Subtropical east</b><span>Humidity, hail, storms</span></div></li><li><span class="dot" style="background:#5F8F7A">4</span><div><b>Temperate south-east</b><span>Frost, rain, moderate UV</span></div></li><li><span class="dot" style="background:#9C8E6A">5</span><div><b>Mediterranean south-west</b><span>Salt, dry heat, winter rain</span></div></li><li><span class="dot" style="background:#6E7F99">6</span><div><b>Cool temperate Tasmania</b><span>Wind, moisture, low irradiance</span></div></li></ol>
    </div>
    </div>
    <div class="grid2" style="margin-top:clamp(36px,5vw,64px)">
      <div><h3>Each module, as a record</h3><p>Manufacturer, model, bill of materials, factory batch and lamination record, install date, string position and mounting. Then every drone image, thermal frame, terahertz scan, work order and replacement, with timestamps.</p></div>
      <div><h3>Linked to its environment</h3><p>Climate zone, long-term weather history, terrain and shading, distance from the coast, salt and dust load, vegetation and fire exposure, plus on-site irradiance, temperature, humidity and wind, down to the microclimate inside the array.</p></div>
      <div><h3>Linked to its performance</h3><p>SCADA and string-level electrical data, weather-normalised, so condition changes can be tied to energy loss at the metering resolution available.</p></div>
      <div><h3>Six climate zones as the proving ground</h3><p>From the monsoonal north to temperate Tasmania, each zone has its own dominant degradation mechanisms. Sites are stratified across them so the same materials can be compared under different exposure.</p></div>
      <div><h3>From database to degradation map</h3><p>Repeat inspections of the same modules, season after season, turn individual findings into degradation rates by material, batch and zone, then into a fleet-wide risk ranking.</p></div>
      <div><h3>From map to deployment guidance</h3><p>Invert the model: given a site's terrain, climate and a proposed module construction, estimate degradation, maintenance cost and premature replacement risk before a single post goes in.</p></div>
    </div>
  </div>
</section>

<section class="band band-dark">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Data and models</p>
      <h2 class="h2">One asset record, a hierarchy of twins</h2>
      <p class="lede">Module IDs, locations, electrical topology, manufacturing batches and replacement histories link RGB, thermal and terahertz inspections with exposure, SCADA data, work orders and actual expenditure.</p>
    </div>
    <div class="grid2">
      <div><h3>Aligned before attributed</h3><p>Timestamps, units, calibration records and data versions are standardised and terminology mapped to PV-Onto. Inconsistent sampling and interval averaging cause systematic power-prediction errors, so alignment precedes any anomaly attribution.</p></div>
      <div><h3>Physics sets the baseline</h3><p>Irradiance, heat-balance and electrical models establish normal-operation baselines. Hierarchical degradation models represent cumulative environmental effects. Cost models evaluate interventions.</p></div>
      <div><h3>Machine learning where it earns its place</h3><p>Parameter estimation, residual modelling and fast surrogate predictions. Model selection stays problem-specific: established solvers are used where they outperform learned ones, and historical fit is never treated as proof of long-term accuracy.</p></div>
      <div><h3>Credibility tied to use</h3><p>Verification of implementation, parameter calibration and independent predictive evaluation are kept distinct, with credibility defined for specific operating conditions, prediction horizons and decisions.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="steps">
      <div class="section-head" style="margin-bottom:0;max-width:none">
        <p class="eyebrow">The loop</p>
        <h2 class="h2">Predictions are tested against outcomes, then the models update</h2>
        <div class="prose" style="max-width:none;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px 40px">
          <p>Before a work order is issued, the system records predicted net benefit, timeframe and prediction interval for cleaning, repair, replacement and deferral. Weather normalisation and controlled comparisons between cleaning zones then assess what actually happened.</p>
          <p>Each intervention's cost, condition change and generation response feeds back into the models. New sites, unrepresented materials or significant drift trigger reassessment, so field experience improves subsequent maintenance, plant design and module production.</p>
          <p><strong>Australian sites are stratified</strong> by temperature and humidity cycling, UV, salt and dust, rainfall and extreme-event exposure, with array microclimates, remote-site travel, communications constraints and local service costs built in. Model structures and priors are shared across sites while calibration stays local.</p>
        </div>
      </div>
      <figure class="figure">
        <a class="frame" href="assets/architecture.jpg" target="_blank" rel="noopener" aria-label="Open diagram at full size"><img src="assets/architecture.jpg" width="3600" height="2118" alt="System diagram showing the feedback loop from decisions and measured outcomes back to the digital twin." loading="lazy"></a>
        <figcaption>Actions, measured outcomes and costs flow back to update the twin. Click to enlarge.</figcaption>
      </figure>
    </div>
  </div>
</section>

{cta("Want the technical detail?", "We are happy to walk engineering and asset-management teams through the sensing, data model and twin architecture.")}
</main>
'''

about_body = f'''
{nav("about.html", solid=True)}
<main>
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>Metrifield Dynamics connects what happens to a solar module with what it costs</h1>
    <p class="lede">We are a Sydney-based company founded in 2026 by three people with backgrounds in field sensing, edge AI, infrastructure and energy. Our aim is a measurable, repeatable reduction in the lifecycle cost of utility-scale solar, under Australian conditions first.</p>
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
        <div class="photo"></div>
        <h3>Harrison</h3>
        <p class="role">Co-founder</p>
        <p>Bio to come.</p>
      </div>
      <div class="person">
        <div class="photo"><img src="assets/sohan.jpg" alt="Sohan Domingo" width="800" height="1000" loading="lazy"></div>
        <h3>Sohan Domingo</h3>
        <p class="role">Co-founder</p>
        <p>Founder of Edgegenix, a Sydney venture studio building computer vision and edge inference systems for councils, utilities, fire agencies and insurers, and of BrightBuddy, bringing companion robots to Australian aged care. Previously with Pano AI. Long-standing focus on LiDAR, computer vision and geospatial systems for infrastructure.</p>
      </div>
      <div class="person">
        <div class="photo"></div>
        <h3>Lauren</h3>
        <p class="role">Co-founder</p>
        <p>Bio to come.</p>
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

{cta("Interested in working with us?", "Pilot sites, data partners, research collaborators and engineers: we would like to hear from you.")}
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
  "index.html": ("Metrifield Dynamics — Lifecycle intelligence for utility-scale solar", "Metrifield links module materials, site exposure, inspection evidence and energy performance into one record, so solar maintenance and design decisions are made on lifecycle cost.", index_body),
  "solutions.html": ("Solutions — Metrifield Dynamics", "Decision support for operating plants, planned plants and module manufacturers, from one condition and degradation database.", solutions_body),
  "technology.html": ("Technology — Metrifield Dynamics", "Tiered RGB, thermal and terahertz sensing, a multimodal asset record and a hybrid physics-and-data digital twin that predicts the most economical action.", technology_body),
  "about.html": ("About — Metrifield Dynamics", "Metrifield Dynamics is a Sydney-based company founded by Harrison, Sohan Domingo and Lauren to reduce the lifecycle cost of utility-scale solar.", about_body),
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
(ROOT/"_redirects").write_text("https://metrifield.com/* https://www.metrifield.com/:splat 301\n")
print("built", ", ".join(PAGES))
