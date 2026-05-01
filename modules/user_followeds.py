from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "userId": query.get("uid"),
        "time": "0",
        "limit": query.get("limit", 20),
        "offset": query.get("offset", 0),
        "getcounts": "true",
    }
    return await request(
        f"/api/user/getfolloweds/{query.get('uid')}",
        data,
        create_option(query),
    )
