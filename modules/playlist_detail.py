from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id", ""),
        "n": 100000,
        "s": query.get("s", 8),
    }
    return await request("/api/v6/playlist/detail", data, create_option(query))
