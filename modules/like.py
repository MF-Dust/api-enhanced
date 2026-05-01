from option import create_option


async def handler(query: dict, request) -> dict:
    like = query.get("like", "true") != "false"
    data = {
        "alg": "itembased",
        "trackId": query.get("id"),
        "like": like,
        "time": "3",
    }
    return await request("/api/radio/like", data, create_option(query, "weapi"))
