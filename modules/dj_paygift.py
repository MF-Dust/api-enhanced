from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 30),
        "offset": query.get("offset", 0),
        "_nmclfl": 1,
    }
    return await request(
        "/api/djradio/home/paygift/list",
        data,
        create_option(query, "weapi"),
    )
