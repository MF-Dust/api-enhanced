from option import create_option


async def handler(query: dict, request) -> dict:
    return await request("/api/social/user/status/support", {}, create_option(query))
