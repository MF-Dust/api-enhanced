from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "type": query.get("type", "song"),
        "msg": query.get("msg", ""),
        "id": query.get("id", ""),
    }
    return await request("/api/share/friends/resource", data, create_option(query))
