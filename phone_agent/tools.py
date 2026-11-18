from __future__ import annotations
import os, platform, subprocess
from pathlib import Path
from .security import safe_path

def _workspace(cfg):
    return Path(cfg["workspace"]).expanduser().resolve()

def _system_info(_cfg, _args):
    return {"platform": platform.platform(), "python": platform.python_version(),
            "prefix": os.environ.get("PREFIX"), "home": str(Path.home()),
            "termux": bool(os.environ.get("TERMUX_VERSION")),
            "android": os.environ.get("ANDROID_ROOT") is not None}

def _list(cfg, a):
    p = safe_path(_workspace(cfg), a.get("path", "."))
    if not p.exists(): raise FileNotFoundError(str(p))
    if not p.is_dir(): raise NotADirectoryError(str(p))
    return {"path": str(p.relative_to(_workspace(cfg))),
            "entries": [{"name": x.name, "type": "dir" if x.is_dir() else "file"}
                        for x in sorted(p.iterdir(), key=lambda x: x.name.lower())]}

def _read(cfg, a):
    p = safe_path(_workspace(cfg), a["path"])
    if p.stat().st_size > 200_000: raise ValueError("File exceeds 200 KB read limit")
    return {"path": str(p.relative_to(_workspace(cfg))), "content": p.read_text(encoding="utf-8")}

def _write(cfg, a):
    p = safe_path(_workspace(cfg), a["path"])
    content = a["content"]
    if not isinstance(content, str) or len(content.encode("utf-8")) > 200_000:
        raise ValueError("content must be UTF-8 text up to 200 KB")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return {"path": str(p.relative_to(_workspace(cfg))), "bytes": len(content.encode("utf-8"))}

def _search(cfg, a):
    root = safe_path(_workspace(cfg), a.get("path", "."))
    if not root.is_dir(): raise NotADirectoryError(str(root))
    needle, matches = a["query"], []
    for p in root.rglob("*"):
        if len(matches) >= 100: break
        try:
            if p.is_file() and not p.is_symlink() and p.stat().st_size <= 200_000:
                for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                    if needle in line:
                        matches.append({"path": str(p.relative_to(_workspace(cfg))), "line": n, "text": line[:500]})
                    if len(matches) >= 100: break
        except (UnicodeDecodeError, OSError):
            pass
    return {"matches": matches, "truncated": len(matches) >= 100}

def _shell(cfg, a):
    if not cfg.get("shell_enabled"):
        raise PermissionError("Shell tool is disabled; explicitly enable it in config.json")
    argv = a.get("argv")
    if not isinstance(argv, list) or not argv or not all(isinstance(x, str) for x in argv):
        raise ValueError("argv must be a non-empty string array")
    if argv[0] not in cfg.get("shell_allowlist", []):
        raise PermissionError("Executable is not allowlisted")
    cwd = safe_path(_workspace(cfg), a.get("cwd", "."))
    timeout = min(max(int(a.get("timeout", 15)), 1), 60)
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False, shell=False)
    return {"returncode": p.returncode, "stdout": p.stdout[-12000:], "stderr": p.stderr[-12000:]}

def _termux_battery(_cfg, _args):
    p = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=8)
    if p.returncode: raise RuntimeError(p.stderr.strip() or "Termux:API battery command failed")
    import json
    return json.loads(p.stdout)

def _clipboard(_cfg, _args):
    p = subprocess.run(["termux-clipboard-get"], capture_output=True, text=True, timeout=8)
    if p.returncode: raise RuntimeError(p.stderr.strip() or "Termux:API clipboard command failed")
    return {"text": p.stdout[:20000]}

TOOLS = {
 "system.info": ("Read basic Termux/runtime information", _system_info),
 "workspace.list": ("List files under the workspace", _list),
 "workspace.read": ("Read a UTF-8 text file under the workspace", _read),
 "workspace.write": ("Write a UTF-8 text file under the workspace", _write),
 "workspace.search": ("Search text files under the workspace", _search),
 "shell.exec": ("Run an allowlisted process in the workspace (disabled by default)", _shell),
 "termux.battery": ("Read battery details through Termux:API", _termux_battery),
 "termux.clipboard.get": ("Read clipboard through Termux:API", _clipboard),
}

def call_tool(name: str, args: dict, cfg: dict):
    if name not in TOOLS: raise KeyError(f"Unknown tool: {name}")
    return TOOLS[name][1](cfg, args)

def catalog():
    return [{"name": name, "description": desc} for name, (desc, _) in TOOLS.items()]
