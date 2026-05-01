from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 6),
    }
    return await request(
        "/api/djradio/personalize/rcmd",
        data,
        create_option(query, "weapi"),
    )
