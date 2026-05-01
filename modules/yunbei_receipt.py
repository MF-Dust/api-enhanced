from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 10),
        "offset": query.get("offset", 0),
    }
    return await request("/api/point/receipt", data, create_option(query))
