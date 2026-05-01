from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "type": query.get("type", 1),
        "limit": 100,
        "offset": 0,
        "total": True,
    }
    return await request("/api/toplist/artist", data, create_option(query, "weapi"))
