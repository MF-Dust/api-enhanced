from option import create_option


async def handler(query: dict, request) -> dict:
    return await request("/api/search/defaultkeyword/get", {}, create_option(query))
