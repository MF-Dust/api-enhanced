from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request("/api/homepage/dragon/ball/static", data, create_option(query))
