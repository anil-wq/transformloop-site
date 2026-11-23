// Transform Loop encrypted-send endpoint (Cloudflare Worker).
// It never sees readable data: the browser encrypts first. It only checks the bot test,
// limits size, and files the encrypted blob as an issue in the private repo.
// Secrets (set in Cloudflare, never in code): TURNSTILE_SECRET, GITHUB_TOKEN.
const ORIGIN = 'https://transformloop.ai';
const REPO = 'mailanilkumar/transformloop-company';
const MAX_BYTES = 30000;

function cors(extra) {
  return Object.assign({
    'Access-Control-Allow-Origin': ORIGIN,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'content-type',
    'Vary': 'Origin'
  }, extra || {});
}
function out(status, obj) {
  return new Response(JSON.stringify(obj), { status: status, headers: cors({ 'content-type': 'application/json' }) });
}

export default {
  async fetch(req, env) {
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors() });
    if (req.method !== 'POST') return out(405, { ok: false });
    if (req.headers.get('Origin') !== ORIGIN) return out(403, { ok: false });

    const text = await req.text();
    if (text.length > MAX_BYTES) return out(413, { ok: false });
    let body;
    try { body = JSON.parse(text); } catch (e) { return out(400, { ok: false }); }
    const b = body && body.blob;
    if (!b || typeof b.k !== 'string' || typeof b.iv !== 'string' || typeof b.ct !== 'string' || b.v !== 1) return out(400, { ok: false });
    if (typeof body.token !== 'string' || !body.token) return out(400, { ok: false });

    const form = new FormData();
    form.append('secret', env.TURNSTILE_SECRET);
    form.append('response', body.token);
    const ip = req.headers.get('CF-Connecting-IP');
    if (ip) form.append('remoteip', ip);
    const v = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
    const vr = await v.json();
    if (!vr.success) return out(403, { ok: false });

    const blob = JSON.stringify({ v: 1, k: b.k, iv: b.iv, ct: b.ct });
    const gh = await fetch('https://api.github.com/repos/' + REPO + '/issues', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + env.GITHUB_TOKEN,
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'transformloop-worker',
        'content-type': 'application/json'
      },
      body: JSON.stringify({
        title: 'Encrypted submission ' + new Date().toISOString(),
        body: blob,
        labels: ['submission']
      })
    });
    if (!gh.ok) return out(502, { ok: false });
    return out(200, { ok: true });
  }
};
