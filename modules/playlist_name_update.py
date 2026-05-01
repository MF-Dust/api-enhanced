from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "name": query.get("name"),
    }
    return await request("/api/playlist/update/name", data, create_option(query))
