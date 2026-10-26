// Cloudflare Pages Function: POST /api/contact
// Sends the enquiry to info@metrifield.com via Resend. Requires env RESEND_API_KEY.
const TO = [
  "info@metrifield.com",
  "sohan.domingo@metrifield.com",
  "sohan.domingo@edgegenix.com",
  "laurens.willemsvanbeveren@metrifield.com",
  "laurenswillemsvanbeveren@gmail.com",
  "harrison.su@metrifield.com",
  "harrisons@caelvox.com.au",
];
const FROM = "Metrifield website <noreply@metrifield.com>";

const esc = (s) => String(s || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });

export async function onRequestPost({ request, env }) {
  let d;
  try { d = await request.json(); } catch { return json(400, { ok: false, error: "Bad request" }); }

  if (d.website) return json(200, { ok: true }); // honeypot filled by a bot: pretend success

  const name = String(d.name || "").trim().slice(0, 200);
  const org = String(d.org || "").trim().slice(0, 200);
  const email = String(d.email || "").trim().slice(0, 200);
  const type = String(d.type || "").trim().slice(0, 100);
  const msg = String(d.msg || "").trim().slice(0, 5000);

  if (!name || !msg || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json(400, { ok: false, error: "Please fill in your name, a valid email and a message." });
  }
  if (!env.RESEND_API_KEY) return json(500, { ok: false, error: "Mail service not configured." });

  const subject = `Website enquiry — ${name}${org ? " (" + org + ")" : ""}`;
  const text = `Name: ${name}\nOrganisation: ${org}\nEmail: ${email}\nI am a: ${type}\n\n${msg}`;
  const html = `<p><b>Name:</b> ${esc(name)}<br><b>Organisation:</b> ${esc(org)}<br><b>Email:</b> <a href="mailto:${esc(email)}">${esc(email)}</a><br><b>I am a:</b> ${esc(type)}</p><p style="white-space:pre-wrap">${esc(msg)}</p>`;

  // Log to Google Sheet (optional; Apps Script web app URL in env, secret optional)
  if (env.SHEET_WEBHOOK_URL) {
    try {
      await fetch(env.SHEET_WEBHOOK_URL, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ secret: env.SHEET_WEBHOOK_SECRET || "", name, org, email, type, msg, source: request.headers.get("referer") || "metrifield.com" }),
      });
    } catch (e) { /* sheet logging is best-effort; email still goes */ }
  }

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, "content-type": "application/json" },
    body: JSON.stringify({ from: FROM, to: TO, reply_to: email, subject, text, html }),
  });
  if (!r.ok) return json(502, { ok: false, error: "Could not send right now. Please email us directly." });
  return json(200, { ok: true });
}

export const onRequest = ({ request }) =>
  request.method === "POST" ? undefined : new Response("Method not allowed", { status: 405 });
