from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 30),
        "offset": query.get("offset", 0),
    }
    return await request("/api/v1/cloud/get", data, create_option(query, "weapi"))
