from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "taskIds": query.get("ids"),
    }
    return await request(
        "/api/vipnewcenter/app/level/task/reward/get",
        data,
        create_option(query, "weapi"),
    )
