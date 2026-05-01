from option import create_option


async def handler(query: dict, request) -> dict:
    data = {}
    key = "userdata" if query.get("year") in ["2017", "2018", "2019"] else "data"
    return await request(
        f"/api/activity/summary/annual/{query.get('year')}/{key}",
        data,
        create_option(query),
    )
