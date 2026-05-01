from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 30),
        "offset": query.get("offset", 0),
        "total": True,
    }
    return await request(
        "/api/digitalAlbum/purchased",
        data,
        create_option(query, "weapi"),
    )
