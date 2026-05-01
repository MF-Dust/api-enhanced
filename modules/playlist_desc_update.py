from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "desc": query.get("desc"),
    }
    return await request("/api/playlist/desc/update", data, create_option(query))
