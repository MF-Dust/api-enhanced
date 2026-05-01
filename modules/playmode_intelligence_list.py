from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "songId": query.get("id", ""),
        "type": "fromPlayOne",
        "playlistId": query.get("pid", ""),
        "startMusicId": query.get("sid") or query.get("id", ""),
        "count": query.get("count", 1),
    }
    return await request("/api/playmode/intelligence/list", data, create_option(query))
