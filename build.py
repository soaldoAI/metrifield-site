#!/usr/bin/env python3
"""Builds the static Metrifield site: index, capabilities, technology, about, contact.
Run: python3 build.py  → writes *.html next to this file, plus body.html (artifact preview copy of index)."""
import pathlib, re

ROOT = pathlib.Path(__file__).parent
import hashlib
VER = hashlib.md5((ROOT/"styles.css").read_bytes()).hexdigest()[:8]
SITE = "https://www.metrifield.com"
EMAIL = "info@metrifield.com"

LOGO = '''<svg viewBox="0 0 28 28" aria-hidden="true"><rect x="1.5" y="1.5" width="25" height="25" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M6 19.5 L11 10 L15 16 L18 12 L22 19.5" fill="none" stroke="#E59A1C" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/></svg>'''
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'

NAV = [("index.html","Home"),("capabilities.html","Capabilities"),("technology.html","Technologies"),("about.html","About"),("contact.html","Contact")]

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
<link rel="stylesheet" href="styles.css?v={VER}">
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
    <div class="fcol"><b>Site</b><a href="capabilities.html">Capabilities</a><a href="technology.html">Technologies</a><a href="about.html">About</a><a href="contact.html">Contact</a></div>
    <div class="fcol"><b>Contact</b><a href="mailto:{EMAIL}">{EMAIL}</a><span>Sydney, NSW</span></div>
    <div class="legal"><span>© 2026 Metrifield Dynamics Pty Ltd</span><span>metrifield.com</span></div>
  </div>
