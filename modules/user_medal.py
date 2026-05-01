from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/medal/user/page",
        {"uid": query.get("uid")},
        create_option(query),
    )
