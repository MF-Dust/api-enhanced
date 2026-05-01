from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/music-vip-membership/front/vip/info",
        {"userId": query.get("uid", "")},
        create_option(query, "weapi"),
    )
