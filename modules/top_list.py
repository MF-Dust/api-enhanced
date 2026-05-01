from option import create_option


async def handler(query: dict, request) -> dict:
    if query.get("idx"):
        return {
            "status": 500,
            "body": {
                "code": 500,
                "msg": "不支持此方式调用,只支持id调用",
            },
        }

    data = {
        "id": query.get("id"),
        "n": "500",
        "s": "0",
    }
    return await request("/api/playlist/v4/detail", data, create_option(query))
