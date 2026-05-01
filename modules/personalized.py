from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 30),
        "total": True,
        "n": 1000,
    }
    return await request(
        "/api/personalized/playlist",
        data,
        create_option(query, "weapi"),
    )
