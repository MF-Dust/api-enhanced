from option import create_option


async def handler(query: dict, request) -> dict:
    type_map = {"new": 0, "hot": 1}
    qtype = query.get("type", "new")
    data = {
        "limit": query.get("limit", 100),
        "offset": query.get("offset", 0),
        "type": type_map.get(qtype, 0),
    }
    return await request("/api/djradio/toplist", data, create_option(query, "weapi"))
