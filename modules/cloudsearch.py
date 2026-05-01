from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "s": query.get("keywords", ""),
        "type": query.get("type", 1),
        "limit": query.get("limit", 30),
        "offset": query.get("offset", 0),
        "total": True,
    }
    return await request("/api/cloudsearch/pc", data, create_option(query))
