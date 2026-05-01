from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "threadid": f"R_MV_5_{query.get('mvid')}",
        "composeliked": True,
    }
    return await request(
        "/api/comment/commentthread/info",
        data,
        create_option(query, "weapi"),
    )
