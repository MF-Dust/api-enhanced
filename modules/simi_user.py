from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "songid": query.get("id"),
        "limit": query.get("limit", 50),
        "offset": query.get("offset", 0),
    }
    return await request("/api/discovery/simiUser", data, create_option(query, "weapi"))
