import random
import time
from base64 import b64encode

import httpx

import config as cfg
from crypto import xeapi_sign, xeapi_decrypt_public_key


def _generate_nonce() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(16))


async def get_xeapi_public_key(
    current_public_key: dict | None = None, device_id: str = ""
) -> dict:
    """Fetch the xeapi public key from NetEase server."""
    if current_public_key is None:
        current_public_key = {}

    nonce = _generate_nonce()
    timestamp = str(int(time.time() * 1000))
    data = {
        "appVersion": "9.1.65",
        "currentKeyVersion": current_public_key.get("version", ""),
        "deviceId": device_id,
        "nonce": nonce,
        "os": "android",
        "requestType": "active",
        "signature": xeapi_sign(timestamp, nonce),
        "t1": "",
        "t2": "",
        "timestamp": timestamp,
        "uid": "",
    }

    async with httpx.AsyncClient(proxy=None, timeout=30.0) as client:
        response = await client.post(
            cfg.API_DOMAIN + "/api/gorilla/anti/crawler/security/key/get",
            headers={
                "User-Agent": (
                    "NeteaseMusic/9.1.65.240927161425(9001065);"
                    "Dalvik/2.1.0 (Linux; U; Android 14; "
                    "23013RK75C Build/UKQ1.230804.001)"
                ),
                "Cookie": f"deviceId={device_id}" if device_id else "",
            },
            content="&".join(f"{k}={v}" for k, v in data.items()),
        )

    res_data = response.json()
    if not res_data or res_data.get("code") != 200 or not res_data.get("data"):
        raise RuntimeError("xeapi public key request failed")

    res_inner = res_data["data"]
    if not res_inner.get("encryptedData"):
        raise RuntimeError("xeapi public key request failed: missing encryptedData")

    # Verify signature
    if res_inner.get("signature"):
        expected_sig = xeapi_sign(str(res_inner.get("timestamp", "")), nonce)
        if expected_sig != res_inner["signature"]:
            raise RuntimeError("xeapi public key response signature mismatch")

    public_key = xeapi_decrypt_public_key(res_inner["encryptedData"])

    # Preserve sk from current key if new response doesn't have it
    if not public_key.get("sk") and current_public_key.get("sk"):
        public_key["sk"] = current_public_key["sk"]
    if not public_key.get("sk"):
        raise RuntimeError("xeapi public key response missing sk")

    return public_key
