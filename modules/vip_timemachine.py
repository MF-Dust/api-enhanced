from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    if query.get("startTime") and query.get("endTime"):
        data["startTime"] = query.get("startTime")
        data["endTime"] = query.get("endTime")
        data["type"] = 1
        data["limit"] = query.get("limit", 60)
    return await request(
        "/api/vipmusic/newrecord/weekflow",
        data,
        create_option(query, "weapi"),
    )
