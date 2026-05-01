from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/feedback/weblog",
        query.get("data", {}),
        create_option(query, "weapi"),
    )
