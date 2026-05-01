from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "userId": query.get("uid"),
        "limit": query.get("limit", 30),
        "time": query.get("before", 0),
        "total": "true",
    }
    return await request("/api/msg/private/history", data, create_option(query, "weapi"))
