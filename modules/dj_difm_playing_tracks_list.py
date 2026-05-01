from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 5),
        "source": query.get("source", 0),
        "channelId": query.get("channelId", ""),
    }
    return await request("/api/dj/difm/playing/tracks/list", data, create_option(query))
