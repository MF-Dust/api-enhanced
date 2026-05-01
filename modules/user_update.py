from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "birthday": query.get("birthday"),
        "city": query.get("city"),
        "gender": query.get("gender"),
        "nickname": query.get("nickname"),
        "province": query.get("province"),
        "signature": query.get("signature"),
    }
    return await request("/api/user/profile/update", data, create_option(query))
