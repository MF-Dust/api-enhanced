from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "taskType": "app_vip_task_center",
        "userId": query.get("id"),
    }
    return await request(
        "/api/middle/vip/mission/user/progress/list",
        data,
        create_option(query, "xeapi"),
    )
