from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "startTime": query.get("startTime"),
        "endTime": query.get("endTime"),
    }
    return await request(
        "/api/creator/musician/play/count/statistic/data/trend/get",
        data,
        create_option(query, "weapi"),
    )
