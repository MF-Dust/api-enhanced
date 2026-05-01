from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request(
        "/api/influencer/web/apply/threshold/detail/get",
        data,
        create_option(query),
    )
