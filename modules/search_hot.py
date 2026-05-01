from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "type": 1111,
    }
    return await request("/api/search/hot", data, create_option(query))
