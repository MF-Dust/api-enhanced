from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "bpm": query.get("bpm", 50),
    }
    return await request("/api/radio/sport/get", data, create_option(query))
