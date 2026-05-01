from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/djradio/category/excludehot",
        {},
        create_option(query, "weapi"),
    )
