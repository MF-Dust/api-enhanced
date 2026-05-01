from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "page": query.get("page", 0),
    }
    return await request(
        "/api/djradio/home/today/perfered",
        data,
        create_option(query, "weapi"),
    )
