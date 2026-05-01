from option import create_option


async def handler(query: dict, request) -> dict:
    initial = query.get("initial")
    if initial is not None:
        if isinstance(initial, str) and not initial.isdigit():
            initial = ord(initial.upper()) if initial else None
        else:
            initial = int(initial)
    data = {
        "initial": initial,
        "offset": query.get("offset", 0),
        "limit": query.get("limit", 30),
        "total": True,
        "type": query.get("type", "1"),
        "area": query.get("area"),
    }
    return await request(
        "/api/v1/artist/list", data, create_option(query, "weapi")
    )
