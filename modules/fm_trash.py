from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "songId": query.get("id"),
        "alg": "RT",
        "time": query.get("time", 25),
    }
    return await request("/api/radio/trash/add", data, create_option(query, "weapi"))
