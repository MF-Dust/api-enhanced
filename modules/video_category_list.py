from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "offset": query.get("offset", 0),
        "total": "true",
        "limit": query.get("limit", 99),
    }
    return await request(
        "/api/cloudvideo/category/list", data, create_option(query, "weapi")
    )
