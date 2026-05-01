from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "albumIds": query.get("ids", ""),
    }
    return await request(
        "/api/vipmall/albumproduct/album/query/sales",
        data,
        create_option(query, "weapi"),
    )
