from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "friendid": query.get("uid"),
    }
    return await request("/api/user/mutualfollow/get", data, create_option(query))
