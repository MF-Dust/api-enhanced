import hashlib
import json
from option import create_option


async def handler(query: dict, request) -> dict:
    captcha = query.get("captcha")
    password = captcha if captcha else (
        query.get("md5_password") or hashlib.md5(
            (query.get("password") or "").encode()
        ).hexdigest()
    )
    data = {
        "type": "1",
        "https": "true",
        "phone": query.get("phone", ""),
        "countrycode": query.get("countrycode", "86"),
        "captcha": captcha,
        ("captcha" if captcha else "password"): password,
        "remember": "true",
    }
    result = await request("/api/w/login/cellphone", data, create_option(query, "weapi"))
    if result["body"].get("code") == 200:
        body_str = json.dumps(result["body"]).replace("avatarImgId_str", "avatarImgIdStr")
        body = json.loads(body_str)
        body["cookie"] = ";".join(result.get("cookie", []))
        return {"status": 200, "body": body, "cookie": result.get("cookie", [])}
    return result
