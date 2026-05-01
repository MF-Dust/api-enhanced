from option import create_option


async def handler(query: dict, request) -> dict:
    if str(query.get("type", "")) == "2000":
        data = {
            "keyword": query.get("keywords", ""),
            "scene": "normal",
            "limit": query.get("limit", 30),
            "offset": query.get("offset", 0),
        }
        return await request("/api/search/voice/get", data, create_option(query))

    data = {
        "s": query.get("keywords", ""),
        "type": query.get("type", 1),
        "limit": query.get("limit", 30),
        "offset": query.get("offset", 0),
    }
    return await request("/api/search/get", data, create_option(query))
