from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "getcounts": True,
        "time": query.get("lasttime", -1),
        "limit": query.get("limit", 30),
        "total": False,
    }
    return await request(f"/api/event/get/{query.get('uid')}", data, create_option(query))
