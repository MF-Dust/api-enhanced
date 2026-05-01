from option import create_option


async def handler(query: dict, request) -> dict:
    id_list = query.get("id", "").replace(" ", "").split(",")
    data = {
        "songIds": id_list,
    }
    return await request("/api/v1/cloud/get/byids", data, create_option(query, "weapi"))
