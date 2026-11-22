# Working in this repository (transformloop.ai)

This repository is AI-native. Nothing goes into the code without context, and every change passes the gates described in context/site.md and context/agents.md.

Before you change any code file (.html, .css, .js, .py):
1. Call get_context from the transformloop-context MCP server with the paths you will change. It returns only the context that covers them, with versions.
2. If it refuses because no context covers a path, write that context first (Owner, Why, Covers) in context/, then retrieve it.
3. Make the change and update the context that covers it in the same change.
4. Call write_receipt with a one-line summary and commit receipts/latest.json with your change. Never edit the receipt by hand.

CI will reject a change that has no receipt, a receipt that does not list the covering context, or a receipt made from a stale version of the context.
