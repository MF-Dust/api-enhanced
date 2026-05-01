from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "forwards": query.get("forwards"),
        "id": query.get("evId"),
        "eventUserId": query.get("uid"),
    }
    return await request("/api/event/forward", data, create_option(query))
