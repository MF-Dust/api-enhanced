from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 20),
        "offset": query.get("offset", 0),
        "beforeTime": query.get("before", 0),
    }
    return await request(
        f"/api/v1/resource/comments/{query.get('threadId')}",
        data,
        create_option(query, "weapi"),
    )
