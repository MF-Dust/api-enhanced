import hashlib
from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "captcha": query.get("captcha", ""),
        "phone": query.get("phone", ""),
        "password": hashlib.md5((query.get("password") or "").encode()).hexdigest(),
        "nickname": query.get("nickname", ""),
        "countrycode": query.get("countrycode", "86"),
        "force": "false",
    }
    return await request("/api/w/register/cellphone", data, create_option(query))
