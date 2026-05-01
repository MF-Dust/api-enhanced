from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 30),
        "offset": query.get("offset", 0),
        "total": True,
        "area": query.get("area", "ALL"),  # ALL:全部,ZH:华语,EA:欧美,KR:韩国,JP:日本
    }
    return await request("/api/album/new", data, create_option(query, "weapi"))
