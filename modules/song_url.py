import json
from option import create_option


async def handler(query: dict, request) -> dict:
    ids = str(query.get("id", "")).split(",")
    data = {
        "ids": json.dumps(ids),
        "br": int(query.get("br", 999000)),
    }
    result = await request("/api/song/enhance/player/url", data, create_option(query))
    items = result["body"].get("data", [])
    items.sort(key=lambda x: ids.index(str(x["id"])) if str(x["id"]) in ids else len(ids))
    return {"status": 200, "body": {"code": 200, "data": items}}
