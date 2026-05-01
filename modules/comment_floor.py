from option import create_option

import config as cfg


async def handler(query: dict, request) -> dict:
    resource_type = cfg.RESOURCE_TYPE_MAP.get(str(query.get("type", 0)), "")
    data = {
        "parentCommentId": query.get("parentCommentId", ""),
        "threadId": resource_type + str(query.get("id", "")),
        "time": query.get("time", -1),
        "limit": query.get("limit", 20),
    }
    return await request(
        "/api/resource/comment/floor/get",
        data,
        create_option(query, "weapi"),
    )
