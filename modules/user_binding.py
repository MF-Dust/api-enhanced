from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request(
        f"/api/v1/user/bindings/{query.get('uid')}",
        data,
        create_option(query, "weapi"),
    )
