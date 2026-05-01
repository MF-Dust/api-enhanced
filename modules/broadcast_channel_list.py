from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "categoryId": query.get("categoryId", "0"),
        "regionId": query.get("regionId", "0"),
        "limit": query.get("limit", "20"),
        "lastId": query.get("lastId", "0"),
        "score": query.get("score", "-1"),
    }
    return await request(
        "/api/voice/broadcast/channel/list", data, create_option(query)
    )
