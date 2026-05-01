from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 10),
        "offset": query.get("offset", 0),
    }
    return await request(
        "/api/song/play/lyrics/mark/user/page",
        data,
        create_option(query),
    )
