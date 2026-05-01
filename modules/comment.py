import config as cfg
from option import create_option


async def handler(query: dict, request) -> dict:
    t_map = {
        1: "add",
        0: "delete",
        2: "reply",
    }
    t = t_map.get(query.get("t"))
    resource_type = cfg.RESOURCE_TYPE_MAP.get(str(query.get("type", "")), "")

    data = {
        "threadId": f"{resource_type}{query.get('id')}",
    }

    if resource_type == "A_EV_2_":
        data["threadId"] = query.get("threadId")

    if t == "add":
        data["content"] = query.get("content")
    elif t == "delete":
        data["commentId"] = query.get("commentId")
    elif t == "reply":
        data["commentId"] = query.get("commentId")
        data["content"] = query.get("content")

    return await request(
        f"/api/resource/comments/{t}",
        data,
        create_option(query, "weapi"),
    )
