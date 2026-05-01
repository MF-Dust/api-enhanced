from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "songId": query.get("id"),
    }
    return await request("/api/song/red/count", data, create_option(query))
