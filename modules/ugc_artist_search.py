from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "keyword": query.get("keyword"),
        "limit": query.get("limit", 40),
    }
    return await request("/api/rep/ugc/artist/search", data, create_option(query))
