"""Application configuration loaded without optional runtime dependencies."""

import os
from pathlib import Path


def gemini_api_key() -> str | None:
    """Return the API key from the environment or the project's .env file."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key

    env_file = Path(__file__).resolve().parent.parent / ".env"
    if not env_file.exists():
        return None

    for line in env_file.read_text(encoding="utf-8").splitlines():
        name, separator, value = line.partition("=")
        if separator and name.strip() == "GEMINI_API_KEY":
            return value.strip().strip('"').strip("'") or None

    return None
