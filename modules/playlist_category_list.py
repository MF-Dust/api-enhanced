from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "cat": query.get("cat", "全部"),
        "limit": query.get("limit", 24),
        "newStyle": True,
    }
    return await request("/api/playlist/category/list", data, create_option(query))
