from option import create_option
from utils import is_one


async def handler(query: dict, request) -> dict:
    t = "sub" if is_one(query.get("t")) else "unsub"
    data = {
        "id": query.get("id"),
    }
    return await request(
        f"/api/cloudvideo/video/{t}", data, create_option(query, "weapi")
    )
