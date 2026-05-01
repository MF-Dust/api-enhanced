from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "songId": query.get("id"),
        "reason": query.get("reason", "好歌献给你"),
        "scene": "",
        "fromUserId": -1,
        "yunbeiNum": query.get("yunbeiNum", 10),
    }
    return await request(
        "/api/yunbei/rcmd/song/submit", data, create_option(query, "weapi")
    )
