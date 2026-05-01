import json

from option import create_option

import config as cfg


def _get_resource_type_id_map() -> dict:
    result = {}
    for key, prefix in cfg.RESOURCE_TYPE_MAP.items():
        stripped = prefix.rstrip("_")
        result[key] = stripped.split("_")[-1]
    return result


RESOURCE_TYPE_ID_MAP = _get_resource_type_id_map()


async def handler(query: dict, request) -> dict:
    ids_raw = str(query.get("ids", query.get("id", "")))
    ids = [id.strip() for id in ids_raw.split(",") if id.strip()]
    data = {
        "resourceType": RESOURCE_TYPE_ID_MAP.get(str(query.get("type", 0)), ""),
        "resourceIds": json.dumps(ids),
    }
    return await request(
        "/api/resource/commentInfo/list",
        data,
        create_option(query, "weapi"),
    )
