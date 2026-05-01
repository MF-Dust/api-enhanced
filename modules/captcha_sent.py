from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "ctcode": query.get("ctcode", "86"),
        "secrete": "music_middleuser_pclogin",
        "cellphone": query.get("phone", ""),
    }
    return await request("/api/sms/captcha/sent", data, create_option(query, "weapi"))
