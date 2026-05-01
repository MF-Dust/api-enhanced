from option import create_option
from utils import is_one


async def handler(query: dict, request) -> dict:
    t = "follow" if is_one(query.get("t")) else "delfollow"
    return await request(f"/api/user/{t}/{query.get('id')}", {}, create_option(query, "weapi"))
