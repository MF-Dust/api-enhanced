from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "keyword": query.get("keyword", ""),
    }
    return await request(
        "/api/search/pc/suggest/keyword/get",
        data,
        create_option(query),
    )
