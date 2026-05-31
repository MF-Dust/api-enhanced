from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "type": "0",
    }
    return await request(
        "/api/vipnewcenter/app/minidesk/music/sign/pc",
        data,
        create_option(query, "xeapi"),
    )
