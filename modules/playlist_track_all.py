from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "id": query.get("id"),
        "n": 100000,
        "s": query.get("s", 8),
    }
    limit = int(query.get("limit", 1000))
    offset = int(query.get("offset", 0))

    res = await request("/api/v6/playlist/detail", data, create_option(query))
    track_ids = res["body"]["playlist"]["trackIds"]
    sliced = track_ids[offset:offset + limit]
    c = "[" + ",".join(f'{{"id":{item["id"]}}}' for item in sliced) + "]"
    ids_data = {"c": c}
    return await request("/api/v3/song/detail", ids_data, create_option(query))
