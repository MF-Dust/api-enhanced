from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request("/api/creator/user/access", data, create_option(query, "weapi"))
