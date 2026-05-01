from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id", ""),
        "tv": -1,
        "lv": -1,
        "rv": -1,
        "kv": -1,
        "_nmclfl": 1,
    }
    return await request("/api/song/lyric", data, create_option(query))
