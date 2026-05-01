from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/personalized/djprogram",
        {},
        create_option(query, "weapi"),
    )
