from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "r": query.get("r", 1080),
    }
    return await request(
        "/api/song/enhance/play/mv/url",
        data,
        create_option(query, "weapi"),
    )
