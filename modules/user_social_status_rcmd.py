from option import create_option


async def handler(query: dict, request) -> dict:
    return await request("/api/social/user/status/rcmd", {}, create_option(query))
