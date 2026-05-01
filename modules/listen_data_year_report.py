from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/content/activity/listen/data/year/report",
        {},
        create_option(query),
    )
