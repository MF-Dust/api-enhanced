from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "date": query.get("date", ""),
    }
    return await request(
        "/api/discovery/recommend/songs/history/detail",
        data,
        create_option(query, "weapi"),
    )
