from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "commentId": query.get("cid"),
        "threadId": f"R_SO_4_{query.get('id')}",
    }
    return await request(
        "/api/resource/comments/delete", data, create_option(query)
    )
