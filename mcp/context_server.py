#!/usr/bin/env python3
"""Context MCP server for transformloop.ai: the retrieval gate. Stdio JSON-RPC, no dependencies."""
import glob, hashlib, json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSION = os.path.join(ROOT, ".context-session.json")


def sha(path):
    with open(os.path.join(ROOT, path), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def covers(ctx_file):
    with open(os.path.join(ROOT, ctx_file), encoding="utf-8") as f:
        for line in f:
            if line.startswith("Covers:"):
                return [p.strip() for p in line[len("Covers:"):].replace(",", " ").split()]
    return []


def covering(path):
    found = []
    for ctx in sorted(glob.glob(os.path.join(ROOT, "context", "*.md"))):
        rel = os.path.relpath(ctx, ROOT).replace(os.sep, "/")
        if path in covers(rel):
            found.append(rel)
    return found


def load_session():
    try:
        with open(SESSION, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"files": [], "retrieved": {}}


def save_session(s):
    with open(SESSION, "w", encoding="utf-8") as f:
        json.dump(s, f)


def get_context(args):
    paths = args.get("paths", [])
    session = load_session()
    out, missing = [], []
    for p in paths:
        ctxs = covering(p)
        if not ctxs:
            missing.append(p)
            continue
        if p not in session["files"]:
            session["files"].append(p)
        for c in ctxs:
            session["retrieved"][c] = sha(c)
            with open(os.path.join(ROOT, c), encoding="utf-8") as f:
                out.append({"file": c, "sha256": sha(c), "covers": p, "text": f.read()})
    save_session(session)
    if missing:
        return {"isError": True, "text": "Write gate: no context covers " + ", ".join(missing)
                + ". Write the context first (Owner, Why, Covers), then retrieve it."}
    return {"text": json.dumps(out, indent=2)}


def write_receipt(args):
    session = load_session()
    if not session["files"]:
        return {"isError": True, "text": "Nothing retrieved yet. Call get_context for the files you will change first."}
    receipt = {
        "summary": args.get("summary", ""),
        "files_touched": sorted(session["files"]),
        "retrieved": [{"file": f, "sha256": h} for f, h in sorted(session["retrieved"].items())],
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    os.makedirs(os.path.join(ROOT, "receipts"), exist_ok=True)
    with open(os.path.join(ROOT, "receipts", "latest.json"), "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
        f.write(chr(10))
    save_session({"files": [], "retrieved": {}})
    return {"text": "Wrote receipts/latest.json. Commit it with your change."}


TOOLS = {
    "get_context": (get_context, "Retrieval gate. Returns the context covering the files you are about to change, with the version (sha256) of each context file. Call this before editing any code.",
                    {"type": "object", "properties": {"paths": {"type": "array", "items": {"type": "string"}}}, "required": ["paths"]}),
    "write_receipt": (write_receipt, "Records what was retrieved into receipts/latest.json so the use gate can check it. Call this after editing and commit the file with your change.",
                      {"type": "object", "properties": {"summary": {"type": "string"}}, "required": ["summary"]}),
}


def reply(msg_id, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": msg_id}
    if error is not None:
        msg["error"] = error
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg) + chr(10))
    sys.stdout.flush()


def handle(msg):
    method, msg_id = msg.get("method"), msg.get("id")
    if method == "initialize":
        reply(msg_id, {"protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
                       "capabilities": {"tools": {}}, "serverInfo": {"name": "transformloop-context", "version": "0.1.0"}})
    elif method == "tools/list":
        reply(msg_id, {"tools": [{"name": n, "description": d, "inputSchema": s} for n, (_, d, s) in TOOLS.items()]})
    elif method == "tools/call":
        params = msg.get("params", {})
        tool = TOOLS.get(params.get("name"))
        if not tool:
            reply(msg_id, error={"code": -32602, "message": "unknown tool"})
            return
        res = tool[0](params.get("arguments", {}))
        reply(msg_id, {"content": [{"type": "text", "text": res["text"]}], "isError": bool(res.get("isError"))})
    elif msg_id is not None:
        reply(msg_id, error={"code": -32601, "message": "method not found"})


def main():
    for line in sys.stdin:
        line = line.strip()
        if line:
            handle(json.loads(line))


if __name__ == "__main__":
    main()
