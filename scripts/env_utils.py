"""Load ignored repository-local environment files without dependencies."""

from __future__ import annotations

import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_FILES = (ROOT / ".env.local", ROOT / ".env")
KEY_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def load_local_env() -> list[str]:
    """Populate unset variables from .env.local, then .env.

    Shell variables win because existing keys are never overwritten. Returning
    names rather than values allows callers to inspect behavior without exposing
    secrets.
    """
    loaded: list[str] = []
    for path in ENV_FILES:
        if not path.is_file():
            continue
        for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if not KEY_PATTERN.fullmatch(key) or key in os.environ:
                continue
            os.environ[key] = _strip_quotes(value.strip())
            loaded.append(key)
    return loaded
