"""Helper functions and utilities."""

import json
from typing import Any


def serialize_json(data: Any) -> str:
    """Serialize data to JSON string.

    Args:
        data: Data to serialize

    Returns:
        JSON string
    """
    return json.dumps(data, ensure_ascii=False)


def deserialize_json(json_str: str) -> dict[str, Any]:
    """Deserialize JSON string to dictionary.

    Args:
        json_str: JSON string

    Returns:
        Dictionary
    """
    return json.loads(json_str)

