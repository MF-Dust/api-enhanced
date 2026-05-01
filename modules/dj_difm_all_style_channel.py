from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "sources": query.get("sources", "[0]"),
    }
    return await request("/api/dj/difm/all/style/channel/v2", data, create_option(query))
