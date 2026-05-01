from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "uid": query.get("uid"),
        "type": query.get("type", 0),
    }
    return await request("/api/v1/play/record", data, create_option(query, "weapi"))
