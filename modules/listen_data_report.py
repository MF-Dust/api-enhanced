from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "type": query.get("type", "week"),
        "endTime": query.get("endTime"),
    }
    return await request(
        "/api/content/activity/listen/data/report",
        data,
        create_option(query),
    )
