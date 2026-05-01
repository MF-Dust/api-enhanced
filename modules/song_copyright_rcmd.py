from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "songid": query.get("songid", query.get("id")),
    }
    return await request("/api/song/copyright/rcmd", data, create_option(query, "eapi"))
