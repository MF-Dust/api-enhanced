from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "rid": query.get("id", ""),
        "limit": query.get("limit", 20),
        "offset": query.get("offset", 0),
        "beforeTime": query.get("before", 0),
    }
    return await request(
        f"/api/v1/resource/comments/R_VI_62_{query.get('id', '')}",
        data,
        create_option(query, "weapi"),
    )
