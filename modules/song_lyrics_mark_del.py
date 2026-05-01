from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "markIds": query.get("id"),
    }
    return await request("/api/song/play/lyrics/mark/del", data, create_option(query))
