from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "ctcode": query.get("ctcode", "86"),
        "cellphone": query.get("phone", ""),
        "captcha": query.get("captcha", ""),
    }
    return await request("/api/sms/captcha/verify", data, create_option(query, "weapi"))
