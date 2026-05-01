from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "resId": query.get("id"),
        "resType": 4,
        "sceneType": 1,
    }
    return await request(
        "/api/v2/discovery/recommend/dislike",
        data,
        create_option(query, "weapi"),
    )
