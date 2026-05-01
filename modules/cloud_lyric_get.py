from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "userId": query.get("uid"),
        "songId": query.get("sid"),
        "lv": -1,
        "kv": -1,
    }
    return await request("/api/cloud/lyric/get", data, create_option(query, "eapi"))
