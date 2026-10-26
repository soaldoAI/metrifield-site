// Cloudflare Pages Function: POST /api/chat
// Retrieval-grounded site assistant on Workers AI (binding: AI).
// Knowledge chunks are compiled from /knowledge/*.md by build.py into ./_knowledge.js.
import { CHUNKS } from "./_knowledge.js";

// Tried in order; the first that responds is used (guards against model retirements).
const MODELS = ["@cf/meta/llama-3.3-70b-instruct-fp8-fast", "@cf/qwen/qwen3-30b-a3b-fp8", "@cf/zai-org/glm-4.7-flash", "@cf/meta/llama-4-scout-17b-16e-instruct"];
const TOP_K = 5;
const MIN_SCORE = 3.5;          // below this: refuse without calling the model
const FALLBACK = "That's outside what I can help with here — I only answer questions about Metrifield Dynamics and our solar asset services. For anything else, email info@metrifield.com or use the Contact page.";

const STOP = new Set("a an and are as at be by do does for from how i in is it its of on or that the this to we what when where which who why with you your can our us me my about tell more please".split(" "));
const tok = (s) => String(s).toLowerCase().replace(/[^a-z0-9µ\-]+/g, " ").split(" ").filter((w) => w.length > 1 && !STOP.has(w));
const stem = (w) => w.replace(/(ings?|ers?|ies|ied|es|s|ly|tion|tions|al)$/,"");
const SYN = { contact: ["contact","email","phone","reach"], email: ["contact","email"], phone: ["contact","phone"], call: ["contact","phone"], customer: ["customer","client","work with","owner","operator"], client: ["customer","client"], twin: ["twin","st-twin","digital"], terahertz: ["terahertz","thz"], thz: ["terahertz","thz"], drone: ["drone","uav","survey"], price: ["price","cost","pricing","quote"], cost: ["price","cost","pricing","quote"], founder: ["founder","founded","team","who"], ceo: ["founder","founded","team"], robot: ["robot","crawling","crawler"], region: ["region","climate","zone","australia"], ai: ["ai","edge","model","vision"] };

// Pre-tokenise chunks once per isolate
const INDEX = CHUNKS.map((c) => {
  const words = tok(c.title + " " + c.title + " " + c.text).map(stem);
  const tf = new Map(); for (const w of words) tf.set(w, (tf.get(w) || 0) + 1);
  return { c, tf, len: words.length, title: new Set(tok(c.title).map(stem)) };
});
const DF = new Map(); for (const e of INDEX) for (const w of e.tf.keys()) DF.set(w, (DF.get(w) || 0) + 1);
const OVERVIEW = ["Who we are","What does Metrifield do in one sentence?","How is this different from a normal drone thermal inspection?","Target customers","Mission"].map((t) => CHUNKS.find((c) => c.title.endsWith("— " + t))).filter(Boolean);
const N = INDEX.length, AVG = INDEX.reduce((a, e) => a + e.len, 0) / N;
const idf = (w) => Math.log(1 + (N - (DF.get(w) || 0) + 0.5) / ((DF.get(w) || 0) + 0.5));

function retrieve(q) {
  let terms = tok(q); terms = terms.flatMap((w) => SYN[w] ? SYN[w] : [w]).map(stem);
  const uniq = [...new Set(terms)];
  const scored = INDEX.map((e) => {
    let s = 0;
    for (const w of uniq) { const f = e.tf.get(w) || 0; if (!f) continue; s += idf(w) * (f * 2.2) / (f + 1.2 * (0.25 + 0.75 * e.len / AVG)); if (e.title.has(w)) s += 1.6; }
    return { s, c: e.c };
  }).sort((a, b) => b.s - a.s);
  return scored.slice(0, TOP_K).filter((x) => x.s > 0);
}

const SYSTEM = `You are the assistant on metrifield.com, the website of Metrifield Dynamics Pty Ltd (Sydney, Australia). Answer in Australian English, plainly, in 2–5 sentences. Use ONLY the reference passages provided in the user message. If the passages do not contain the answer, say you don't have that information and suggest emailing info@metrifield.com. Never invent prices, dates, customers, certifications or capabilities. Do not discuss grants, government funding or funding applications. Do not mention "passages" or "context" — just answer. If asked your name, say you are the Metrifield assistant, an automated helper.`;

const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });

const UNKNOWN_RE = /don'?t have (that|this|the) information|do not have (that|this|the) information|not (something )?(i|we) (can|have)|outside what i can help/i;

async function logChat(env, ctx, rec) {
  if (!env.SHEET_WEBHOOK_URL) return;
  const p = fetch(env.SHEET_WEBHOOK_URL, { method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ kind: "chat", secret: env.SHEET_WEBHOOK_SECRET || "", ...rec }) }).catch(() => {});
  ctx && ctx.waitUntil ? ctx.waitUntil(p) : await p;
}

