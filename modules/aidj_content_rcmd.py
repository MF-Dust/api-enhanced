import json
import time

from option import create_option


async def handler(query: dict, request) -> dict:
    ext_info = {}
    if query.get("latitude") is not None:
        ext_info["lbsInfoList"] = [
            {
                "lat": query.get("latitude"),
                "lon": query.get("longitude"),
                "time": int(time.time()),
            }
        ]
    ext_info["noAidjToAidj"] = False
    ext_info["lastRequestTimestamp"] = int(time.time() * 1000)
    ext_info["listenedTs"] = False
    data = {
        "extInfo": json.dumps(ext_info),
    }
    return await request("/api/aidj/content/rcmd/info", data, create_option(query))
