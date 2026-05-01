from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "type": query.get("type", 1),
        "s": query.get("keywords", ""),
    }
    return await request(
        "/api/search/suggest/multimatch",
        data,
        create_option(query, "weapi"),
    )