</footer>
<script>
(function(){{
  var n=document.getElementById('nav'),b=n&&n.querySelector('.nav-toggle');
  if(b){{b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)}})}}
  var Z={{
   1:{{name:"Monsoonal &amp; humid tropical north",color:"#D6A75A",regions:"Top End, the Kimberley, far-north and tropical-coast Queensland",exposure:"Heat, humidity, wet–dry seasonality, intense rainfall, prolonged wetting and rapid vegetation growth.",mechanism:"Transient wetting and obstruction are not the same as construction-dependent moisture ingress, corrosion or electrical deterioration — the two must be separated.",act:"RGB for surface and vegetation; thermal only under valid conditions; EL or electrical reference if unresolved; terahertz only for qualified modules with controlled surface moisture. Inspect drainage and vegetation interfaces."}},
   2:{{name:"Warm humid eastern seaboard",color:"#7FA8C9",regions:"Central and south-east Queensland coast and hinterland, New South Wales north and central coast to Sydney",exposure:"Humidity, rain, dew, urban and coastal deposits, bird activity and local shading.",mechanism:"Reversible surface losses may coexist with persistent moisture-related or electrical abnormalities.",act:"RGB links deposits to geometry; thermal localises load-dependent anomalies; EL or electrical tests for unresolved features. Condition-triggered inspection, not postcode-based intervals."}},
   3:{{name:"Arid interior &amp; north-west",color:"#C77D52",regions:"Pilbara, Goldfields and the Western Australian interior, Central Australia, far-north South Australia, western Queensland",exposure:"High module temperature, strong diurnal variation, dry mineral deposits, dust and remoteness.",mechanism:"Reversible soiling and thermal losses differ from interconnection fatigue and encapsulation ageing, and must be confirmed independently.",act:"RGB with soiling references; thermal with irradiance, wind and load context; EL for electrical integrity; terahertz only after excluding surface contamination. Cleaning-value thresholds and dust-aware dock design."}},
   4:{{name:"Semi-arid transition &amp; inland agricultural margins",color:"#9C8E6A",regions:"South Australian mid-north and inland, western New South Wales and the Riverina, southern inland Queensland, the Victorian Mallee",exposure:"Seasonal dry periods, intermittent rain, agricultural and road dust, vegetation cycles, birds and local maintenance activity.",mechanism:"Deposits and shading may create mismatch; installation stress or electrical faults require independent evidence.",act:"Compare the same assets before and after cleaning or seasonal change; RGB and operating data first; escalate selectively to EL, electrical tests or qualified terahertz."}},
   5:{{name:"Mediterranean-type south-west &amp; southern pockets",color:"#5F8F7A",regions:"Perth and the south-west of Western Australia, Adelaide, the Eyre Peninsula and the South Australian coastal south",exposure:"Dry summers, wetter winters, seasonal deposits, extreme heat, smoke and episodic rainfall.",mechanism:"Seasonal soiling, construction-dependent UV and thermal ageing, and possible deposit redistribution after rain.",act:"Repeat RGB and thermal on the same modules across seasons; keep EL conditions comparable; verify post-rain recovery rather than assuming natural cleaning."}},
   6:{{name:"Temperate south-east &amp; Tasmania",color:"#6E7F99",regions:"New South Wales south coast and tablelands, the ACT, Victoria, Tasmania",exposure:"Cooler seasonal conditions, wetting, dew, low solar angles, local frost, site-specific snow or snow load.",mechanism:"Temporary frost and condensation effects must be separated from persistent moisture-related or material deterioration.",act:"Avoid frost and dew artefacts; thermal only in a valid irradiance and load window; EL or electrical reference for persistent abnormalities; reinspect when conditions are suitable."}}
  }};
  var sel=document.getElementById('zone-select'),panel=document.getElementById('zone-panel');
  function showZone(k){{var z=Z[k]; if(!z||!panel)return; panel.hidden=false;
    document.getElementById('zp-dot').style.background=z.color; document.getElementById('zp-eyebrow').textContent='Zone '+k;
    document.getElementById('zp-title').innerHTML=z.name; document.getElementById('zp-regions').textContent=z.regions;
    document.getElementById('zp-exposure').innerHTML=z.exposure; document.getElementById('zp-mechanism').innerHTML=z.mechanism;
    document.getElementById('zp-act').innerHTML=z.act;
    document.querySelectorAll('.zone-pin').forEach(function(e){{e.classList.toggle('active',e.getAttribute('data-zone')===String(k))}});
    document.querySelectorAll('.aumap,.zones').forEach(function(e){{e.classList.add('focused')}});
    document.querySelectorAll('.aumap .region').forEach(function(r){{r.classList.toggle('alive',r.getAttribute('data-region')===String(k))}});
    if(sel&&sel.value!==String(k)){{for(var i=0;i<sel.options.length;i++){{if(sel.options[i].value===String(k)){{sel.selectedIndex=i;break}}}}}}
    panel.scrollIntoView({{behavior:'smooth',block:'nearest'}});
  }}
  if(sel){{sel.addEventListener('change',function(){{if(sel.value)showZone(sel.value)}})}}
  document.querySelectorAll('.zone-pin').forEach(function(e){{
    e.addEventListener('click',function(){{showZone(e.getAttribute('data-zone'))}});
    e.addEventListener('keydown',function(ev){{if(ev.key==='Enter'||ev.key===' '){{ev.preventDefault();showZone(e.getAttribute('data-zone'))}}}});
  }});
  if('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches){{
    var secs=[].slice.call(document.querySelectorAll('main > section'));
    secs.forEach(function(sec,i){{ var r=sec.getBoundingClientRect(); if(r.top>window.innerHeight*0.9){{sec.classList.add('is-entering')}} }});
    var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.remove('is-entering');io.unobserve(e.target)}}}})}},{{rootMargin:'0px 0px -12% 0px',threshold:0.08}});
    secs.forEach(function(sec){{io.observe(sec)}});
  }}
  var DN={{"rgb": {{"col": "Field sensing", "n": "01", "title": "RGB + thermal", "q": "Is it dirt, or is it damage?", "body": "Scheduled and event-triggered drone surveys capture RGB and thermal imagery across the whole array. Edge AI checks image quality in flight, maps every observation to an individual module ID and grades anomalies, so detailed inspection goes only where it is likely to change a decision.", "inputs": "Flight plans \u00b7 RGB and thermal frames \u00b7 module map", "outputs": "Located, graded anomalies per module", "to": "db", "link": "technology.html#sensing", "linktext": "Sensing on the Technology page"}}, "thz": {{"col": "Field sensing", "n": "02", "title": "Targeted THz", "q": "What is happening inside the glass?", "body": "A robot moves onto flagged modules, and onto healthy reference modules, and scans them at close range with terahertz. Terahertz passes through glass and encapsulant and reflects at each internal interface, giving evidence of moisture, delamination and material change that surface imaging and thermal cannot show.", "inputs": "Priority list from screening \u00b7 healthy controls", "outputs": "Subsurface condition per scanned module", "to": "db", "link": "technology.html#sensing", "linktext": "Robotic terahertz diagnostics"}}, "site": {{"col": "Field sensing", "n": "03", "title": "Site context", "q": "Is it the module, or the place it lives?", "body": "Terrain, shading and long-term climate are combined with on-site irradiance, module and ambient temperature, humidity, wind, salt and dust. This separates regional conditions from microclimates inside the array, so environmental effects are not mistaken for persistent faults.", "inputs": "Weather station \u00b7 climate records \u00b7 terrain model", "outputs": "Exposure history for every module location", "to": "twin", "link": "index.html#regions", "linktext": "Regional exposure map"}}, "db": {{"col": "Cloud intelligence", "n": "04", "title": "Multimodal asset database", "q": "What do we know about this exact module?", "body": "Every inspection, scan, electrical reading, work order and real cost is attached to a module ID, its string position, its manufacturing batch and a timestamp. Data is aligned and calibrated before anything is attributed, so the record can be trusted across years and sites.", "inputs": "Inspections \u00b7 THz scans \u00b7 SCADA \u00b7 work orders \u00b7 bills of materials", "outputs": "A traceable condition history per module", "to": "twin", "link": "technology.html#database", "linktext": "The climate and condition database"}}, "twin": {{"col": "Cloud intelligence", "n": "05", "title": "Dynamic digital twin", "q": "Which action is worth taking, and when?", "body": "Physics-based yield, thermal and degradation models are combined with field data to form module, string and plant twins. For each option \u2014 clean, reinspect, repair, replace or defer \u2014 the twin predicts recoverable energy, failure risk and cost, with a prediction interval, before a work order is raised.", "inputs": "Asset record \u00b7 exposure history \u00b7 electrical data", "outputs": "Ranked interventions with predicted net benefit", "to": "ops", "link": "technology.html", "linktext": "How the twin works"}}, "ops": {{"col": "Decision support", "n": "06", "title": "Operating plants", "q": "Recover energy without paying for low-value work.", "body": "Interventions are scheduled on recoverable energy, expected loss and cost, then verified against measured outcomes. Weather-normalised comparisons between cleaning zones confirm what actually happened, and the result feeds back into the models.", "inputs": "Ranked interventions", "outputs": "Work orders \u00b7 measured outcomes \u00b7 actual costs", "to": "db", "link": "capabilities.html#operators", "linktext": "Operating plants"}}, "new": {{"col": "Decision support", "n": "07", "title": "New plants", "q": "Avoid costs before they are built in.", "body": "Field evidence from comparable sites is translated into design scenarios: module selection, layout, mounting and maintenance access are compared on lifetime energy and cost, not upfront cost alone. Design assumptions carry through to commissioning and become the operating twin.", "inputs": "Site exposure \u00b7 degradation evidence by material and zone", "outputs": "Design scenarios ranked by lifetime value", "to": "db", "link": "capabilities.html#developers", "linktext": "Deploying plants"}}, "mfg": {{"col": "Decision support", "n": "08", "title": "Manufacturers", "q": "Prevent recurring failures at the source.", "body": "Field failure modes are compared across matched environments and batches to find links to material selection and process conditions. Targeted validation then supports changes that reduce future defects, rework and warranty exposure.", "inputs": "Field performance by batch, material and climate zone", "outputs": "Material and process recommendations \u00b7 targeted QA", "to": "db", "link": "capabilities.html#manufacturers", "linktext": "Manufacturing plants"}}}}, DORD=["rgb", "thz", "site", "db", "twin", "ops", "new", "mfg"], dcur=null;
  var dpanel=document.getElementById('dpanel');
  var idg=document.getElementById('idiag');
  function dfocus(ids,outs){{ // ids: tiles to keep alive; outs: outcomes to keep alive; null = clear
    if(!idg) return;
    if(!ids){{ idg.classList.remove('focused'); document.querySelectorAll('.dtile,.dout').forEach(function(e){{e.classList.remove('alive','active')}}); document.querySelectorAll('[data-arrow]').forEach(function(a){{a.classList.remove('lit')}}); return; }}
    idg.classList.add('focused');
    document.querySelectorAll('.dtile').forEach(function(t){{t.classList.toggle('alive',ids.indexOf(t.getAttribute('data-node'))>=0)}});
    document.querySelectorAll('.dout').forEach(function(b){{b.classList.toggle('alive',outs.indexOf(b.getAttribute('data-out'))>=0)}});
    var h=document.getElementById('dhint'); if(h) h.hidden=true;
  }}
  var OUT_OF={{}}; // node -> outcomes it contributes to (derived)
  var dscrim=document.getElementById('dscrim');
  function dscrimSet(on){{ if(!dscrim) return; var mobile=window.innerWidth<=960; if(mobile){{ [dscrim,dpanel,opanel].forEach(function(el){{ if(el && el.parentNode!==document.body) document.body.appendChild(el); }}); }} dscrim.classList.toggle('on', on&&mobile); }}
  if(dscrim){{ dscrim.addEventListener('click',function(){{ if(dcur) dhide(); if(ocur) ohide(); }}); }}
  [dpanel,opanel].forEach(function(pn){{ if(!pn) return; var y0=null; pn.addEventListener('touchstart',function(e){{ y0=e.touches[0].clientY }},{{passive:true}}); pn.addEventListener('touchend',function(e){{ if(y0===null) return; var dy=e.changedTouches[0].clientY-y0; if(dy>70 && pn.scrollTop<=0){{ if(dcur) dhide(); if(ocur) ohide(); }} y0=null; }},{{passive:true}}); }});
  var dhome=document.getElementById('idiag');
  window.addEventListener('resize',function(){{ if(window.innerWidth>960 && dhome){{ [dpanel,opanel].forEach(function(el){{ if(el && el.parentNode===document.body) dhome.appendChild(el); }}); if(dscrim) dscrim.classList.remove('on'); }} }});
  var dfrom=null;
  function dshow(id,from){{ var d=DN[id]; if(!d||!dpanel) return; dcur=id; ocur=null; dfrom=from||null; if(opanel) opanel.hidden=true;
    document.getElementById('dp-col').textContent=d.col; document.getElementById('dp-title').textContent=d.n+' — '+d.title;
    document.getElementById('dp-q').textContent=d.q; document.getElementById('dp-body').textContent=d.body;
    document.getElementById('dp-in').textContent=d.inputs; document.getElementById('dp-out').textContent=d.outputs;
    var l=document.getElementById('dp-link'); l.href=d.link; l.firstChild.textContent=d.linktext+' ';
    document.getElementById('dp-count').textContent=d.n+' / 0'+DORD.length;
    var outs=Object.keys(DOUT).filter(function(k){{return DOUT[k].nodes.indexOf(id)>=0}});
    dfocus([id],(from&&from.out)?[from.out]:[]);
    var bk=document.getElementById('dp-back'); if(bk){{ if(from&&from.out){{bk.hidden=false; bk.textContent='← Back to '+DOUT[from.out].title.replace('&amp;','&'); bk.setAttribute('data-go-out',from.out)}} else bk.hidden=true; }}
    var oc=document.getElementById('dp-contrib'); if(oc){{oc.innerHTML=outs.map(function(k){{return '<button type="button" class="dtag" data-go-out="'+k+'">'+DOUT[k].title+'</button>'}}).join('')}}
    document.querySelectorAll('.dtile').forEach(function(t){{var on=t.getAttribute('data-node')===id; t.classList.toggle('active',on); t.setAttribute('aria-expanded',on)}});
    document.querySelectorAll('[data-arrow]').forEach(function(a){{a.classList.remove('lit')}});
    document.querySelectorAll('[data-arrow="'+id+'"]').forEach(function(a){{a.classList.add('lit')}});
    if(id==='ops'||id==='new'||id==='mfg'){{document.querySelectorAll('[data-arrow="back"]').forEach(function(a){{a.classList.add('lit')}})}}
    dpanel.hidden=false; dpanel.classList.remove('pop'); void dpanel.offsetWidth; dpanel.classList.add('pop');
    dscrimSet(true);
  }}
  function dhide(){{ dcur=null; dscrimSet(false); if(dpanel) dpanel.hidden=true; document.querySelectorAll('.dtile').forEach(function(t){{t.setAttribute('aria-expanded','false')}}); dfocus(null) }}
  document.querySelectorAll('.dtile').forEach(function(t){{t.addEventListener('click',function(){{var id=t.getAttribute('data-node'); if(dcur===id) dhide(); else dshow(id)}})}});
  var dc=document.getElementById('dp-close'); if(dc) dc.addEventListener('click',dhide);
  var dp=document.getElementById('dp-prev'), dnx=document.getElementById('dp-next');
  if(dp) dp.addEventListener('click',function(){{var i=DORD.indexOf(dcur); dshow(DORD[(i-1+DORD.length)%DORD.length])}});
  if(dnx) dnx.addEventListener('click',function(){{var i=DORD.indexOf(dcur); dshow(DORD[(i+1)%DORD.length])}});
  document.addEventListener('keydown',function(e){{ if(!dcur) return; if(e.key==='Escape') dhide(); if(e.key==='ArrowRight') dnx.click(); if(e.key==='ArrowLeft') dp.click(); }});
  var DOUT={{"deploy": {{"title": "Lower deployment cost", "metric": "Construction cost per MW, including rework and premature replacement in the first years", "how": "Design choices are tested against field evidence from comparable sites before construction: module selection, layout, mounting and maintenance access are compared on lifetime value rather than upfront price, so costly corrections are avoided after the plant is built.", "nodes": ["site", "db", "twin", "new"], "link": "capabilities.html#developers", "linktext": "Deploying plants"}}, "om": {{"title": "Lower O&amp;M cost", "metric": "Operating cost per MW per year; inspection visits and specialist call-outs avoided", "how": "Fleet-wide drone screening replaces routine manual inspection, terahertz diagnostics are sent only where they can change a decision, and work orders are ranked by expected net benefit, so low-value cleaning and unnecessary replacements stop.", "nodes": ["rgb", "thz", "twin", "ops"], "link": "capabilities.html#operators", "linktext": "Operating plants"}}, "life": {{"title": "Longer useful life", "metric": "Degradation rate in percent per year; economic service life of the module fleet", "how": "Subsurface problems such as moisture ingress and delamination are found before they become failures, material and batch risks are traced back to the factory, and sites are matched to constructions that suit their climate zone.", "nodes": ["thz", "db", "mfg", "new"], "link": "technology.html#database", "linktext": "The climate and condition database"}}, "energy": {{"title": "More delivered energy", "metric": "MWh recovered per year; availability; weather-normalised performance ratio", "how": "Energy losses are attributed to their cause at the metering resolution available, cleaning and repair are timed by recoverable energy, and measured generation response after each intervention confirms what was actually recovered.", "nodes": ["rgb", "site", "twin", "ops"], "link": "capabilities.html#operators", "linktext": "Operating plants"}}, "warranty": {{"title": "Lower warranty exposure", "metric": "Recurring defects per batch; claims and rework per MW shipped", "how": "Field performance is compared across matched environments and manufacturing batches, so material and process causes of recurring failures are identified and validated before they reach wider production.", "nodes": ["thz", "db", "mfg"], "link": "capabilities.html#manufacturers", "linktext": "Manufacturing plants"}}, "lcoe": {{"title": "Lower lifecycle cost", "metric": "Net LCOE improvement after all platform costs: equipment, inspection, computing and model maintenance", "how": "The outcomes above act on both sides of the LCOE ratio at once: lower deployment, operating and replacement cost in the numerator, more delivered energy over a longer life in the denominator. Every claim is benchmarked against the plant's existing workflow.", "nodes": ["rgb", "thz", "site", "db", "twin", "ops", "new", "mfg"], "link": "technology.html", "linktext": "How it is measured"}}}}, ocur=null;
  var opanel=document.getElementById('opanel');
  function oshow(k,from){{ var o=DOUT[k]; if(!o||!opanel) return; ocur=k; dcur=null; if(dpanel) dpanel.hidden=true;
    document.getElementById('op-title').innerHTML=o.title; document.getElementById('op-metric').textContent=o.metric; document.getElementById('op-how').textContent=o.how;
    var l=document.getElementById('op-link'); l.href=o.link; l.firstChild.textContent=o.linktext+' ';
    dfocus((from&&from.node)?[from.node]:[],[k]);
    var ob=document.getElementById('op-back'); if(ob){{ if(from&&from.node){{ob.hidden=false; ob.textContent='← Back to '+DN[from.node].n+' '+DN[from.node].title; ob.setAttribute('data-go-node',from.node)}} else ob.hidden=true; }}
    var dr=document.getElementById('op-drivers'); if(dr){{dr.innerHTML=o.nodes.map(function(n){{return '<button type="button" class="dtag" data-go-node="'+n+'"><i>'+DN[n].n+'</i>'+DN[n].title+'</button>'}}).join('')}}
    document.querySelectorAll('.dout').forEach(function(b){{b.classList.toggle('active',b.getAttribute('data-out')===k)}});
    document.querySelectorAll('[data-arrow]').forEach(function(a){{a.classList.toggle('lit', k==='lcoe')}});
    opanel.hidden=false; opanel.classList.remove('pop'); void opanel.offsetWidth; opanel.classList.add('pop');
    dscrimSet(true);
  }}
  function ohide(){{ ocur=null; dscrimSet(false); if(opanel) opanel.hidden=true; dfocus(null) }}
  document.querySelectorAll('.dout').forEach(function(b){{b.addEventListener('click',function(){{var k=b.getAttribute('data-out'); if(ocur===k) ohide(); else oshow(k)}})}});
  var oc=document.getElementById('op-close'); if(oc) oc.addEventListener('click',ohide);
  document.addEventListener('click',function(e){{ var g=e.target.closest('[data-go-out]'); if(g){{ var fromNode=dcur; oshow(g.getAttribute('data-go-out'), fromNode?{{node:fromNode}}:null); return}} var n=e.target.closest('[data-go-node]'); if(n){{ var fromOut=ocur; dshow(n.getAttribute('data-go-node'), fromOut?{{out:fromOut}}:null)}} }});
  if(idg){{ idg.addEventListener('click',function(e){{ if(!e.target.closest('.dtile,.dout,.dpanel')){{ if(dcur) dhide(); if(ocur) ohide(); }} }}); }}
  document.addEventListener('keydown',function(e){{ if(e.key==='Escape'&&ocur) ohide(); }});
  var HUB={{"record": {{"dir": "in", "title": "Each module, as a record", "text": "Manufacturer, model, bill of materials, factory batch and lamination record, install date, string position and mounting. Then every drone image, thermal frame, terahertz scan, work order and replacement, with timestamps."}}, "environment": {{"dir": "in", "title": "Linked to its environment", "text": "Climate zone, long-term weather history, terrain and shading, distance from the coast, salt and dust load, vegetation and fire exposure, plus on-site irradiance, temperature, humidity and wind, down to the microclimate inside the array."}}, "performance": {{"dir": "in", "title": "Linked to its performance", "text": "SCADA and string-level electrical data, weather-normalised, so condition changes can be tied to energy loss at the metering resolution available."}}, "zones": {{"dir": "in", "title": "Six climate zones as the proving ground", "text": "From the monsoonal north to temperate Tasmania, each zone has its own dominant degradation mechanisms. Sites are stratified across them so the same materials can be compared under different exposure."}}, "map": {{"dir": "out", "title": "From database to degradation map", "text": "Repeat inspections of the same modules, season after season, turn individual findings into degradation rates by material, batch and zone, then into a fleet-wide risk ranking."}}, "guidance": {{"dir": "out", "title": "From map to deployment guidance", "text": "Invert the model: given a site's terrain, climate and a proposed module construction, estimate degradation, maintenance cost and premature replacement risk before a single post goes in."}}}}, hcur=null;
  var hwrap=document.querySelector('.hubwrap');
  function hshow(k){{ if(!hwrap) return; var h=HUB[k]; hcur=k;
    document.getElementById('hp-eyebrow').textContent=h.dir==='in'?'Flows in':'Comes out';
    document.getElementById('hp-title').textContent=h.title; document.getElementById('hp-what').textContent=h.text;
    hwrap.classList.add('focused'); document.querySelectorAll('.hnode,.hlink').forEach(function(e){{e.classList.toggle('alive',e.getAttribute('data-h')===k)}});
    document.querySelectorAll('.hnode').forEach(function(e){{e.classList.toggle('active',e.getAttribute('data-h')===k)}});
    hplace(k);
  }}
  function hplace(k){{ var pop=document.getElementById('hpanel'), sc=document.querySelector('.hubscroll'), node=document.querySelector('.hnode[data-h="'+k+'"]'); if(!pop||!sc||!node) return;
    pop.hidden=false; pop.classList.remove('pop'); void pop.offsetWidth; pop.classList.add('pop');
    if(window.innerWidth<=760){{ pop.style.left=pop.style.top=''; pop.classList.add('hpop-static'); pop.scrollIntoView({{behavior:'smooth',block:'nearest'}}); return; }}
    pop.classList.remove('hpop-static');
    var r=node.getBoundingClientRect(), c=sc.getBoundingClientRect(), out=node.classList.contains('hnode-out'), pw=pop.offsetWidth, ph=pop.offsetHeight, gap=14;
    var left=out? r.left-c.left-pw-gap : r.right-c.left+gap;
    var top=r.top-c.top+r.height/2-ph/2;
    top=Math.max(0,Math.min(top,c.height-ph)); left=Math.max(0,Math.min(left,c.width-pw));
    pop.classList.toggle('hpop-left',out); pop.style.left=left+'px'; pop.style.top=top+'px';
  }}
  window.addEventListener('resize',function(){{ if(hcur) hplace(hcur) }});
  var hx=document.getElementById('hp-close'); if(hx) hx.addEventListener('click',hreset);
  document.addEventListener('keydown',function(e){{ if(e.key==='Escape'&&hcur) hreset() }});
  function hreset(){{ hcur=null; if(!hwrap) return; hwrap.classList.remove('focused'); document.querySelectorAll('.hnode,.hlink').forEach(function(e){{e.classList.remove('alive','active')}});
    var pop=document.getElementById('hpanel'); if(pop) pop.hidden=true; }}
  document.querySelectorAll('.hnode').forEach(function(n){{ var k=n.getAttribute('data-h'); n.addEventListener('click',function(){{ hcur===k?hreset():hshow(k) }}); n.addEventListener('keydown',function(e){{ if(e.key==='Enter'||e.key===' '){{e.preventDefault(); hcur===k?hreset():hshow(k)}} }}); }});
  var hc=document.querySelector('.hcore'); if(hc){{ hc.addEventListener('click',hreset); hc.addEventListener('keydown',function(e){{ if(e.key==='Enter'||e.key===' '){{e.preventDefault();hreset()}} }}); }}
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
    <h1 class="hero-h1"><span>Intelligent Inspection.</span> <em>Spatiotemporal Twins.</em></h1>
    <p class="lede">Robotic terahertz diagnostics assess subsurface condition. Digital twins track change across sites and time, guiding decisions to lower lifecycle costs.</p>
    <div class="hero-actions">
      <a class="btn btn-accent" href="technology.html">Explore our technology {ARROW}</a>
      <a class="btn btn-outline" href="contact.html">Talk to our team</a>
    </div>
    <div class="hero-foot">
      <span>Sensor <b>RGB&thinsp;|&thinsp;Thermal&thinsp;|&thinsp;THz</b></span>
      <span>Platform <b>UAV&thinsp;|&thinsp;UGV</b></span>
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

      <div class="idiag" id="idiag">
        <div class="idiag-head"><h3>PV lifecycle cost optimisation</h3><p class="dhint" id="dhint">Click any step or outcome to explore</p></div>
        <div class="idiag-grid">
          <div class="dcol dcol-sense"><h4>Field sensing</h4><button type="button" class="dtile" data-node="rgb" aria-expanded="false"><img src="assets/drone.jpg" alt="" loading="lazy"><span class="dt"><b>RGB + thermal</b><i>Drone survey</i><small>Routine screening<br>Edge AI: locate &amp; triage</small></span><span class="dn">01</span></button><button type="button" class="dtile" data-node="thz" aria-expanded="false"><img src="assets/crawler.jpg" alt="" loading="lazy"><span class="dt"><b>Targeted THz</b><i>Robot on the panel</i><small>Encapsulation &amp; interfaces<br>Confirms what imaging flags</small></span><span class="dn">02</span></button><button type="button" class="dtile" data-node="site" aria-expanded="false"><img src="assets/weather.jpg" alt="" loading="lazy"><span class="dt"><b>Site context</b><i>Climate · terrain · exposure</i><small>Irradiance, temperature,<br>humidity, wind, salt &amp; dust</small></span><span class="dn">03</span></button></div>
          <div class="dgap" aria-hidden="true"><span data-arrow="rgb"></span><span data-arrow="thz"></span><span data-arrow="site"></span></div>
          <div class="dcol dcol-cloud"><h4>Cloud intelligence</h4><button type="button" class="dtile dtile-big" data-node="db" aria-expanded="false"><span class="dt"><b>Multimodal asset database</b><svg viewBox="0 0 300 120" class="dico"><ellipse cx="48" cy="22" rx="40" ry="14" fill="#4D7FB2"/><path d="M8 22v26c0 8 18 14 40 14s40-6 40-14V22c0 8-18 14-40 14S8 30 8 22z" fill="#6B9AC9"/><path d="M8 48v26c0 8 18 14 40 14s40-6 40-14V48c0 8-18 14-40 14S8 56 8 48z" fill="#4D7FB2"/><path d="M8 74v14c0 8 18 14 40 14s40-6 40-14V74c0 8-18 14-40 14S8 82 8 74z" fill="#2F5F91"/><g transform="translate(110,0)"><rect x="1" y="1" width="188" height="118" rx="10" fill="#fff" stroke="#D5DDE4" stroke-width="2"/><rect x="14" y="14" width="56" height="38" rx="4" fill="#2F5F91"/><g stroke="#fff" stroke-width="1.5" opacity=".7"><path d="M14 27h56M14 40h56M28 14v38M42 14v38M56 14v38"/></g><rect x="80" y="16" width="94" height="8" rx="4" fill="#0E1B2A"/><rect x="80" y="30" width="70" height="7" rx="3.5" fill="#B9C5D0"/><rect x="80" y="43" width="82" height="7" rx="3.5" fill="#B9C5D0"/><circle cx="24" cy="78" r="8" fill="#BA6D4C"/><rect x="40" y="73" width="60" height="9" rx="4.5" fill="#B9C5D0"/><rect x="14" y="96" width="30" height="10" rx="2" fill="#4D7FB2"/><rect x="50" y="92" width="30" height="14" rx="2" fill="#6B9AC9"/><rect x="86" y="86" width="30" height="20" rx="2" fill="#2F5F91"/><rect x="128" y="70" width="46" height="36" rx="6" fill="#F4F6F8" stroke="#D5DDE4"/><path d="M136 98l10-10 8 6 12-14" fill="none" stroke="#BA6D4C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g></svg><small>Module ID · location · time<br>Materials · batch · history<br>SCADA · work orders · cost</small></span><span class="dn">04</span></button><span class="ddown" data-arrow="db" aria-hidden="true"></span><button type="button" class="dtile dtile-big" data-node="twin" aria-expanded="false"><span class="dt"><b>Dynamic digital twin</b><svg viewBox="0 0 400 110" class="dico"><g><path d="M10 70l60-30 70 30-60 30z" fill="#DCE6D8"/><g fill="#2F5F91"><path d="M30 62l34-17 10 5-34 17z"/><path d="M48 71l34-17 10 5-34 17z"/><path d="M66 80l34-17 10 5-34 17z"/><path d="M44 55l34-17 10 5-34 17z"/><path d="M62 64l34-17 10 5-34 17z"/><path d="M80 73l34-17 10 5-34 17z"/></g></g><g transform="translate(165,10)"><circle cx="40" cy="24" r="12" fill="#BA6D4C"/><g stroke="#BA6D4C" stroke-width="2.5" stroke-linecap="round"><path d="M40 4v6M40 38v6M20 24h6M54 24h6M26 10l4 4M50 34l4 4M26 38l4-4M50 14l4-4"/></g><path d="M6 72C20 70 24 50 40 50s20 20 34 22" fill="none" stroke="#0E1B2A" stroke-width="3"/></g><g transform="translate(250,10)"><rect x="8" y="10" width="64" height="60" rx="4" fill="#2F5F91"/><g stroke="#fff" stroke-width="1.2" opacity=".55"><path d="M8 30h64M8 50h64M24 10v60M40 10v60M56 10v60"/></g><path d="M18 20l14 16-6 10 16 10 6 12" fill="none" stroke="#BA6D4C" stroke-width="3" stroke-linejoin="round"/></g><g transform="translate(330,10)"><rect x="8" y="50" width="14" height="22" rx="2" fill="#6B9AC9"/><rect x="30" y="38" width="14" height="34" rx="2" fill="#4D7FB2"/><rect x="52" y="24" width="14" height="48" rx="2" fill="#2F5F91"/><path d="M8 44L30 32 52 18 72 10" fill="none" stroke="#BA6D4C" stroke-width="3" stroke-linecap="round"/></g></svg><small>Yield · degradation · economics<br>Module → string → plant</small></span><span class="dn">05</span></button></div>
          <div class="dgap" aria-hidden="true"><span data-arrow="twin" class="to-ops"></span><span data-arrow="twin" class="to-new"></span><span data-arrow="twin" class="to-mfg"></span></div>
          <div class="dcol dcol-decide"><h4>Decision support</h4><button type="button" class="dtile" data-node="ops" aria-expanded="false"><img src="assets/band.jpg" alt="" loading="lazy"><span class="dt"><b>Operating plants</b><i>Clean · inspect · repair</i><small>Prioritise by net benefit</small></span><span class="dn">06</span></button><button type="button" class="dtile" data-node="new" aria-expanded="false"><img src="assets/aerial.jpg" alt="" loading="lazy"><span class="dt"><b>New plants</b><i>Layout · tilt · module choice</i><small>Compare lifetime cost</small></span><span class="dn">07</span></button><button type="button" class="dtile" data-node="mfg" aria-expanded="false"><img src="assets/factory.jpg" alt="" loading="lazy"><span class="dt"><b>Manufacturers</b><i>Encapsulation · lamination</i><small>Batch QA · warranty risk</small></span><span class="dn">08</span></button></div>
        </div>
        <p class="dloop" data-arrow="back"><span class="dloop-line"></span><span>Model update</span><span class="dloop-r">Actions · measured outcomes · costs</span></p>
        <div class="douts" role="group" aria-label="Outcomes">
          <button type="button" class="dout" data-out="deploy"><i></i><b>Lower deployment cost</b><small>$ / MW built</small></button>
          <button type="button" class="dout" data-out="om"><i></i><b>Lower O&amp;M cost</b><small>$ / MW · year</small></button>
          <button type="button" class="dout" data-out="life"><i></i><b>Longer useful life</b><small>% degradation / year</small></button>
          <button type="button" class="dout" data-out="energy"><i></i><b>More delivered energy</b><small>MWh recovered</small></button>
          <button type="button" class="dout" data-out="warranty"><i></i><b>Lower warranty exposure</b><small>defects / batch</small></button>
          <button type="button" class="dout dout-sum" data-out="lcoe"><i></i><b>Lower lifecycle cost</b><small>net LCOE improvement</small></button>
        </div>
        <div class="dscrim" id="dscrim"></div>
        <div class="dpanel" id="dpanel" hidden>
          <span class="dsheet-grip" aria-hidden="true"></span>
          <div class="dp-top">
            <span class="dp-nav"><button type="button" class="dp-close" id="dp-close">← Overview</button><button type="button" class="dp-close dp-back" id="dp-back" hidden></button></span>
            <span class="dp-pager"><span id="dp-count">01 / 08</span><button type="button" id="dp-prev" aria-label="Previous step">←</button><button type="button" id="dp-next" aria-label="Next step">→</button></span>
          </div>
          <p class="eyebrow" id="dp-col"></p>
          <p class="dp-title" id="dp-title"></p>
          <h3 class="dp-q" id="dp-q"></h3>
          <p class="dp-body" id="dp-body"></p>
          <div class="dp-io"><div><b>In</b><span id="dp-in"></span></div><div><b>Out</b><span id="dp-out"></span></div><div><b>Contributes to</b><span id="dp-contrib"></span></div></div>
          <a class="dp-link" id="dp-link" href="#">Learn more <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg></a>
        </div>
        <div class="dpanel opanel" id="opanel" hidden>
          <span class="dsheet-grip" aria-hidden="true"></span>
          <div class="dp-top"><span class="dp-nav"><button type="button" class="dp-close" id="op-close">← Overview</button><button type="button" class="dp-close dp-back" id="op-back" hidden></button></span><span class="dp-pager">Outcome</span></div>
          <h3 class="dp-q" id="op-title"></h3>
          <div class="dp-io"><div><b>Measured by</b><span id="op-metric"></span></div><div><b>How it is achieved</b><span id="op-how"></span></div></div>
          <div class="dp-io"><div><b>Driven by</b><span id="op-drivers"></span></div></div>
          <a class="dp-link" id="op-link" href="#">Learn more {ARROW}</a>
        </div>
      </div>
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
    <div class="region-intro">
      <div class="section-head" style="margin-bottom:0">
        <p class="eyebrow">Regional exposure &amp; inspection decisions</p>
        <h2 class="h2">Where in Australia are your solar assets?</h2>
        <p class="lede">Two panels can deliver the same power today yet carry very different lifetime costs, because hidden material deterioration develops differently under each site's conditions. Find your region to see the dominant exposures, the mechanisms that must be told apart, and how we diagnose before we act.</p>
      </div>
      <div class="region-pick">
        <label class="zone-pick" for="zone-select">Choose a state or region
          <select id="zone-select">
            <option value="">Select…</option>
            <option value="1">Northern Territory — Top End</option>
            <option value="1">Queensland — far north &amp; tropical coast</option>
            <option value="1">Western Australia — Kimberley</option>
            <option value="2">Queensland — central &amp; south-east coast</option>
            <option value="2">New South Wales — north &amp; central coast, Sydney</option>
            <option value="3">Western Australia — Pilbara, Goldfields &amp; interior</option>
            <option value="3">Northern Territory — Central Australia</option>
            <option value="3">South Australia — far north &amp; outback</option>
            <option value="3">Queensland — western inland</option>
            <option value="4">South Australia — mid-north &amp; inland</option>
            <option value="4">New South Wales — western plains &amp; Riverina</option>
            <option value="4">Queensland — southern inland</option>
            <option value="4">Victoria — Mallee &amp; north-west</option>
            <option value="5">Western Australia — Perth &amp; south-west</option>
            <option value="5">South Australia — Adelaide, Eyre &amp; coastal south</option>
            <option value="6">New South Wales — south coast &amp; tablelands</option>
            <option value="6">Australian Capital Territory</option>
            <option value="6">Victoria</option>
            <option value="6">Tasmania</option>
          </select>
        </label>
        <p class="region-note">Regional context should change inspection and maintenance decisions, not assign a failure rate to an entire state.</p>
      </div>
    </div>
    <div class="mapwrap">
      <svg class="aumap" viewBox="0 0 540 470" role="img" aria-label="Map of Australia shaded into six exposure regions used to frame inspection decisions"><defs><clipPath id="au-clip"><path d="M374.7 28.6 L387.4 69.4 L407.2 81.8 L415.3 122.5 L424.7 134.9 L452.6 157.1 L468.8 185.5 L495.6 209.0 L497.9 236.2 L503.7 249.8 L495.6 284.4 L482.8 302.9 L475.8 315.2 L472.3 321.4 L463.0 341.2 L461.9 354.8 L450.2 363.4 L432.8 365.9 L420.0 379.5 L408.4 372.1 L402.6 369.6 L386.3 377.0 L364.2 369.6 L354.9 365.9 L342.1 353.5 L334.0 336.2 L328.1 327.6 L318.8 330.1 L310.7 316.5 L297.9 325.1 L278.1 302.9 L272.3 293.0 L240.9 285.6 L216.5 288.1 L182.8 295.5 L158.4 311.5 L135.1 315.2 L107.2 321.4 L88.6 328.8 L56.0 321.4 L54.9 304.1 L64.2 291.8 L61.9 273.2 L50.2 252.2 L36.3 218.9 L38.6 199.1 L44.4 167.0 L61.9 155.9 L75.8 152.2 L96.7 147.2 L122.3 138.6 L138.6 118.8 L154.9 110.2 L157.2 96.6 L171.2 87.9 L188.6 69.4 L207.2 81.8 L224.7 80.5 L232.8 58.3 L238.6 49.6 L252.6 37.3 L259.5 34.8 L279.3 44.7 L297.9 44.7 L309.5 48.4 L296.7 64.5 L299.1 79.3 L310.7 92.9 L337.4 112.6 L354.9 111.4 L363.0 81.8 L365.3 50.9 L374.7 28.6 Z"/><path d="M400.2 399.2 L418.8 404.2 L442.1 401.7 L440.9 421.5 L437.4 430.1 L427.0 435.1 L415.3 432.6 L407.2 419.0 L400.2 405.4 L400.2 399.2 Z"/></clipPath></defs><g clip-path="url(#au-clip)"><path d="M0 0 L540 0 L540 470 L0 470 Z" class="region" data-region="3" fill="#C77D52" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/><path d="M0 0 L540 0 L540 168 L440 172 L405 152 L330 134 L230 134 L170 124 L130 124 L0 124 Z" class="region" data-region="1" fill="#D6A75A" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/><path d="M390 152 L540 165 L540 322 L468 324 L445 300 L425 270 L400 235 L380 200 L370 165 Z" class="region" data-region="2" fill="#7FA8C9" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/><path d="M230 200 L380 200 L400 235 L425 270 L445 300 L468 324 L352 328 L352 305 L300 295 L240 275 L215 240 Z" class="region" data-region="4" fill="#9C8E6A" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/><path d="M0 245 L70 245 L125 275 L150 300 L150 340 L0 340 Z" class="region" data-region="5" fill="#5F8F7A" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/><path d="M295 295 L352 305 L352 350 L295 350 Z" class="region" data-region="5" fill="#5F8F7A" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/><path d="M350 330 L468 322 L540 322 L540 470 L350 470 Z" class="region" data-region="6" fill="#6E7F99" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></g><path d="M374.7 28.6 L387.4 69.4 L407.2 81.8 L415.3 122.5 L424.7 134.9 L452.6 157.1 L468.8 185.5 L495.6 209.0 L497.9 236.2 L503.7 249.8 L495.6 284.4 L482.8 302.9 L475.8 315.2 L472.3 321.4 L463.0 341.2 L461.9 354.8 L450.2 363.4 L432.8 365.9 L420.0 379.5 L408.4 372.1 L402.6 369.6 L386.3 377.0 L364.2 369.6 L354.9 365.9 L342.1 353.5 L334.0 336.2 L328.1 327.6 L318.8 330.1 L310.7 316.5 L297.9 325.1 L278.1 302.9 L272.3 293.0 L240.9 285.6 L216.5 288.1 L182.8 295.5 L158.4 311.5 L135.1 315.2 L107.2 321.4 L88.6 328.8 L56.0 321.4 L54.9 304.1 L64.2 291.8 L61.9 273.2 L50.2 252.2 L36.3 218.9 L38.6 199.1 L44.4 167.0 L61.9 155.9 L75.8 152.2 L96.7 147.2 L122.3 138.6 L138.6 118.8 L154.9 110.2 L157.2 96.6 L171.2 87.9 L188.6 69.4 L207.2 81.8 L224.7 80.5 L232.8 58.3 L238.6 49.6 L252.6 37.3 L259.5 34.8 L279.3 44.7 L297.9 44.7 L309.5 48.4 L296.7 64.5 L299.1 79.3 L310.7 92.9 L337.4 112.6 L354.9 111.4 L363.0 81.8 L365.3 50.9 L374.7 28.6 Z" fill="none" stroke="var(--map-line)" stroke-width="1.5" stroke-linejoin="round"/><path d="M400.2 399.2 L418.8 404.2 L442.1 401.7 L440.9 421.5 L437.4 430.1 L427.0 435.1 L415.3 432.6 L407.2 419.0 L400.2 405.4 L400.2 399.2 Z" fill="none" stroke="var(--map-line)" stroke-width="1.5" stroke-linejoin="round"/><g class="city"><circle cx="241.7" cy="49.8" r="2.6"/><text x="247.7" y="43.8" text-anchor="start">Darwin</text></g><g class="city"><circle cx="413.8" cy="104.9" r="2.6"/><text x="419.8" y="108.9" text-anchor="start">Cairns</text></g><g class="city"><circle cx="497.5" cy="235.3" r="2.6"/><text x="489.5" y="239.3" text-anchor="end">Brisbane</text></g><g class="city"><circle cx="476.6" cy="314.4" r="2.6"/><text x="468.6" y="318.4" text-anchor="end">Sydney</text></g><g class="city"><circle cx="452.6" cy="331.8" r="2.6"/><text x="444.6" y="341.8" text-anchor="end">Canberra</text></g><g class="city"><circle cx="404.5" cy="363.1" r="2.6"/><text x="396.5" y="375.1" text-anchor="end">Melbourne</text></g><g class="city"><circle cx="331.2" cy="327.5" r="2.6"/><text x="337.2" y="321.5" text-anchor="start">Adelaide</text></g><g class="city"><circle cx="69" cy="290.6" r="2.6"/><text x="62" y="294.6" text-anchor="end">Perth</text></g><g class="city"><circle cx="431.8" cy="425.7" r="2.6"/><text x="437.8" y="429.7" text-anchor="start">Hobart</text></g><g class="city"><circle cx="276.7" cy="188.7" r="2.6"/><text x="283.7" y="192.7" text-anchor="start">Alice Springs</text></g><g class="city"><circle cx="104" cy="160" r="2.6"/><text x="111" y="164" text-anchor="start">Pilbara</text></g><g class="zone-pin" data-zone="1" role="button" tabindex="0" aria-label="Zone 1: Monsoonal &amp; humid tropical north"><circle cx="276" cy="97" r="24" fill="#D6A75A" opacity=".28"/><circle cx="276" cy="97" r="14" fill="#D6A75A"/><text x="276" y="102" text-anchor="middle" font-size="14" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">1</text></g><g class="zone-pin" data-zone="2" role="button" tabindex="0" aria-label="Zone 2: Warm humid eastern seaboard"><circle cx="430" cy="215" r="24" fill="#7FA8C9" opacity=".28"/><circle cx="430" cy="215" r="14" fill="#7FA8C9"/><text x="430" y="220" text-anchor="middle" font-size="14" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">2</text></g><g class="zone-pin" data-zone="3" role="button" tabindex="0" aria-label="Zone 3: Arid interior &amp; north-west"><circle cx="178" cy="164" r="24" fill="#C77D52" opacity=".28"/><circle cx="178" cy="164" r="14" fill="#C77D52"/><text x="178" y="169" text-anchor="middle" font-size="14" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">3</text></g><g class="zone-pin" data-zone="4" role="button" tabindex="0" aria-label="Zone 4: Semi-arid transition &amp; inland margins"><circle cx="300" cy="250" r="24" fill="#9C8E6A" opacity=".28"/><circle cx="300" cy="250" r="14" fill="#9C8E6A"/><text x="300" y="255" text-anchor="middle" font-size="14" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">4</text></g><g class="zone-pin" data-zone="5" role="button" tabindex="0" aria-label="Zone 5: Mediterranean-type south-west &amp; southern pockets"><circle cx="98" cy="300" r="24" fill="#5F8F7A" opacity=".28"/><circle cx="98" cy="300" r="14" fill="#5F8F7A"/><text x="98" y="305" text-anchor="middle" font-size="14" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">5</text></g><g class="zone-pin" data-zone="6" role="button" tabindex="0" aria-label="Zone 6: Temperate south-east &amp; Tasmania"><circle cx="383" cy="340" r="24" fill="#6E7F99" opacity=".28"/><circle cx="383" cy="340" r="14" fill="#6E7F99"/><text x="383" y="345" text-anchor="middle" font-size="14" font-weight="700" fill="#fff" font-family="Figtree,sans-serif">6</text></g></svg>
      <ol class="zones"><li class="zone-pin" data-zone="1" role="button" tabindex="0"><span class="dot" style="background:#D6A75A">1</span><div><b>Monsoonal &amp; humid tropical north</b><span>Heat, humidity, wet season, vegetation</span></div></li><li class="zone-pin" data-zone="2" role="button" tabindex="0"><span class="dot" style="background:#7FA8C9">2</span><div><b>Warm humid eastern seaboard</b><span>Humidity, dew, coastal deposits, shading</span></div></li><li class="zone-pin" data-zone="3" role="button" tabindex="0"><span class="dot" style="background:#C77D52">3</span><div><b>Arid interior &amp; north-west</b><span>Heat, diurnal swing, dust, remoteness</span></div></li><li class="zone-pin" data-zone="4" role="button" tabindex="0"><span class="dot" style="background:#9C8E6A">4</span><div><b>Semi-arid transition &amp; inland margins</b><span>Dry spells, farm dust, birds, mismatch</span></div></li><li class="zone-pin" data-zone="5" role="button" tabindex="0"><span class="dot" style="background:#5F8F7A">5</span><div><b>Mediterranean-type south-west &amp; southern pockets</b><span>Dry summers, wet winters, salt, smoke</span></div></li><li class="zone-pin" data-zone="6" role="button" tabindex="0"><span class="dot" style="background:#6E7F99">6</span><div><b>Temperate south-east &amp; Tasmania</b><span>Cool, wet, dew, frost, low sun angles</span></div></li></ol>
    </div>
    <div class="zone-panel" id="zone-panel" hidden>
      <div class="zp-head"><span class="dot" id="zp-dot"></span><div><p class="eyebrow" id="zp-eyebrow">Zone</p><h3 id="zp-title"></h3><p id="zp-regions" class="zp-regions"></p></div></div>
      <div class="zp-grid zp-grid-3">
        <div><b>Exposure</b><p id="zp-exposure"></p></div>
        <div><b>Mechanism to separate</b><p id="zp-mechanism"></p></div>
        <div><b>Diagnose → act</b><p id="zp-act"></p></div>
      </div>
      <p class="zp-note">Generalised exposure and diagnostic framework, not a measured failure-rate map. Local exposure, module construction and operating conditions require site-level verification. Sources: Australian Bureau of Meteorology; IEA PVPS Task 13; selected PV reliability and terahertz inspection studies.</p>
    </div>
  </div>
