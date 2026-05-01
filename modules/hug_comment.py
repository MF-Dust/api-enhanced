import config as cfg
from option import create_option


async def handler(query: dict, request) -> dict:
    resource_type_map = cfg.RESOURCE_TYPE_MAP
    resource_type = resource_type_map.get(str(query.get("type", 0)), "R_SO_4_")
    thread_id = resource_type + str(query.get("sid", ""))
    data = {
        "targetUserId": query.get("uid"),
        "commentId": query.get("cid"),
        "threadId": thread_id,
    }
    return await request(
        "/api/v2/resource/comments/hug/listener",
        data,
        create_option(query),
    )
