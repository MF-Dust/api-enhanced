from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "scene": "playlist_head",
        "playlistId": query.get("id"),
        "newStyle": "true",
    }
    return await request("/api/playlist/detail/rcmd/get", data, create_option(query))
