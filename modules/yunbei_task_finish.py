from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "userTaskId": query.get("userTaskId"),
        "depositCode": query.get("depositCode", "0"),
    }
    return await request(
        "/api/usertool/task/point/receive", data, create_option(query, "weapi")
    )
