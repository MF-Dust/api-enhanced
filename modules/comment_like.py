from option import create_option
from utils import is_one

import config as cfg


async def handler(query: dict, request) -> dict:
    t = "like" if is_one(query.get("t")) else "unlike"
    resource_type = cfg.RESOURCE_TYPE_MAP.get(str(query.get("type", 0)), "")
    data = {
        "threadId": resource_type + str(query.get("id", "")),
        "commentId": query.get("cid", ""),
    }
    if resource_type == "A_EV_2_":
        data["threadId"] = query.get("threadId", "")
    return await request(
        f"/api/v1/comment/{t}",
        data,
        create_option(query, "weapi"),
    )
