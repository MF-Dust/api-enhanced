from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "roomId": query.get("roomId"),
    }
    return await request("/api/listen/together/end/v2", data, create_option(query))
