from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "privacy": 0,
    }
    return await request("/api/playlist/update/privacy", data, create_option(query))
