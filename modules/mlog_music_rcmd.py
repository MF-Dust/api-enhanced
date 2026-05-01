import json
from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("mvid", 0),
        "type": 2,
        "rcmdType": 20,
        "limit": query.get("limit", 10),
        "extInfo": json.dumps({"songId": query.get("songid")}),
    }
    return await request("/api/mlog/rcmd/feed/list", data, create_option(query))
