from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request("/api/v1/user/info", data, create_option(query, "weapi"))
