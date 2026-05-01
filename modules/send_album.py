from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "msg": query.get("msg", ""),
        "type": "album",
        "userIds": "[" + str(query.get("user_ids", "")) + "]",
    }
    return await request("/api/msg/private/send", data, create_option(query))
