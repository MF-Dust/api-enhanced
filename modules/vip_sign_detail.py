from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "signDayTime": query.get("timestamp"),
        "type": "1",
    }
    return await request(
        "/api/vipnewcenter/app/level/user/checkin/history/detail",
        data,
        create_option(query, "eapi"),
    )
