from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "time": query.get("time", "-1"),
        "limit": query.get("limit", "12"),
    }
    return await request(
        "/api/mlog/playlist/mylike/bytime/get",
        data,
        create_option(query, "weapi"),
    )
