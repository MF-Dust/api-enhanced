import json
import os
import random
import re
import string
import time
import tempfile
from pathlib import Path
from urllib.parse import urlencode, quote

import httpx

import config as cfg
from crypto import weapi, linuxapi, eapi, eapi_res_decrypt
from utils import cookie_to_json, cookie_obj_to_string, to_boolean

# OS platform info
OS_MAP = {
    "pc": {
        "os": "pc",
        "appver": "3.1.17.204416",
        "osver": "Microsoft-Windows-10-Professional-build-19045-64bit",
        "channel": "netease",
    },
    "linux": {
        "os": "linux",
        "appver": "1.2.1.0428",
        "osver": "Deepin 20.9",
        "channel": "netease",
    },
    "android": {
        "os": "android",
        "appver": "8.20.20.231215173437",
        "osver": "14",
        "channel": "xiaomi",
    },
    "iphone": {
        "os": "iPhone OS",
        "appver": "9.0.90",
        "osver": "16.2",
        "channel": "distribution",
    },
}

# User-Agent profiles
USER_AGENT_MAP = {
    "weapi": {
        "pc": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    },
    "linuxapi": {
        "linux": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    },
    "api": {
        "pc": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Chrome/91.0.4472.164 NeteaseMusicDesktop/3.0.18.203152",
        "android": "NeteaseMusic/9.1.65.240927161425(9001065);Dalvik/2.1.0 (Linux; U; Android 14; 23013RK75C Build/UKQ1.230804.001)",
        "iphone": "NeteaseMusic 9.0.90/5038 (iPhone; iOS 16.2; zh_CN)",
    },
}

SPECIAL_STATUS_CODES = {201, 302, 400, 502, 800, 801, 802, 803}

# Pre-compute WNMCID
_chars = string.ascii_lowercase
WNMCID = f"{''.join(random.choice(_chars) for _ in range(6))}.{int(time.time() * 1000)}.01.0"


def _get_anonymous_token() -> str:
    if cfg.ANONYMOUS_TOKEN:
        return cfg.ANONYMOUS_TOKEN
    try:
        tmp_path = Path(tempfile.gettempdir()) / "anonymous_token"
        return tmp_path.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def _choose_user_agent(crypto: str, ua_type: str = "pc") -> str:
    return USER_AGENT_MAP.get(crypto, {}).get(ua_type, "")


def _process_cookie(cookie: dict, uri: str) -> dict:
    ntes_nuid = "".join(random.choice("0123456789abcdef") for _ in range(32))
    os_info = OS_MAP.get(cookie.get("os", ""), OS_MAP["pc"])

    processed = {
        **cookie,
        "__remember_me": "true",
        "ntes_kaola_ad": "1",
        "_ntes_nuid": cookie.get("_ntes_nuid", ntes_nuid),
        "_ntes_nnid": cookie.get("_ntes_nnid", f"{ntes_nuid},{int(time.time() * 1000)}"),
        "WNMCID": cookie.get("WNMCID", WNMCID),
        "WEVNSM": cookie.get("WEVNSM", "1.0.0"),
        "osver": cookie.get("osver", os_info["osver"]),
        "deviceId": cookie.get("deviceId", cfg.DEVICE_ID),
        "os": cookie.get("os", os_info["os"]),
        "channel": cookie.get("channel", os_info["channel"]),
        "appver": cookie.get("appver", os_info["appver"]),
    }

    if "login" not in uri:
        nmtid = "".join(random.choice("0123456789abcdef") for _ in range(16))
        processed["NMTID"] = nmtid

    if "MUSIC_U" not in processed:
        if "MUSIC_A" not in processed:
            processed["MUSIC_A"] = _get_anonymous_token()

    return processed


def _create_header_cookie(header: dict) -> str:
    parts = []
    for key, value in header.items():
        parts.append(f"{quote(str(key))}={quote(str(value))}")
    return "; ".join(parts)


def _generate_request_id() -> str:
    return f"{int(time.time() * 1000)}_{random.randint(0, 999):04d}"


