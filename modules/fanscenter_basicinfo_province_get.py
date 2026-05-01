from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request("/api/fanscenter/basicinfo/province/get", data, create_option(query))
