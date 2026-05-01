from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "mvId": query.get("id"),
    }
    return await request("/api/rep/ugc/mv/get", data, create_option(query))
