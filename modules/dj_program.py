from option import create_option

from utils import to_boolean


async def handler(query: dict, request) -> dict:
    data = {
        "radioId": query.get("rid", ""),
        "limit": query.get("limit", 30),
        "offset": query.get("offset", 0),
        "asc": to_boolean(query.get("asc", False)),
    }
    return await request("/api/dj/program/byradio", data, create_option(query, "weapi"))
