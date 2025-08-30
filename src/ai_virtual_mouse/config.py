# src/ai_virtual_mouse/config.py

from pathlib import Path
from typing import Any, Dict

import yaml

DEFAULT_CONFIG_PATH = Path("config.yaml")


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r") as f:
        return yaml.safe_load(f)


def get_nested(config: Dict[str, Any], *keys, default=None):
    """
    Helper to safely get nested config values.
    Example: get_nested(cfg, "gesture", "click_threshold", default=30.0)
    """
    current = config
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
