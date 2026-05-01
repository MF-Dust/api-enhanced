from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "songId": query.get("id"),
    }
    return await request("/api/rep/ugc/song/get", data, create_option(query))
