import time

from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "startTime": query.get("startTime", int(time.time() * 1000)),
        "endTime": query.get("endTime", int(time.time() * 1000)),
    }
    return await request("/api/mcalendar/detail", data, create_option(query, "weapi"))
