from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 30),
        "offset": query.get("offset", 0),
    }
    return await request("/api/djradio/hot/v1", data, create_option(query, "weapi"))
