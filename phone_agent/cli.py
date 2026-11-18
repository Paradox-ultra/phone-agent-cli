from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .config import init_config, load_config
from .tools import catalog, call_tool
from .server import serve

def emit(obj): print(json.dumps(obj, ensure_ascii=False, indent=2))

def main():
    p = argparse.ArgumentParser(prog="phone-agent", description="Phone Agent CLI for Termux")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("init"); sub.add_parser("doctor"); sub.add_parser("tools"); sub.add_parser("serve")
    c = sub.add_parser("call"); c.add_argument("tool"); c.add_argument("--json", default="{}")
    args = p.parse_args()
    try:
        if args.command == "init":
            cfg = init_config()
            emit({"ok": True, "workspace": cfg["workspace"], "api": "http://127.0.0.1:8765",
                  "config": "~/.config/phone-agent/config.json", "message": "Bearer token generated; keep it private."})
        elif args.command == "doctor":
            cfg = load_config()
            import shutil, platform
            emit({"ok": True, "python": platform.python_version(), "workspace_exists": Path(cfg["workspace"]).exists(),
                  "termux_api": bool(shutil.which("termux-battery-status")), "shell_enabled": cfg["shell_enabled"],
                  "host": cfg["host"], "port": cfg["port"]})
        elif args.command == "tools": emit({"ok": True, "tools": catalog()})
        elif args.command == "serve": serve()
        elif args.command == "call":
            cfg = load_config(); result = call_tool(args.tool, json.loads(args.json), cfg)
            emit({"ok": True, "tool": args.tool, "data": result})
    except Exception as e:
        emit({"ok": False, "error": {"code": type(e).__name__.upper(), "message": str(e)}})
        sys.exit(1)

if __name__ == "__main__": main()
