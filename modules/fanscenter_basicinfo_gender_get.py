from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request("/api/fanscenter/basicinfo/gender/get", data, create_option(query))
