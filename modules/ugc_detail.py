from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "auditStatus": query.get("auditStatus", ""),
        "limit": query.get("limit", 10),
        "offset": query.get("offset", 0),
        "order": query.get("order", "desc"),
        "sortBy": query.get("sortBy", "createTime"),
        "type": query.get("type", 1),
    }
    return await request("/api/rep/ugc/detail", data, create_option(query, "weapi"))
