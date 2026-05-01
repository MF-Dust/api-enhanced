from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "areaId": query.get("type", 0),
        "total": True,
    }
    return await request(
        "/api/v1/discovery/new/songs", data, create_option(query, "weapi")
    )
