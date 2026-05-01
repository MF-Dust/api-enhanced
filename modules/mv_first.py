from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "area": query.get("area", ""),
        "limit": query.get("limit", 30),
        "total": True,
    }
    return await request("/api/mv/first", data, create_option(query))
