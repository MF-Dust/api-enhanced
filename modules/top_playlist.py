import json

from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "cat": query.get("cat", "全部"),
        "order": query.get("order", "hot"),
        "limit": query.get("limit", 50),
        "offset": query.get("offset", 0),
        "total": True,
    }
    res = await request("/api/playlist/list", data, create_option(query, "weapi"))
    result_str = json.dumps(res).replace("avatarImgId_str", "avatarImgIdStr")
    return json.loads(result_str)