async function flagUnanswered(env, ctx, rec) {
  if (!env.RESEND_API_KEY) return;
  const esc = (x) => String(x || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const p = fetch("https://api.resend.com/emails", { method: "POST",
    headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, "content-type": "application/json" },
    body: JSON.stringify({ from: "Metrifield website <noreply@metrifield.com>", to: ["info@metrifield.com"],
      subject: `Website chat: unanswered question — "${String(rec.question).slice(0, 60)}"`,
      text: `A visitor asked the site assistant something it couldn't answer.\n\nPage: ${rec.page}\nQuestion: ${rec.question}\nAssistant replied: ${rec.answer}\n\nIf this is a real gap, add it to knowledge/06-faq.md in the site repo. Logged in the "Chat log" tab of the Website Enquiries sheet.`,
      html: `<p>A visitor asked the site assistant something it couldn't answer.</p><p><b>Page:</b> ${esc(rec.page)}<br><b>Question:</b> ${esc(rec.question)}<br><b>Assistant replied:</b> ${esc(rec.answer)}</p><p style="color:#666">If this is a real gap, add it to <code>knowledge/06-faq.md</code> in the site repo. Logged in the "Chat log" tab of the Website Enquiries sheet.</p>` }) }).catch(() => {});
  ctx && ctx.waitUntil ? ctx.waitUntil(p) : await p;
}

export async function onRequestPost(ctx) {
  const { request, env } = ctx;
  if (!env.AI) return json(500, { ok: false, error: "Assistant not configured." });
  let body; try { body = await request.json(); } catch { return json(400, { ok: false, error: "Bad request" }); }
  const history = (Array.isArray(body.messages) ? body.messages : []).filter((m) => m && (m.role === "user" || m.role === "assistant") && m.content).slice(-8);
  const last = [...history].reverse().find((m) => m.role === "user");
  if (!last) return json(400, { ok: false, error: "Empty message" });
  const q = String(last.content).slice(0, 500);
  const page = String(body.page || request.headers.get("referer") || "").slice(0, 200);

  // Greetings / meta without retrieval
  if (/^\s*(hi|hello|hey|g'day|good (morning|afternoon|evening)|thanks?|thank you|cheers)\b[\s!.?]*$/i.test(q)) {
    return json(200, { ok: true, reply: "Hi — I can answer questions about Metrifield Dynamics: what we do, our drone and terahertz inspection services, the digital twin, who we work with and how to get started. What would you like to know?" });
  }

  if (/\b(your name|who are you|are you (a )?(bot|human|person|real)|what are you)\b/i.test(q)) {
    return json(200, { ok: true, reply: "I'm the Metrifield assistant — an automated helper that answers from the content on metrifield.com, not a person. Ask me about our services, the technology or how to get started; for anything specific to your site, use the Contact page." });
  }

  // Use previous user turn as extra retrieval context for follow-ups like "tell me more"
  const prevUser = history.filter((m) => m.role === "user").slice(-2, -1)[0];
  let hits = retrieve(q.split(/\s+/).length <= 4 && prevUser ? q + " " + prevUser.content : q);
  // Generic "about the company" questions: the word "Metrifield" is in every passage so it scores ~0; route to the overview chunks.
  if ((!hits.length || hits[0].s < MIN_SCORE) && /metrifield|your (company|business|team|services?)|what (do|does|can) you (do|offer|provide)|about you\b|who are you/i.test(q)) {
    hits = OVERVIEW.map((c) => ({ s: MIN_SCORE, c }));
  }
  if (!hits.length || hits[0].s < MIN_SCORE) {
    await logChat(env, ctx, { page, question: q, answer: FALLBACK, status: "off-topic", sources: "", model: "" });
    return json(200, { ok: true, reply: FALLBACK, gated: true });
  }

  const context = hits.map((h, i) => `[${i + 1}] ${h.c.title}\n${h.c.text}`).join("\n\n");
  const messages = [{ role: "system", content: SYSTEM }];
  for (const m of history.slice(0, -1)) messages.push({ role: m.role, content: String(m.content).slice(0, 1500) });
  messages.push({ role: "user", content: `Reference passages:\n\n${context}\n\nQuestion: ${q}` });

  let lastErr = null;
  for (const model of MODELS) {
    try {
      const r = await env.AI.run(model, { messages, max_tokens: 350, temperature: 0.2 });
      let reply = ((r && (r.response || (r.result && r.result.response))) || "").trim();
      reply = reply.replace(/<think>[\s\S]*?<\/think>\s*/g, "").trim(); // strip reasoning blocks some models emit
      if (!reply) continue;
      const unknown = UNKNOWN_RE.test(reply);
      const rec = { page, question: q, answer: reply, status: unknown ? "unknown" : "answered", sources: hits.map((h) => h.c.title).join(" | "), model };
      await logChat(env, ctx, rec);
      if (unknown) await flagUnanswered(env, ctx, rec);
      return json(200, { ok: true, reply, sources: hits.map((h) => h.c.title), model, unknown });
    } catch (e) { lastErr = e; console.error("AI error", model, e && e.message); }
  }
  return json(200, { ok: false, error: "The assistant is unavailable right now. Please email info@metrifield.com.", detail: String(lastErr && lastErr.message || lastErr).slice(0, 300) });
}

export const onRequest = ({ request }) => request.method === "POST" ? undefined : new Response("Method not allowed", { status: 405 });
