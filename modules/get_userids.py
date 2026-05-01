from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "nicknames": query.get("nicknames"),
    }
    return await request("/api/user/getUserIds", data, create_option(query, "weapi"))
