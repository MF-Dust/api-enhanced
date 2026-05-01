from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "nickname": query.get("nickname"),
    }
    return await request("/api/activate/initProfile", data, create_option(query))
