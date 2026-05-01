from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", "100"),
        "offset": query.get("offset", "0"),
        "userId": query.get("uid", ""),
        "isWebview": "true",
        "includeRedHeart": "true",
        "includeTop": "true",
    }
    return await request("/api/user/playlist/create", data, create_option(query))
