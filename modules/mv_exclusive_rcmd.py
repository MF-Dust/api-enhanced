from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "offset": query.get("offset", 0),
        "limit": query.get("limit", 30),
    }
    return await request("/api/mv/exclusive/rcmd", data, create_option(query))
