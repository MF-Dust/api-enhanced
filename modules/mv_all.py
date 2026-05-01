import json

from option import create_option


async def handler(query: dict, request) -> dict:
    tags = json.dumps({
        "地区": query.get("area", "全部"),
        "类型": query.get("type", "全部"),
        "排序": query.get("order", "上升最快"),
    }, ensure_ascii=False)
    data = {
        "tags": tags,
        "offset": query.get("offset", 0),
        "total": "true",
        "limit": query.get("limit", 30),
    }
    return await request("/api/mv/all", data, create_option(query))
