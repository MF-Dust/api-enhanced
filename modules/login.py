import hashlib
from option import create_option


async def handler(query: dict, request) -> dict:
    password = query.get("md5_password") or hashlib.md5(
        (query.get("password") or "").encode()
    ).hexdigest()
    data = {
        "type": "0",
        "https": "true",
        "username": query.get("email", ""),
        "password": password,
        "rememberLogin": "true",
    }
    result = await request("/api/w/login", data, create_option(query))
    if result["body"].get("code") == 502:
        return {
            "status": 200,
            "body": {"msg": "账号或密码错误", "code": 502, "message": "账号或密码错误"},
        }
    if result["body"].get("code") == 200:
        import json
        body_str = json.dumps(result["body"]).replace("avatarImgId_str", "avatarImgIdStr")
        body = json.loads(body_str)
        body["cookie"] = ";".join(result.get("cookie", []))
        return {"status": 200, "body": body, "cookie": result.get("cookie", [])}
    return result
