import json

from option import create_option


async def handler(query: dict, request) -> dict:
    size = query.get("size", 30)
    cursor = query.get("cursor", 0)
    scene = query.get("scene", 0)
    data = {
        "authority": "false",
        "page": json.dumps({
            "size": size,
            "cursor": cursor,
        }),
        "scene": scene,
        "size": size,
        "sortType": "0",
    }
    return await request(
        "/api/user/follow/users/mixed/get/v2",
        data,
        create_option(query),
    )
