from pathlib import Path

def safe_path(root: Path, supplied: str) -> Path:
    base = root.expanduser().resolve()
    candidate = (base / supplied).resolve()
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        raise PermissionError("Path escapes the configured workspace") from exc
    return candidate
