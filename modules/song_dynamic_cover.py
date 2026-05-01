from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "songId": query.get("id"),
    }
    return await request("/api/songplay/dynamic-cover", data, create_option(query))
