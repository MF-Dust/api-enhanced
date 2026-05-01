from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id", ""),
    }
    return await request(
        "/api/vipmall/albumproduct/detail",
        data,
        create_option(query, "weapi"),
    )
