import json
from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "logs": json.dumps([
            {
                "action": "play",
                "json": {
                    "download": 0,
                    "end": "playend",
                    "id": query.get("id"),
                    "sourceId": query.get("sourceid"),
                    "time": query.get("time"),
                    "type": "song",
                    "wifi": 0,
                    "source": "list",
                    "mainsite": 1,
                    "content": "",
                },
            },
        ]),
    }
    return await request("/api/feedback/weblog", data, create_option(query, "weapi"))
