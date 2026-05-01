from option import create_option


async def handler(query: dict, request) -> dict:
    return await request("/api/playlist/catalogue", {}, create_option(query, "eapi"))
