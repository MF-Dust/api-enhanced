from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request(
        "/api/nmusician/workbench/mission/stage/list",
        data,
        create_option(query, "weapi"),
    )
