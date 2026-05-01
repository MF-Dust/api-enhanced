from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "cat": query.get("cat", "全部"),
        "limit": query.get("limit", 50),
        "lasttime": query.get("before", 0),
        "total": True,
    }
    return await request(
        "/api/playlist/highquality/list", data, create_option(query, "weapi")
    )
