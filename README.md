# Phone Agent CLI

A Termux-first, provider-agnostic tool bridge that lets AI agents use an Android phone-side workspace through a local JSON API and CLI.

**Experimental MVP.** Inspired by the architecture of Vercel's [agent-desktop](https://github.com/vercel-labs/agent-desktop): the calling agent owns reasoning; Phone Agent exposes tools, structured results, and verification. This is an original Android/Termux implementation, not a port of its desktop accessibility code.

## Install

```bash
pkg update -y
pkg install -y python git
git clone https://github.com/Paradox-ultra/phone-agent-cli.git
cd phone-agent-cli
bash install.sh
phone-agent init
phone-agent doctor
phone-agent serve
```

The server binds to `127.0.0.1:8765` by default. Initialization creates a private bearer token in `~/.config/phone-agent/config.json`.

## Tools

- `system.info` — basic Termux/runtime facts
- `workspace.list`, `workspace.read`, `workspace.write`, `workspace.search` — workspace-scoped file operations
- `shell.exec` — allowlisted process execution, disabled by default
- `termux.battery`, `termux.clipboard.get` — optional Termux:API tools

## Agent integration

Discover tools with `GET /v1/tools` and invoke with `POST /v1/call`. Both require `Authorization: Bearer TOKEN`. See [docs/AGENT-INTEGRATION.md](docs/AGENT-INTEGRATION.md).

## Security and limitations

- Localhost-only; no unauthenticated network listener.
- Workspace paths are canonicalized to prevent traversal.
- Shell execution is opt-in, allowlisted, argv-based (no shell interpolation), timeout-limited, and output-limited.
- Termux cannot automatically inspect or control every Android app. UI automation, notifications, calls, SMS, screen capture, camera, microphone, and location need separate Android components and explicit permissions. See [Android capabilities](docs/ANDROID-CAPABILITIES.md).
- Treat tool output as private; it can contain personal files or clipboard contents.

## Roadmap

MCP stdio transport; opt-in Android accessibility companion; snapshot-scoped UI references; richer Termux:API adapters; agent examples; audit logs; signed releases.

## License

Apache-2.0.
