from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "userId": query.get("uid"),
    }
    return await request("/api/djradio/get/byuser", data, create_option(query, "weapi"))
