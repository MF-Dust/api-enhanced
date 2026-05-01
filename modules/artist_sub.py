from option import create_option
from utils import is_one


async def handler(query: dict, request) -> dict:
    t = "sub" if is_one(query.get("t")) else "unsub"
    data = {
        "artistId": query.get("id"),
        "artistIds": f"[{query.get('id')}]",
    }
    return await request(
        f"/api/artist/{t}", data, create_option(query, "weapi")
    )