</section>

<section class="band" id="who">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Capabilities</p>
      <h2 class="h2 h2-wide">What we do at each stage of a solar asset's life</h2>
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
    <p class="eyebrow">Technologies</p>
    <h1>Grounded in physics. Accountable to evidence.</h1>
    <p class="lede">Our hybrid digital twin combines physical modelling with real-world observations to track how assets evolve across space and time. It quantifies performance impacts, evaluates intervention scenarios and tests predictions against measured outcomes.</p>
  </div>
</section>

<section class="band band-tint" id="chain">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The evidence chain</p>
      <h2 class="h2 h2-wide">From material origins to measured outcomes.</h2>
      <p class="lede">A continuous evidence chain connects physical conditions, asset performance and verified results, keeping predictions traceable, testable and open to refinement.</p>
    </div>
    <div class="chainwrap"><svg class="chainloop" viewBox="0 0 900 560" role="img" aria-label="The evidence chain as a loop: material and process context, environmental exposure, condition evolution, performance impact, outcome validation, feeding back to the start">
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>
<path d="M494.8 95.5 A185 185 0 0 1 606.9 177.0" class="arc" marker-end="url(#arrow)"/>
<path d="M634.5 262.1 A185 185 0 0 1 591.7 393.9" class="arc" marker-end="url(#arrow)"/>
<path d="M519.3 446.5 A185 185 0 0 1 380.7 446.5" class="arc" marker-end="url(#arrow)"/>
<path d="M308.3 393.9 A185 185 0 0 1 265.5 262.1" class="arc" marker-end="url(#arrow)"/>
<path d="M293.1 177.0 A185 185 0 0 1 405.2 95.5" class="arc arc-back" marker-end="url(#arrow)"/>
<g class="node"><circle cx="450.0" cy="90.0" r="40"/><g transform="translate(450.0 90.0)" class="nico"><path d="M-14 -4l14-7 14 7-14 7z"/><path d="M-14 3l14 7 14-7"/><path d="M-14 10l14 7 14-7"/></g><text x="450.0" y="149.0" text-anchor="middle" class="num">01</text><text x="450.0" y="20.0" text-anchor="middle" class="lbl">Material &amp; process context</text><text x="450.0" y="40.0" text-anchor="middle" class="sub">Bill of materials · batch · lamination</text></g>
<g class="node"><circle cx="625.9" cy="217.8" r="40"/><g transform="translate(625.9 217.8)" class="nico"><circle cx="-2" cy="-2" r="7"/><path d="M-2 -16v4M-2 8v4M-16 -2h4M8 -2h4M-12 -12l3 3M5 5l3 3M-12 8l3-3M5 -9l3-3"/></g><text x="625.9" y="169.8" text-anchor="middle" class="num">02</text><text x="684.9" y="200.7" text-anchor="start" class="lbl">Environmental exposure</text><text x="684.9" y="220.7" text-anchor="start" class="sub">Climate zone · terrain · microclimate</text></g>
<g class="node"><circle cx="558.7" cy="424.7" r="40"/><g transform="translate(558.7 424.7)" class="nico"><path d="M-16 4h7l4-12 6 20 4-8h11"/></g><text x="558.7" y="376.7" text-anchor="middle" class="num">03</text><text x="595.2" y="476.8" text-anchor="start" class="lbl">Condition evolution</text><text x="595.2" y="496.8" text-anchor="start" class="sub">Repeat inspection · subsurface evidence</text></g>
<g class="node"><circle cx="341.3" cy="424.7" r="40"/><g transform="translate(341.3 424.7)" class="nico"><path d="M-14 14h28"/><rect x="-12" y="2" width="6" height="10"/><rect x="-3" y="-5" width="6" height="17"/><rect x="6" y="-12" width="6" height="24"/></g><text x="341.3" y="376.7" text-anchor="middle" class="num">04</text><text x="304.8" y="476.8" text-anchor="end" class="lbl">Performance impact</text><text x="304.8" y="496.8" text-anchor="end" class="sub">Energy loss · weather-normalised</text></g>
<g class="node"><circle cx="274.1" cy="217.8" r="40"/><g transform="translate(274.1 217.8)" class="nico"><circle cx="0" cy="0" r="15"/><path d="M-7 0l5 5 9-10"/></g><text x="274.1" y="169.8" text-anchor="middle" class="num">05</text><text x="215.1" y="200.7" text-anchor="end" class="lbl">Outcome validation</text><text x="215.1" y="220.7" text-anchor="end" class="sub">Measured cost · generation response</text></g>
<text x="450" y="265" text-anchor="middle" class="centre">Validated outcomes</text>
<text x="450" y="291" text-anchor="middle" class="centre2">inform future maintenance,</text>
<text x="450" y="313" text-anchor="middle" class="centre2">design and manufacturing</text>
</svg></div>
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
      <p class="eyebrow">Decision-making</p>
      <h2 class="h2">Where every module is, what it is made of, and how it is behaving</h2>
      <p class="lede">Each module is linked to the place it lives. Over time the database becomes a map of how solar hardware ages across Australia's climate zones, and a guide to what to build where. <a href="index.html#regions">Explore the regional map</a>.</p>
    </div>

    <div class="hubwrap">
      <div class="hubscroll"><svg class="hub" viewBox="0 0 900 460" role="img" aria-label="Four input streams flow into one database record per module; two outputs are drawn from it">
