from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "type": "text",
        "msg": query.get("msg"),
        "userIds": "[" + str(query.get("user_ids", "")) + "]",
    }
    return await request("/api/msg/private/send", data, create_option(query))
