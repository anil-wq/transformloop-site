Owner: mailanilkumar
Why: Defines how agents build code in this repository: they retrieve context through an MCP server, record what they retrieved in a receipt, and the use gate checks the receipt.
Covers: mcp/context_server.py mcp/verify_receipt.py
Status: built and tested locally; wired into the Context gate workflow

# The loop an agent follows
1. Retrieve (retrieval gate): call get_context with the paths about to be changed. The MCP server (mcp/context_server.py, configured in .mcp.json) returns only the context files that cover those paths, with the sha256 version of each. If no context covers a path, it refuses: write the context first (write gate).
2. Change: edit the code and update the context that covers it, in the same change.
3. Record: call write_receipt. It writes receipts/latest.json listing the files touched and the context files and versions retrieved. Commit it with the change.
4. Verify (use gate, freshness gate): CI runs mcp/verify_receipt.py. A code change fails if there is no receipt, if the receipt does not list the context covering each changed file, or if a retrieved context version is not the version that was current before the change (stale context).

# Decisions and reasons
- The server has no dependencies and uses stdio. Reason: nothing to install, nothing to leak, runs anywhere an agent runs.
- The receipt records versions, not copies of the context. Reason: small, and the version is enough to prove the agent saw the current context.
- The server only reads files in this repository and writes only receipts/latest.json and a local, git-ignored session file. Reason: least privilege.
- Receipts are checked against the version of the context before the change, so updating the context in the same change is allowed and expected.

# Golden checks
1. get_context on a covered path returns the covering context and its sha256.
2. get_context on an uncovered path is refused.
3. A code change with a valid receipt passes the use gate.
4. A code change with no receipt fails. A code change with a stale receipt fails.
