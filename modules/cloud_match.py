from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "userId": query.get("uid"),
        "songId": query.get("sid"),
        "adjustSongId": query.get("asid"),
    }
    return await request(
        "/api/cloud/user/song/match", data, create_option(query, "weapi")
    )
