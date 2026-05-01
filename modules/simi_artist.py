from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "artistid": query.get("id"),
    }
    return await request(
        "/api/discovery/simiArtist",
        data,
        create_option(query, "weapi"),
    )