<defs><marker id="harrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>
<text x="146.0" y="20" text-anchor="middle" class="hhead">Flows in</text>
<text x="746.0" y="20" text-anchor="middle" class="hhead hhead-out">Comes out</text>
<path class="hlink" data-h="record" d="M282 62 H316 V230 H404" marker-end="url(#harrow)"/>
<path class="hlink" data-h="environment" d="M282 162 H316 V230 H404" marker-end="url(#harrow)"/>
<path class="hlink" data-h="performance" d="M282 262 H316 V230 H404" marker-end="url(#harrow)"/>
<path class="hlink" data-h="zones" d="M282 362 H316 V230 H404" marker-end="url(#harrow)"/>
<path class="hlink hout" data-h="guidance" d="M534 230 H574 V150 H608" marker-end="url(#harrow)"/>
<path class="hlink hout" data-h="map" d="M534 230 H574 V310 H608" marker-end="url(#harrow)"/>
<g class="hnode" data-h="record" role="button" tabindex="0" aria-label="Module record"><rect x="10" y="30.0" width="272" height="64" rx="14"/><g transform="translate(42 62)" class="hicon"><rect x="-12" y="-9" width="24" height="18" rx="3"/><path d="M-6 -2h6M-6 3h12"/></g><text x="72" y="58" class="hlabel">Module record</text><text x="72" y="77" class="hsub">ID · materials · batch · history</text></g>
<g class="hnode" data-h="environment" role="button" tabindex="0" aria-label="Environment"><rect x="10" y="130.0" width="272" height="64" rx="14"/><g transform="translate(42 162)" class="hicon"><circle cx="0" cy="-4" r="4.5"/><path d="M-12 10c3-7 7-10 12-10s9 3 12 10"/></g><text x="72" y="158" class="hlabel">Environment</text><text x="72" y="177" class="hsub">Climate · terrain · microclimate</text></g>
<g class="hnode" data-h="performance" role="button" tabindex="0" aria-label="Performance"><rect x="10" y="230.0" width="272" height="64" rx="14"/><g transform="translate(42 262)" class="hicon"><path d="M-12 9l6-8 5 4 5-9 8 6"/></g><text x="72" y="258" class="hlabel">Performance</text><text x="72" y="277" class="hsub">SCADA · strings · weather-normalised</text></g>
<g class="hnode" data-h="zones" role="button" tabindex="0" aria-label="Six climate zones"><rect x="10" y="330.0" width="272" height="64" rx="14"/><g transform="translate(42 362)" class="hicon"><circle cx="0" cy="0" r="11"/><path d="M-11 0h22M0 -11c-5 5-5 17 0 22M0 -11c5 5 5 17 0 22"/></g><text x="72" y="358" class="hlabel">Six climate zones</text><text x="72" y="377" class="hsub">Sites stratified by exposure</text></g>
<g class="hnode hnode-out" data-h="guidance" role="button" tabindex="0" aria-label="Deployment guidance"><rect x="610" y="118.0" width="272" height="64" rx="14"/><g transform="translate(642 150)" class="hicon"><path d="M-10 10l6-16 5 9 8-3-7 10z"/></g><text x="672" y="146" class="hlabel">Deployment guidance</text><text x="672" y="165" class="hsub">What to build where</text></g>
<g class="hnode hnode-out" data-h="map" role="button" tabindex="0" aria-label="Degradation map"><rect x="610" y="278.0" width="272" height="64" rx="14"/><g transform="translate(642 310)" class="hicon"><path d="M-12 -7l8-3 8 3 8-3v16l-8 3-8-3-8 3z M-4 -10v16M4 -7v16"/></g><text x="672" y="306" class="hlabel">Degradation map</text><text x="672" y="325" class="hsub">Rates by material · batch · zone</text></g>
<g class="hcore" role="button" tabindex="0" data-h="core" aria-label="The database">
    <rect x="406" y="156" width="128" height="150" rx="16" fill="#fff" stroke="none"/>
    <ellipse cx="470" cy="184" rx="44" ry="14"/><path d="M426 184v24c0 8 20 14 44 14s44-6 44-14v-24c0 8-20 14-44 14s-44-6-44-14z"/><path d="M426 208v24c0 8 20 14 44 14s44-6 44-14v-24c0 8-20 14-44 14s-44-6-44-14z" class="hcore-low"/>
    <text x="470" y="272" text-anchor="middle" class="hlabel">One record</text><text x="470" y="291" text-anchor="middle" class="hlabel">per module</text>
  </g>
