from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "trackIds": query.get("ids"),
    }
    return await request("/api/song/like/check", data, create_option(query))
