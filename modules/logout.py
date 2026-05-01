from option import create_option


async def handler(query: dict, request) -> dict:
    return await request("/api/logout", {}, create_option(query))
