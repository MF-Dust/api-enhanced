from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "artistId": query.get("id"),
    }
    return await request("/api/rep/ugc/artist/get", data, create_option(query))
