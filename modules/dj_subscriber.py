from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "time": query.get("time", "-1"),
        "id": query.get("id", ""),
        "limit": query.get("limit", "20"),
        "total": "true",
    }
    return await request("/api/djradio/subscriber", data, create_option(query, "weapi"))
