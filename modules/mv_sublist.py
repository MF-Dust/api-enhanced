from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 25),
        "offset": query.get("offset", 0),
        "total": True,
    }
    return await request(
        "/api/cloudvideo/allvideo/sublist",
        data,
        create_option(query, "weapi"),
    )
