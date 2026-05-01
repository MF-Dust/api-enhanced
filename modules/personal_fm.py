from option import create_option


async def handler(query: dict, request) -> dict:
    return await request("/api/v1/radio/get", {}, create_option(query, "weapi"))
