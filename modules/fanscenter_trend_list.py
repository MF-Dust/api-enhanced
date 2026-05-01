import time
from option import create_option


async def handler(query: dict, request) -> dict:
    now = int(time.time() * 1000)
    data = {
        "startTime": query.get("startTime", now - 7 * 24 * 3600 * 1000),
        "endTime": query.get("endTime", now),
        "type": query.get("type", 0),
    }
    return await request("/api/fanscenter/trend/list", data, create_option(query))
