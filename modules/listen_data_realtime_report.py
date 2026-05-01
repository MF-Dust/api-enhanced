from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "type": query.get("type", "week"),
    }
    return await request(
        "/api/content/activity/listen/data/realtime/report",
        data,
        create_option(query),
    )
