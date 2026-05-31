from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "threadId": f"R_SO_4_{query.get('id')}",
        "commentId": query.get("cid"),
        "reason": query.get("reason"),
    }
    return await request("/api/report/reportcomment", data, create_option(query))
