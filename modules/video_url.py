from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "ids": f'["{query.get("id")}"]',
        "resolution": query.get("res", 1080),
    }
    return await request("/api/cloudvideo/playurl", data, create_option(query, "weapi"))
