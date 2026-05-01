from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "resolution": query.get("res", 1080),
        "type": 1,
    }
    return await request("/api/mlog/detail/v1", data, create_option(query, "weapi"))