async def ncm_request(url: str, data: dict, options: dict) -> dict:
    headers = {**(options.get("headers") or {})}
    ip = options.get("realIP") or options.get("ip") or ""

    if ip:
        headers["X-Real-IP"] = ip
        headers["X-Forwarded-For"] = ip

    cookie = options.get("cookie") or {}
    if isinstance(cookie, str):
        cookie = cookie_to_json(cookie)

    if isinstance(cookie, dict):
        cookie = _process_cookie(cookie, url)
        headers["Cookie"] = cookie_obj_to_string(cookie)

    crypto = options.get("crypto", "")
    csrf_token = cookie.get("__csrf", "")

    if not crypto:
        crypto = "eapi" if cfg.ENCRYPT else "api"

    encrypt_data = ""
    answer = {"status": 500, "body": {}, "cookie": []}

    # Handle e_r (encrypt response)
    e_r = to_boolean(
        options.get("e_r") if options.get("e_r") is not None
        else data.get("e_r") if data.get("e_r") is not None
        else cfg.ENCRYPT_RESPONSE
    )
    data["e_r"] = e_r

    target_url = ""

    if crypto == "weapi":
        headers["Referer"] = options.get("domain") or cfg.DOMAIN
        headers["User-Agent"] = options.get("ua") or _choose_user_agent("weapi")
        data["csrf_token"] = csrf_token
        encrypt_data = weapi(data)
        # weapi URL: strip /api/ prefix and prepend /weapi/
        path = url[5:] if url.startswith("/api/") else url
        target_url = f"{options.get('domain') or cfg.DOMAIN}/weapi/{path}"

    elif crypto == "linuxapi":
        headers["User-Agent"] = options.get("ua") or _choose_user_agent("linuxapi", "linux")
        encrypt_data = linuxapi({
            "method": "POST",
            "url": f"{options.get('domain') or cfg.DOMAIN}{url}",
            "params": data,
        })
        target_url = f"{options.get('domain') or cfg.DOMAIN}/api/linux/forward"

    elif crypto in ("eapi", "api"):
        header = {
            "osver": cookie.get("osver"),
            "deviceId": cookie.get("deviceId"),
            "os": cookie.get("os"),
            "appver": cookie.get("appver"),
            "versioncode": cookie.get("versioncode", "140"),
            "mobilename": cookie.get("mobilename", ""),
            "buildver": cookie.get("buildver", str(int(time.time()))[:10]),
            "resolution": cookie.get("resolution", "1920x1080"),
            "__csrf": csrf_token,
            "channel": cookie.get("channel"),
            "requestId": _generate_request_id(),
        }
        if options.get("checkToken"):
            header["X-antiCheatToken"] = cfg.CHECK_TOKEN
        if cookie.get("MUSIC_U"):
            header["MUSIC_U"] = cookie["MUSIC_U"]
        if cookie.get("MUSIC_A"):
            header["MUSIC_A"] = cookie["MUSIC_A"]

        headers["Cookie"] = _create_header_cookie(header)
        headers["User-Agent"] = options.get("ua") or _choose_user_agent("api", "iphone")

        if crypto == "eapi":
            data["header"] = header
            encrypt_data = eapi(url, data)
            # eapi URL: strip /api/ prefix and prepend /eapi/
            path = url[5:] if url.startswith("/api/") else url
            target_url = f"{options.get('domain') or cfg.API_DOMAIN}/eapi/{path}"
        else:
            target_url = f"{options.get('domain') or cfg.API_DOMAIN}{url}"
            encrypt_data = data
    else:
        print(f"[ERR] Unknown Crypto: {crypto}")
        return {"status": 500, "body": {"code": 500, "msg": f"Unknown crypto: {crypto}"}, "cookie": []}

    # Prepare request body
    if isinstance(encrypt_data, dict):
        body = urlencode(encrypt_data)
    else:
        body = urlencode(encrypt_data) if isinstance(encrypt_data, dict) else str(encrypt_data)

    # For weapi/eapi, encrypt_data is a dict with params/encSecKey or params
    if crypto in ("weapi", "eapi", "linuxapi") and isinstance(encrypt_data, dict):
        body = urlencode(encrypt_data)

    use_e_r = crypto in ("eapi", "weapi") and e_r

    # Proxy settings
    proxy_url = options.get("proxy")
    if not proxy_url and cfg.ENABLE_PROXY == "true" and cfg.PROXY_URL:
        proxy_url = cfg.PROXY_URL

    try:
        async with httpx.AsyncClient(
            proxy=proxy_url if proxy_url else None,
            timeout=30.0,
            follow_redirects=False,
        ) as client:
            response = await client.post(
                target_url,
                content=body,
                headers=headers,
            )

        # Extract cookies from response
        answer["cookie"] = [
            re.sub(r"\s*Domain=[^(;|$)]+;*", "", v)
            for k, v in response.headers.multi_items()
            if k.lower() == "set-cookie"
        ]

        if use_e_r:
            hex_content = response.content.hex().upper()
            answer["body"] = eapi_res_decrypt(hex_content, headers.get("x-aeapi", False))
        else:
            try:
                answer["body"] = response.json()
            except Exception:
                answer["body"] = response.text or {}

        # Ensure body is a dict for consistent access
        if not isinstance(answer["body"], dict):
            answer["body"] = {"code": response.status_code, "data": answer["body"]}

        if "code" in answer["body"]:
            answer["body"]["code"] = int(answer["body"]["code"])

        answer["status"] = int(answer["body"].get("code", response.status_code))

        if answer["body"].get("code") in SPECIAL_STATUS_CODES:
            answer["status"] = 200

    except Exception as e:
        answer["status"] = 502
        answer["body"] = {"code": 502, "msg": str(e)}
        print(f"[ERR] {answer}")

    answer["status"] = answer["status"] if 100 < answer["status"] < 600 else 400

    if answer["status"] == 200:
        return answer
    else:
        print(f"[ERR] {answer}")
        raise RequestError(answer)


class RequestError(Exception):
    def __init__(self, response: dict):
        self.status = response.get("status", 500)
        self.body = response.get("body", {})
        self.cookie = response.get("cookie", [])
        super().__init__(str(self.body))
