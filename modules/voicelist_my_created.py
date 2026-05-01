from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "limit": query.get("limit", 20),
    }
    return await request(
        "/api/social/my/created/voicelist/v1", data, create_option(query, "weapi")
    )
