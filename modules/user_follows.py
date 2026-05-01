from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "offset": query.get("offset", 0),
        "limit": query.get("limit", 30),
        "order": True,
    }
    return await request(
        f"/api/user/getfollows/{query.get('uid')}",
        data,
        create_option(query, "weapi"),
    )
