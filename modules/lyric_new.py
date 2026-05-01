from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "cp": False,
        "tv": 0,
        "lv": 0,
        "rv": 0,
        "kv": 0,
        "yv": 0,
        "ytv": 0,
        "yrv": 0,
    }
    return await request("/api/song/lyric/v1", data, create_option(query))
