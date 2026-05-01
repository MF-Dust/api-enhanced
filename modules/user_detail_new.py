from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "all": "true",
        "userId": query.get("uid"),
    }
    res = await request(
        f"/api/w/v1/user/detail/{query.get('uid')}",
        data,
        create_option(query, "eapi"),
    )
    return res
