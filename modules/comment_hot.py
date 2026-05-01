from option import create_option

import config as cfg


async def handler(query: dict, request) -> dict:
    resource_type = cfg.RESOURCE_TYPE_MAP.get(str(query.get("type", 0)), "")
    data = {
        "rid": query.get("id", ""),
        "limit": query.get("limit", 20),
        "offset": query.get("offset", 0),
        "beforeTime": query.get("before", 0),
    }
    return await request(
        f"/api/v1/resource/hotcomments/{resource_type}{query.get('id', '')}",
        data,
        create_option(query, "weapi"),
    )
