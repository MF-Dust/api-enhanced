import hashlib
import base64
from option import create_option
from utils import generate_device_id
import config as cfg


def _cloudmusic_dll_encode_id(some_id: str) -> str:
    key = "3go8&$8*3*3h0k(2)2"
    xored = ""
    for i, ch in enumerate(some_id):
        xored += chr(ord(ch) ^ ord(key[i % len(key)]))
    digest = hashlib.md5(xored.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("utf-8")


async def handler(query: dict, request) -> dict:
    device_id = generate_device_id()
    cfg.DEVICE_ID = device_id
    encoded_id = base64.b64encode(
        f"{device_id} {_cloudmusic_dll_encode_id(device_id)}".encode("utf-8")
    ).decode("utf-8")
    data = {"username": encoded_id}
    result = await request("/api/register/anonimous", data, create_option(query, "weapi"))
    if result["body"].get("code") == 200:
        return {
            "status": 200,
            "body": {
                **result["body"],
                "cookie": ";".join(result.get("cookie", [])),
            },
            "cookie": result.get("cookie", []),
        }
    return result
