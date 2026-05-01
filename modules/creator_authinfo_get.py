from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request("/api/user/creator/authinfo/get", data, create_option(query))
