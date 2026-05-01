from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "compose_reminder": "true",
        "compose_hot_comment": "true",
        "limit": query.get("limit", 10),
        "user_id": query.get("uid"),
        "time": query.get("time", 0),
    }
    return await request(
        "/api/comment/user/comment/history", data, create_option(query, "weapi")
    )
