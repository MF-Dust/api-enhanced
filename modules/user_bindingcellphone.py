import hashlib

from option import create_option


async def handler(query: dict, request) -> dict:
    password = query.get("password", "")
    data = {
        "phone": query.get("phone"),
        "countrycode": query.get("countrycode", "86"),
        "captcha": query.get("captcha"),
        "password": hashlib.md5(password.encode()).hexdigest() if password else "",
    }
    return await request(
        "/api/user/bindingCellphone", data, create_option(query, "weapi")
    )
