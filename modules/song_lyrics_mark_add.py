from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "songId": query.get("id"),
        "markId": query.get("markId", ""),
        "data": query.get("data", "[]"),
    }
    return await request("/api/song/play/lyrics/mark/add", data, create_option(query))
