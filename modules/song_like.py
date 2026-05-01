from option import create_option


async def handler(query: dict, request) -> dict:
    like = query.get("like", "true") != "false"
    data = {
        "trackId": query.get("id", ""),
        "userid": query.get("uid", ""),
        "like": like,
    }
    return await request("/api/song/like", data, create_option(query))
