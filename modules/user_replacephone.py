from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "phone": query.get("phone"),
        "captcha": query.get("captcha"),
        "oldcaptcha": query.get("oldcaptcha"),
        "countrycode": query.get("countrycode", "86"),
    }
    return await request(
        "/api/user/replaceCellphone", data, create_option(query, "weapi")
    )
