Owner: mailanilkumar
Why: Defines what the Transform Loop website is for, what AI-native means here, the decisions behind it, and the checks it must keep passing.
Covers: index.html, build-check/index.html, worker/worker.js, build-check-reader/index.html
Status: live content, Build Check live at /build-check/, open items at bottom

# What AI-native means here (standing rule)

transformloop.ai is AI-native from day one. Nothing goes into the code without context. The context itself goes through every required gate, including the retrieval gate:
- Write gate: every context file names an Owner, the Why and what it Covers. Checked on every change.
- Retrieval gate: every code file is covered by a context file, and agents retrieve that context through the MCP context server before they change the code. Checked on every change.
- Use gate: a change to code must update the context that covers it in the same change, and must carry a receipt of the context the agent retrieved. Checked on every change.
- Freshness gate: the receipt must name the version of the context that was current before the change. A stale version fails. Checked on every change.
- Health gate: golden checks (below) run against the live site once in a while, on a schedule, not on every change. When one fails, the context or the site gets fixed.

These are enforced by GitHub workflows in .github/workflows: context-gate.yml (every change) and health.yml (scheduled).

# How agents build here (standing rule)

- The agent that builds the code is the same agent that retrieves the context. It never works from memory or from the whole repository.
- Retrieval goes through an MCP context server. The agent asks for the context covering the files it is about to touch and gets back only that context, with the version (hash) of each context file.
- Every retrieval is recorded in a receipt. The details of what was retrieved are checked again at the use gate.
- Status: built. The server, the receipt and the checks are described in context/agents.md.

# Feature: one-page site (index.html)

Why it exists: it is the front door for Transform Loop, a consultancy that helps software teams get more from their AI budget with code they can trust. A visitor should understand the offer in one screen and be able to book a call.

Decisions and reasons:
- Layered information. The headline, the three outcomes, the Book a call button, the short bio and the proof headline are always visible. Details sit on flip tiles (five gates, four services, four method steps). Reason: simple at a glance, depth on demand.
- Flip tiles flip on hover with a mouse and on tap or Enter on touch and keyboard. Reason: works on phones and without a mouse.
- Proof section describes how the trading platform was built (process only). It never shows strategy, trades, returns or performance numbers. Reason: that is private and not the point.
- No client is named on the site without that client's written approval.
- Nothing on the site may relate to the business of any current or former employer.
- Single static file, no tracking, no form that collects data on the home page. Reason: nothing to leak, free hosting, nobody in the middle of visitors' information. The one exception is the opt-in encrypted send in the Build Check (see Open items): nothing leaves the browser unless the visitor chooses to send.

# Golden checks (the health gate runs these)
1. The headline reads: Get more from your AI budget, with code you can trust.
2. There are exactly five gates (Write, Retrieval, Use, Health, Freshness).
3. Every call-to-action button leads to a real destination (LinkedIn for now, see open items). No placeholder links.
4. No performance numbers, no returns, no client names, no employer references anywhere.
5. The page works at phone width with no sideways scrolling (checked by hand for now).

# Open items
- No booking link yet: the call-to-action sends people to LinkedIn. Replace with a booking link when one exists.
- No headshot: the About section has no photo for now. Add one when available.
- Domain: transformloop.ai is pointed at this site (DNS at the registrar, custom domain and HTTPS in GitHub Pages). Done 2026-11-22.
- AI Build Check lives at /build-check/ (build-check/index.html). Answers stay in the visitor's browser and nothing is sent anywhere. No email capture yet; it arrives with the email platform. Added 2026-11-22.
- Build Check comparison takes up to four pasted codes (you plus up to three colleagues, for example CEO, CTO and COO), one per line. It shows every person side by side, flags areas where views differ (different status, or confidence 50 points apart), lists those first, and asks one question per flagged area: what evidence would convince all of us? Same role twice is shown as CTO and CTO 2. Everything still happens in the browser. Added 2026-11-22.
- Encrypted send (decided by Anil 2026-11-22; live since 2026-11-22: Worker tl-send.anil-94f.workers.dev, secrets set by Anil in Cloudflare): after results, a visitor may choose to send their answers, company name and work email to Transform Loop. The browser encrypts everything with a public key, so only Anil's private key can read it. A Cloudflare Worker (worker/worker.js) checks a Turnstile bot check, limits size, and files the encrypted blob as an issue in the private repo. Nothing is readable in transit or at rest without the private key. build-check-reader/index.html decrypts in the browser from a pasted key and groups submissions by company. No logins. The private key is held only by Anil and is never stored in any repo. Worker secrets (Turnstile secret, GitHub token) are entered by Anil, never by the agent.
- Encrypted send details: browser uses AES-GCM for the data and wraps the key with RSA-OAEP using the public key embedded in build-check/index.html; the payload holds company, work email, role, results code and time. The Worker stores blobs as issues labelled submission in the private repo. build-check-reader/index.html (was reader/) is noindex and decrypts from a key file Anil chooses. Round trip tested with Node WebCrypto 2026-11-22.
- Reader shows each submission as a table (area, confidence, evidence answers, blockers) decoded from the results code, grouped by company. Fixed 2026-11-22 after the first test showed the raw code.
- Reader moved to /build-check-reader/ (2026-11-22) and gained a Download button: after decrypting, it saves one readable markdown file with every company, person and area. Anil attaches that file in chat so the agent can file it per company and analyse. The reader still never uploads anything.
