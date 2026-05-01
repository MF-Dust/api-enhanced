from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 20),
        "offset": query.get("offset", 0),
    }
    return await request(
        "/api/vipnewcenter/app/level/growth/details",
        data,
        create_option(query, "weapi"),
    )
