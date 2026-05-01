from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "refresh": query.get("refresh", False),
        "cursor": query.get("cursor"),
    }
    return await request("/api/homepage/block/page", data, create_option(query, "weapi"))
