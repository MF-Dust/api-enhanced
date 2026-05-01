from option import create_option

import config as cfg


async def handler(query: dict, request) -> dict:
    resource_type = cfg.RESOURCE_TYPE_MAP.get(str(query.get("type", 0)), "")
    thread_id = resource_type + str(query.get("id", ""))
    page_size = query.get("pageSize", 20)
    page_no = query.get("pageNo", 1)
    sort_type = int(query.get("sortType", 99))
    if sort_type == 1:
        sort_type = 99

    cursor = ""
    if sort_type == 99:
        cursor = str((page_no - 1) * page_size)
    elif sort_type == 2:
        cursor = f"normalHot#{(page_no - 1) * page_size}"
    elif sort_type == 3:
        cursor = query.get("cursor", "0")

    data = {
        "threadId": thread_id,
        "pageNo": page_no,
        "showInner": query.get("showInner", True),
        "pageSize": page_size,
        "cursor": cursor,
        "sortType": sort_type,
    }
    return await request("/api/v2/resource/comments", data, create_option(query))
