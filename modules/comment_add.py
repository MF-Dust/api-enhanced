from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "threadId": f"R_SO_4_{query.get('id')}",
        "content": query.get("content"),
        "resourceType": "0",
        "resourceId": "0",
        "expressionPicId": "-1",
        "bubbleId": "-1",
        "checkToken": "",
    }
    return await request("/api/resource/comments/add", data, create_option(query))
