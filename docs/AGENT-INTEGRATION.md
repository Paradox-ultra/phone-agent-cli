# Agent integration

Phone Agent intentionally ships without an LLM. The agent owns planning and verification; Phone Agent exposes an inspectable capability surface.

## HTTP tools

Start `phone-agent serve`. The API binds to `127.0.0.1` by default.

1. Read the token from `~/.config/phone-agent/config.json`.
2. Discover tools with `GET /v1/tools`.
3. Invoke a tool with `POST /v1/call`, for example `{"tool":"workspace.list","arguments":{"path":"."}}`.
4. Inspect the JSON response before deciding the next action.

All requests use `Authorization: Bearer TOKEN`.

## Python adapter example

```python
import json, urllib.request
BASE = "http://127.0.0.1:8765"
TOKEN = "read-from-phone-agent-config"
def phone_tool(name, arguments=None):
    body = json.dumps({"tool": name, "arguments": arguments or {}}).encode()
    req = urllib.request.Request(BASE + "/v1/call", data=body,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)
```

## MCP roadmap

MCP stdio is planned as a transport adapter separate from tool implementations. The same contracts can serve shell agents, IDE agents, and custom orchestrators.

## Remote agents

Do not bind to `0.0.0.0` on an untrusted network. Prefer an authenticated SSH tunnel or secured private overlay network. Never paste the bearer token into prompts, public issue comments, or logs.
