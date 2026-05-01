from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/social/user/status",
        {"visitorId": query.get("uid")},
        create_option(query),
    )
