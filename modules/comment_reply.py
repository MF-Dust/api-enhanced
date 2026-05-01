from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "threadId": query.get("id", ""),
        "commentId": query.get("commentId", ""),
        "content": query.get("content", ""),
        "resourceType": "0",
        "resourceId": "0",
    }
    return await request("/api/v1/resource/comments/reply", data, create_option(query))
