from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "s": query.get("keywords", ""),
    }
    type_ = "keyword" if query.get("type") == "mobile" else "web"
    return await request(
        f"/api/search/suggest/{type_}",
        data,
        create_option(query, "weapi"),
    )
