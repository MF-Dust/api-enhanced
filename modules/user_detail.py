import json
from option import create_option


async def handler(query: dict, request) -> dict:
    uid = query.get("uid", "")
    result = await request(f"/api/v1/user/detail/{uid}", {}, create_option(query, "weapi"))
    result_str = json.dumps(result).replace("avatarImgId_str", "avatarImgIdStr")
    return json.loads(result_str)
