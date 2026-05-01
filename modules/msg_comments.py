from option import create_option


async def handler(query: dict, request) -> dict:
    uid = query.get("uid")
    data = {
        "beforeTime": query.get("before", "-1"),
        "limit": query.get("limit", 30),
        "total": "true",
        "uid": uid,
    }
    return await request(
        f"/api/v1/user/comments/{uid}",
        data,
        create_option(query, "weapi"),
    )
