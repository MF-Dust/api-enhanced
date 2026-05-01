from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id", ""),
        "private_cloud": "true",
        "work_type": 1,
        "order": query.get("order", "hot"),
        "offset": query.get("offset", 0),
        "limit": query.get("limit", 100),
    }
    return await request("/api/v1/artist/songs", data, create_option(query))
