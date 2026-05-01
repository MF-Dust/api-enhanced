from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "ids": f"[{int(query.get('id', 0))}]",
        "br": int(query.get("br", 999000)),
    }
    response = await request(
        "/api/song/enhance/player/url", data, create_option(query, "weapi")
    )
    playable = False
    if response.get("body", {}).get("code") == 200:
        if response["body"]["data"][0].get("code") == 200:
            playable = True
    if playable:
        response["body"] = {"code": 200, "success": True, "message": "ok"}
    else:
        response["body"] = {"code": 200, "success": False, "message": "亲爱的,暂无版权"}
    return response
