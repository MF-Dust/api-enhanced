from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "keyword": query.get("keyword", ""),
        "scene": "normal",
        "limit": query.get("limit", "10"),
        "offset": query.get("offset", "30"),
        "e_r": True,
    }
    return await request("/api/search/voicelist/get", data, create_option(query))
