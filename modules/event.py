from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "pagesize": query.get("pagesize", 20),
        "lasttime": query.get("lasttime", -1),
    }
    return await request("/api/v1/event/get", data, create_option(query, "weapi"))
