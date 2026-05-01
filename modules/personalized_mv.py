from option import create_option


async def handler(query: dict, request) -> dict:
    return await request("/api/personalized/mv", {}, create_option(query, "weapi"))
