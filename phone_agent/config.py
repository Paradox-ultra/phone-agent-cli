from __future__ import annotations
import json, os, secrets
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("PHONE_AGENT_CONFIG", Path.home() / ".config" / "phone-agent"))
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_WORKSPACE = Path(os.environ.get("PHONE_AGENT_WORKSPACE", Path.home() / "phone-agent-workspace"))

def load_config() -> dict:
    if not CONFIG_FILE.exists():
        raise RuntimeError("Not initialized. Run: phone-agent init")
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))

def init_config() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DEFAULT_WORKSPACE.mkdir(parents=True, exist_ok=True)
    cfg = {"token": secrets.token_urlsafe(32), "host": "127.0.0.1", "port": 8765,
           "workspace": str(DEFAULT_WORKSPACE), "shell_enabled": False,
           "shell_allowlist": ["pwd", "ls", "git", "python", "python3", "grep", "find", "cat", "head", "tail"]}
    fd = os.open(CONFIG_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    return cfg
