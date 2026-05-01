from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    return await request(
        "/api/nmusician/workbench/mission/cycle/list",
        data,
        create_option(query, "weapi"),
    )
