"""
Utility functions for PyNCMAPI.

This module provides helper functions for cookie handling, type conversion,
IP address generation, and other common operations.
"""

import random
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

DATA_DIR = Path(__file__).parent / "data"


def cookie_to_json(cookie_str: str) -> dict[str, str]:
    """
    Convert cookie string to dictionary.

    Args:
        cookie_str: Cookie string in format "key1=value1; key2=value2"

    Returns:
        Dictionary with cookie key-value pairs
    """
    if not cookie_str:
        return {}
    result = {}
    for item in cookie_str.split(";"):
        item = item.strip()
        if not item:
            continue
        parts = item.split("=", 1)
        if len(parts) == 2:
            result[parts[0].strip()] = parts[1].strip()
    return result


def cookie_obj_to_string(cookie: dict[str, Any]) -> str:
    """
    Convert cookie dictionary to string.

    Args:
        cookie: Dictionary with cookie key-value pairs

    Returns:
        Cookie string in format "key1=value1; key2=value2"
    """
    parts = []
    for key, value in cookie.items():
        parts.append(f"{quote(str(key))}={quote(str(value))}")
    return "; ".join(parts)


def to_boolean(val: Any) -> bool:
    """
    Convert value to boolean.

    Args:
        val: Value to convert (string, int, bool, etc.)

    Returns:
        Boolean representation of the value
    """
    if isinstance(val, bool):
        return val
    if val == "":
        return False
    return str(val).lower() in ("true", "1")


def js_loose_equal(left: Any, right: Any) -> bool:
    """
    Match JavaScript's loose equality for query params.

    Args:
        left: Left value to compare
        right: Right value to compare

    Returns:
        True if values are loosely equal
    """
    if left == right:
        return True
    try:
        return float(left) == float(right)
    except (TypeError, ValueError):
        return str(left).lower() == str(right).lower()


def is_one(val: Any) -> bool:
    """Check if value is loosely equal to 1."""
    return js_loose_equal(val, 1)


def _ip_to_int(ip: str) -> int:
    """Convert IP address string to integer."""
    parts = [int(x) for x in ip.split(".")]
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]


def _int_to_ip(ip_int: int) -> str:
    """Convert integer to IP address string."""
    return ".".join(
        [
            str((ip_int >> 24) & 0xFF),
            str((ip_int >> 16) & 0xFF),
            str((ip_int >> 8) & 0xFF),
            str(ip_int & 0xFF),
        ]
    )


def _parse_cidr(cidr: str) -> dict[str, Any]:
    """
    Parse CIDR notation to IP range.

    Args:
        cidr: CIDR notation string (e.g., "192.168.0.0/24")

    Returns:
        Dictionary with start, end, count, and cidr fields
    """
    ip_str, prefix_len_str = cidr.split("/")
    prefix_len = int(prefix_len_str)
    ip_int = _ip_to_int(ip_str)
    mask = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    start = ip_int & mask
    end = start | (~mask & 0xFFFFFFFF)
    count = end - start + 1
    return {"start": start, "end": end, "count": count, "cidr": cidr}


_china_ip_ranges: list[dict[str, Any]] = []
_total_ips: int = 0


def _load_china_ip_ranges() -> None:
    """Load China IP ranges from data file."""
    global _china_ip_ranges, _total_ips
    if _china_ip_ranges:
        return
    try:
        filepath = DATA_DIR / "china_ip_ranges.txt"
        content = filepath.read_text(encoding="utf-8-sig")
        lines = [line.strip() for line in content.split("\n") if line.strip() and not line.startswith("#")]
        total = 0
        ranges = []
        for line in lines:
            r = _parse_cidr(line)
            ranges.append(r)
            total += r["count"]
        ranges.sort(key=lambda x: x["count"], reverse=True)
        _china_ip_ranges = ranges
        _total_ips = total
    except Exception as e:
        from logger import log_error

        log_error("Failed to load china_ip_ranges.txt", exc=e)
        _china_ip_ranges = []
        _total_ips = 0


def generate_random_chinese_ip() -> str:
    """
    Generate random Chinese IP address.

    Returns:
        Random IP address string from China IP ranges
    """
    _load_china_ip_ranges()
    if not _total_ips:
        return f"116.{random.randint(25, 94)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    offset = random.randint(0, _total_ips - 1)
    chosen = None
    for seg in _china_ip_ranges:
        if offset < seg["count"]:
            chosen = seg
            break
        offset -= seg["count"]
    if not chosen:
        chosen = _china_ip_ranges[-1]
    seg_size = chosen["end"] - chosen["start"] + 1
    ip_int = chosen["start"] + random.randint(0, seg_size - 1)
    return _int_to_ip(ip_int)


def generate_device_id() -> str:
    """
    Generate random device ID.

    Returns:
        52-character hexadecimal device ID
    """
    hex_chars = "0123456789ABCDEF"
    return "".join(random.choice(hex_chars) for _ in range(52))


def generate_chain_id(cookie: dict[str, Any], action: str = "login") -> str:
    """
    Generate chain ID for request tracking.

    Args:
        cookie: Cookie dictionary
        action: Action type (default: "login")

    Returns:
        Chain ID string
    """
    device_id = cookie.get("sDeviceId", f"unknown-{random.randint(0, 999999)}")
    return f"v1_{device_id}_web_{action}_{int(time.time() * 1000)}"
