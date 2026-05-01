from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "limit": query.get("limit", 20),
        "offset": query.get("offset", 0),
    }
    return await request("/api/playlist/subscribers", data, create_option(query))
