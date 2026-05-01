from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "artistId": query.get("id"),
        "limit": query.get("limit"),
        "offset": query.get("offset"),
        "total": True,
    }
    return await request("/api/artist/mvs", data, create_option(query, "weapi"))
