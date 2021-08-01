from typing import Any, Dict

__all__ = ("rollout",)


def rollout(keys: Dict[str, Any], separator: str = ".") -> Dict[str, Any]:
    updated = {}
    for comp_key, val in keys.items():
        assert isinstance(comp_key, str)
        parts = comp_key.split(separator)
        key = parts[0]
        if len(parts) == 1:
            updated[key] = val
        else:
            if key not in updated:
                updated[key] = {}
            tail = separator.join(parts[1:])
            updated[key][tail] = val
    for key, val in updated.items():
        updated[key] = rollout(val) if isinstance(val, dict) else val
    return updated
