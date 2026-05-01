from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "uid": query.get("uid", ""),
        "limit": query.get("limit", 30),
        "offset": query.get("offset", 0),
        "includeVideo": True,
    }
    return await request("/api/user/playlist", data, create_option(query, "weapi"))
