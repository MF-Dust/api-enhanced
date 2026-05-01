from option import create_option


async def handler(query: dict, request) -> dict:
    type_map = {
        0: "pc",
        1: "android",
        2: "iphone",
        3: "ipad",
    }
    client_type = type_map.get(query.get("type", 0), "pc")
    return await request(
        "/api/v2/banner/get",
        {"clientType": client_type},
        create_option(query),
    )
