from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "mlogId": query.get("id"),
    }
    return await request(
        "/api/mlog/video/convert/id",
        data,
        create_option(query, "weapi"),
    )
