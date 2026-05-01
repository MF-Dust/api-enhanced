from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "br": int(query.get("br", 999000)),
    }
    return await request("/api/song/enhance/download/url", data, create_option(query))
