from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "captcha": query.get("captcha"),
        "phone": query.get("phone"),
        "oldcaptcha": query.get("oldcaptcha"),
        "ctcode": query.get("ctcode", "86"),
    }
    return await request(
        "/api/user/replaceCellphone",
        data,
        create_option(query, "weapi"),
    )
