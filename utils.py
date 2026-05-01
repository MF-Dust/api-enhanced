import os
import random
import secrets
import time
from pathlib import Path
from urllib.parse import quote, unquote

DATA_DIR = Path(__file__).parent / "data"


def cookie_to_json(cookie_str: str) -> dict:
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


def cookie_obj_to_string(cookie: dict) -> str:
    parts = []
    for key, value in cookie.items():
        parts.append(f"{quote(str(key))}={quote(str(value))}")
    return "; ".join(parts)


def to_boolean(val) -> bool:
    if isinstance(val, bool):
        return val
    if val == "":
        return False
    return str(val).lower() in ("true", "1")


def js_loose_equal(left, right) -> bool:
    """Match JavaScript's common string/number equality for query params."""
    if left == right:
        return True
    try:
        return float(left) == float(right)
    except (TypeError, ValueError):
        return str(left).lower() == str(right).lower()


def is_one(val) -> bool:
    return js_loose_equal(val, 1)


def _ip_to_int(ip: str) -> int:
    parts = [int(x) for x in ip.split(".")]
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]


def _int_to_ip(ip_int: int) -> str:
    return ".".join([
        str((ip_int >> 24) & 0xFF),
        str((ip_int >> 16) & 0xFF),
        str((ip_int >> 8) & 0xFF),
        str(ip_int & 0xFF),
    ])


def _parse_cidr(cidr: str) -> dict:
    ip_str, prefix_len_str = cidr.split("/")
    prefix_len = int(prefix_len_str)
    ip_int = _ip_to_int(ip_str)
    mask = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    start = ip_int & mask
    end = start | (~mask & 0xFFFFFFFF)
    count = end - start + 1
    return {"start": start, "end": end, "count": count, "cidr": cidr}


_china_ip_ranges: list[dict] = []
_total_ips: int = 0


def _load_china_ip_ranges():
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
        print(f"Failed to load china_ip_ranges.txt: {e}")
        _china_ip_ranges = []
        _total_ips = 0


def generate_random_chinese_ip() -> str:
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
    hex_chars = "0123456789ABCDEF"
    return "".join(random.choice(hex_chars) for _ in range(52))


def generate_chain_id(cookie: dict, action: str = "login") -> str:
    device_id = cookie.get("sDeviceId", f"unknown-{random.randint(0, 999999)}")
    return f"v1_{device_id}_web_{action}_{int(time.time() * 1000)}"
