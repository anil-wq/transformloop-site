#!/usr/bin/env python3
"""Use gate, receipt part: a code change must carry a receipt of the context it retrieved, and that context must have been current."""
import glob, hashlib, json, os, subprocess, sys

CODE = (".html", ".css", ".js", ".py")
SKIP = ("context/", ".github/", "receipts/")


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def covers(ctx):
    with open(ctx, encoding="utf-8") as f:
        for line in f:
            if line.startswith("Covers:"):
                return [p.strip() for p in line[len("Covers:"):].replace(",", " ").split()]
    return []


def main():
    base = os.environ["BASE"]
    changed = run("git", "diff", "--name-only", "--diff-filter=ACMR", base, "HEAD").stdout.split()
    code = [c for c in changed if c.endswith(CODE) and not c.startswith(SKIP)]
    if not code:
        print("Use gate (receipt): no code changed, nothing to check.")
        return 0
    fail = 0
    if "receipts/latest.json" not in changed:
        print("::error::Use gate: code changed but receipts/latest.json was not updated. Retrieve context with the MCP server and write a receipt.")
        return 1
    with open("receipts/latest.json", encoding="utf-8") as f:
        receipt = json.load(f)
    listed = {r["file"]: r["sha256"] for r in receipt.get("retrieved", [])}
    touched = receipt.get("files_touched", [])
    for c in code:
        need = [x.replace(os.sep, "/") for x in sorted(glob.glob("context/*.md")) if c in covers(x)]
        if c not in touched:
            print("::error::Use gate: " + c + " changed but the receipt does not list it as retrieved before editing")
            fail = 1
        for n in need:
            if n not in listed:
                print("::error::Use gate: the receipt is missing the context " + n + " that covers " + c)
                fail = 1
    for f, sha in listed.items():
        old = subprocess.run(["git", "show", base + ":" + f], capture_output=True)
        if old.returncode == 0 and hashlib.sha256(old.stdout).hexdigest() != sha:
            print("::error::Freshness gate: " + f + " was retrieved at a version that is not the current one. Retrieve again and redo the change.")
            fail = 1
    if not fail:
        print("Use gate (receipt): receipt matches the current context.")
    return fail


if __name__ == "__main__":
    sys.exit(main())
