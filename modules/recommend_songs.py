from option import create_option


async def handler(query: dict, request) -> dict:
    data = {"afresh": query.get("afresh")}
    return await request(
        "/api/v3/discovery/recommend/songs", data, create_option(query, "weapi")
    )
