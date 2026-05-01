import json
from option import create_option
from utils import cookie_to_json


async def handler(query: dict, request) -> dict:
    uri = query.get("uri", "")
    data = {}
    try:
        raw_data = query.get("data")
        if isinstance(raw_data, str):
            data = json.loads(raw_data)
        elif isinstance(raw_data, dict):
            data = raw_data
        else:
            data = {}
        if isinstance(data.get("cookie"), str):
            data["cookie"] = cookie_to_json(data["cookie"])
            query["cookie"] = data["cookie"]
    except Exception:
        data = {}

    crypto = query.get("crypto", "")
    return await request(uri, data, create_option(query, crypto))
