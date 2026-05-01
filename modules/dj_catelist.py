from option import create_option


async def handler(query: dict, request) -> dict:
    return await request("/api/djradio/category/get", {}, create_option(query, "weapi"))
