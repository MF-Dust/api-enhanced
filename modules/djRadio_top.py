from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "djRadioId": query.get("djRadioId", None),
        "sortIndex": query.get("sortIndex", 1),
        "dataGapDays": query.get("dataGapDays", 7),
        "dataType": query.get("dataType", 3),
    }
    return await request(
        "/api/expert/worksdata/works/top/get",
        data,
        create_option(query),
    )
