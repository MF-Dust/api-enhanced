from option import create_option

import config as cfg


async def handler(query: dict, request) -> dict:
    resource_type = cfg.RESOURCE_TYPE_MAP.get(str(query.get("type", 0)), "")
    thread_id = resource_type + str(query.get("sid", ""))
    data = {
        "targetUserId": query.get("uid", ""),
        "commentId": query.get("cid", ""),
        "cursor": query.get("cursor", "-1"),
        "threadId": thread_id,
        "pageNo": query.get("page", 1),
        "idCursor": query.get("idCursor", -1),
        "pageSize": query.get("pageSize", 100),
    }
    return await request(
        "/api/v2/resource/comments/hug/list",
        data,
        create_option(query),
    )
