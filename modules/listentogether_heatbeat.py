from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "roomId": query.get("roomId"),
        "songId": query.get("songId"),
        "playStatus": query.get("playStatus"),
        "progress": query.get("progress"),
    }
    return await request("/api/listen/together/heartbeat", data, create_option(query))
