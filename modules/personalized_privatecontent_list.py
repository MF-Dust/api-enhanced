from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "offset": query.get("offset", 0),
        "total": "true",
        "limit": query.get("limit", 60),
    }
    return await request(
        "/api/v2/privatecontent/list",
        data,
        create_option(query, "weapi"),
    )
