from typing import Dict, Any, Union
import time
import json
import logging

def format_timestamp(ts: Union[float, int]) -> str:
    """Formats a UNIX timestamp into a readable string."""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

def deep_merge(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merges dictionary B into dictionary A."""
    for key, value in source.items():
        if key in target and isinstance(target[key], dict) and isinstance(value, dict):
            target[key] = deep_merge(target[key], value)
        else:
            target[key] = value
    return target

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Utility to safely load a JSON configuration file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"JSON file not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"JSON file decode error: {file_path}")
        return {}