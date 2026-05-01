from option import create_option


async def handler(query: dict, request) -> dict:
    return await request("/api/djradio/recommend/v1", {}, create_option(query, "weapi"))
