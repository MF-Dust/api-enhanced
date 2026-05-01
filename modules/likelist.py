from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "uid": query.get("uid"),
    }
    return await request("/api/song/like/get", data, create_option(query))
