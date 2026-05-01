from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request(
        "/api/vipnewcenter/app/user/sign/info",
        data,
        create_option(query, "weapi"),
    )
