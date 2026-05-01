from option import create_option
from utils import is_one


async def handler(query: dict, request) -> dict:
    t = "false" if is_one(query.get("t")) else "true"
    data = {
        "contentType": "BROADCAST",
        "contentId": query.get("id"),
        "cancelCollect": t,
    }
    return await request(
        "/api/content/interact/collect", data, create_option(query)
    )
