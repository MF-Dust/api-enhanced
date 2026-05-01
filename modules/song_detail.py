from option import create_option


async def handler(query: dict, request) -> dict:
    ids = str(query.get("ids", "")).split(",")
    c = "[" + ",".join(f'{{"id":{id}}}' for id in ids) + "]"
    data = {"c": c}
    return await request("/api/v3/song/detail", data, create_option(query, "weapi"))
