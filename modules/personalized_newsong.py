from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "type": "recommend",
        "limit": query.get("limit", 10),
        "areaId": query.get("areaId", 0),
    }
    return await request(
        "/api/personalized/newsong",
        data,
        create_option(query, "weapi"),
    )
