from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "tags": query.get("tags"),
    }
    return await request("/api/playlist/tags/update", data, create_option(query))
