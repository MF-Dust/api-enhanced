from option import create_option


async def handler(query: dict, request) -> dict:
    t = "sub" if str(query.get("t")) == "1" else "unsub"
    data = {
        "mvId": query.get("mvid"),
        "mvIds": f'["{query.get("mvid")}"]',
    }
    return await request(f"/api/mv/{t}", data, create_option(query, "weapi"))
