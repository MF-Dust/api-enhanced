from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("evId"),
    }
    return await request("/api/event/delete", data, create_option(query, "weapi"))
