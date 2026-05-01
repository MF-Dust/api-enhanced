from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 100),
    }
    return await request(
        "/api/play-record/song/list",
        data,
        create_option(query, "weapi"),
    )
