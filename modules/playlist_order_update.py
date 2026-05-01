from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "ids": query.get("ids"),
    }
    return await request(
        "/api/playlist/order/update",
        data,
        create_option(query, "weapi"),
    )
