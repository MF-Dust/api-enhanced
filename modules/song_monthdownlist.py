from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", "20"),
        "offset": query.get("offset", "0"),
        "total": "true",
    }
    return await request("/api/member/song/monthdownlist", data, create_option(query))
