import time

from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 20),
        "startTimestamp": query.get("before", int(time.time() * 1000)),
    }
    return await request(
        "/api/sub/artist/new/works/mv/list", data, create_option(query, "weapi")
    )
