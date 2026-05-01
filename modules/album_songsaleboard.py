from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "albumType": query.get("albumType", 0),  # 0为数字专辑,1为数字单曲
    }
    type_ = query.get("type", "daily")  # daily,week,year,total
    if type_ == "year":
        data["year"] = query.get("year")
    return await request(
        f"/api/feealbum/songsaleboard/{type_}/type",
        data,
        create_option(query, "weapi"),
    )
