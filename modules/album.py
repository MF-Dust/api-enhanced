from option import create_option


async def handler(query: dict, request) -> dict:
    return await request(
        f"/api/v1/album/{query.get('id')}", {}, create_option(query, "weapi")
    )