</svg>
      <div class="hpop" id="hpanel" hidden>
        <button type="button" class="hpop-close" id="hp-close" aria-label="Close">×</button>
        <p class="eyebrow" id="hp-eyebrow">The database</p>
        <h3 id="hp-title">One record per module</h3>
        <p class="hp-what" id="hp-what"></p>
      </div></div>
      <p class="hhint">Click any box to see what it holds. Four streams flow in and attach to the same module; two things come out of it.</p>
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
        <div class="photo"><img src="assets/harrison.jpg" alt="Harrison Su" width="800" height="800" loading="lazy"></div>
        <h3>Harrison Su</h3>
        <p class="role">Co-founder</p>
        <p>PhD in Materials Science and Engineering, and Director of Caelvox Technologies, developing advanced sensing architecture and automated inspection systems. His research spans energy materials, terahertz imaging and advanced characterisation, including collaborations with the Australian Synchrotron and the Australian Centre for Neutron Scattering. Focused on translating materials science into validated diagnostics, industrial applications and asset intelligence.</p>
      </div>
      <div class="person">
        <div class="photo"><img src="assets/laurens.jpg" alt="Laurens Willems van Beveren" width="800" height="800" loading="lazy"></div>
        <h3>Laurens Willems van Beveren</h3>
        <p class="role">Co-founder</p>
        <p>PhD in Applied Physics and Director of Australian Vacuum Services and Australian Drone Surveys. Former Experimental Scientist at Australia's National Measurement Institute, with extensive experience in precision instrumentation, measurement science and systems engineering. Combines scientific instrumentation expertise with CASA-credentialed drone operations, supporting reliable sensor integration, field inspection and engineering deployment.</p>
      </div>
      <div class="person">
        <div class="photo"><img src="assets/sohan.jpg" alt="Sohan Domingo" width="800" height="800" loading="lazy"></div>
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
  "technology.html": ("Technologies — Metrifield Dynamics", "Tiered RGB, thermal and terahertz sensing, a multimodal asset record and a hybrid physics-and-data digital twin that predicts the most economical action.", technology_body),
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
(ROOT/"_headers").write_text("/*\n  Cache-Control: public, max-age=0, must-revalidate\n/assets/*\n  Cache-Control: public, max-age=604800\n/styles.css\n  Cache-Control: public, max-age=31536000, immutable\n")
(ROOT/"_redirects").write_text("https://metrifield.com/* https://www.metrifield.com/:splat 301\n/solutions.html /capabilities.html 301\n/solutions /capabilities.html 301\n")
print("built", ", ".join(PAGES))
