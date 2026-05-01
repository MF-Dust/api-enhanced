from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "offset": query.get("offset", 0),
        "limit": query.get("limit", 30),
        "total": "true",
    }
    return await request("/api/forwards/get", data, create_option(query, "weapi"))
