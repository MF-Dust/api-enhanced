from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "name": query.get("name", ""),
        "privacy": query.get("privacy", "0"),
        "type": query.get("type", "NORMAL"),
    }
    return await request("/api/playlist/create", data, create_option(query, "weapi"))
