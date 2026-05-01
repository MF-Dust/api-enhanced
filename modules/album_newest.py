from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        "/api/discovery/newAlbum", {}, create_option(query, "weapi")
    )
