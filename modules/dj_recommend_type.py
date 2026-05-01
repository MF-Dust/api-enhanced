from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "cateId": query.get("type", ""),
    }
    return await request("/api/djradio/recommend", data, create_option(query, "weapi"))
