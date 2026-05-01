from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 30),
        "time": query.get("lasttime", -1),
    }
    return await request("/api/msg/notices", data, create_option(query, "weapi"))
