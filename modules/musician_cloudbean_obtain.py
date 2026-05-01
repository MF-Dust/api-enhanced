from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "userMissionId": query.get("id"),
        "period": query.get("period"),
    }
    return await request(
        "/api/nmusician/workbench/mission/reward/obtain/new",
        data,
        create_option(query, "weapi"),
    )
