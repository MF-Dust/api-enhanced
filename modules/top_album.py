from datetime import datetime

from option import create_option


async def handler(query: dict, request) -> dict:
    now = datetime.now()
    data = {
        "area": query.get("area", "ALL"),
        "limit": query.get("limit", 50),
        "offset": query.get("offset", 0),
        "type": query.get("type", "new"),
        "year": query.get("year", now.year),
        "month": query.get("month", now.month),
        "total": False,
        "rcmd": True,
    }
    return await request(
        "/api/discovery/new/albums/area", data, create_option(query, "weapi")
    )
