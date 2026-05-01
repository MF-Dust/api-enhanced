from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    for key, value in query.items():
        if key.startswith("/api/"):
            data[key] = value
    return await request("/api/batch", data, create_option(query))
