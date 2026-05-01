from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request(
        "/api/discovery/recommend/songs/history/recent",
        data,
        create_option(query, "weapi"),
    )
