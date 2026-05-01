import config as cfg
from option import create_option


async def handler(query: dict, request) -> dict:
    t = query.get("t")
    is_subscribe = str(t) == "1"
    path = "subscribe" if is_subscribe else "unsubscribe"
    data = {"id": query.get("id")}
    if is_subscribe:
        data["checkToken"] = query.get("checkToken", cfg.CHECK_TOKEN)
    query["checkToken"] = True  # 强制开启checkToken
    return await request(f"/api/playlist/{path}", data, create_option(query, "eapi"))
