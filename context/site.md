Owner: mailanilkumar
Why: Defines what the Transform Loop website is for, what AI-native means here, the decisions behind it, and the checks it must keep passing.
Covers: index.html, build-check/index.html
Status: live content, two open items (see bottom)

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
- Single static file, no tracking, no form that collects data. Reason: nothing to leak, free hosting, nobody in the middle of visitors' information.

# Golden checks (the health gate runs these)
1. The headline reads: Get more from your AI budget, with code you can trust.
2. There are exactly five gates (Write, Retrieval, Use, Health, Freshness).
3. Every Book a call button leads to the real booking link (see open items).
4. No performance numbers, no returns, no client names, no employer references anywhere.
5. The page works at phone width with no sideways scrolling (checked by hand for now).

# Open items
- Booking link is still the placeholder https://calendly.com/. Replace with the real link.
- Headshot is still the placeholder initials AC. Replace with a real photo.
- Domain: transformloop.ai is pointed at this site (DNS at the registrar, custom domain and HTTPS in GitHub Pages). Done 2026-11-22.
