Owner: Anil Chintalacheruvu
Why: Defines what the Transform Loop website (index.html) is for, the decisions behind it, and the checks it must keep passing.
Status: live content, two open items (see bottom)

# Standing rule

transformloop.ai is AI-native from day one. Nothing goes into the code without context. Every change to site code must update a file in context/ in the same change, and every context file must name an Owner and the Why. This is enforced by the Context gate workflow, which fails any change that breaks it.

# Feature: one-page site (index.html)

Why it exists: it is the front door for Transform Loop, a consultancy that helps software teams get more from their AI budget with code they can trust. A visitor should understand the offer in one screen and be able to book a call.

Decisions and reasons:
- Layered information. The headline, the three outcomes, the Book a call button, the short bio and the proof headline are always visible. Details sit on flip tiles (five gates, four services, four method steps). Reason: simple at a glance, depth on demand.
- Flip tiles flip on hover with a mouse and on tap or Enter on touch and keyboard. Reason: works on phones and without a mouse.
- Proof section describes how the trading platform was built (process only). It never shows strategy, trades, returns or performance numbers. Reason: that is private and not the point.
- No client is named on the site without that client's written approval.
- Nothing on the site may relate to the business of any current or former employer.
- Single static file, no tracking, no form that collects data. Reason: nothing to leak, free hosting, nobody in the middle of visitors' information.

# Golden checks (the site must always pass these)
1. The headline reads: Get more from your AI budget, with code you can trust.
2. There are exactly five gates (Write, Retrieval, Use, Health, Freshness), four services and four method steps.
3. Every Book a call button leads to the real booking link (see open items).
4. No performance numbers, no returns, no client names, no employer references anywhere.
5. The page works at phone width with no sideways scrolling.

# Open items
- Booking link is still the placeholder https://calendly.com/. Replace with the real link.
- Headshot is still the placeholder initials AC. Replace with a real photo.
