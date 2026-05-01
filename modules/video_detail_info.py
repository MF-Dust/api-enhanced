from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "threadid": f"R_VI_62_{query.get('vid')}",
        "composeliked": True,
    }
    return await request(
        "/api/comment/commentthread/info", data, create_option(query, "weapi")
    )
