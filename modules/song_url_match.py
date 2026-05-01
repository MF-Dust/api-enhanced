import config as cfg
from unblock import match_id, UnblockUnavailable


async def handler(query: dict, request) -> dict:
    try:
        result = await match_id(query.get("id"), query.get("source"))
        url = result.get("data", {}).get("url", "")
        proxy_url = ""
        if url and "kuwo" in url:
            proxy_url = cfg.PROXY_URL + url if cfg.ENABLE_PROXY == "true" and cfg.PROXY_URL else url
        return {
            "status": 200,
            "body": {
                "code": 200,
                "data": url,
                "proxyUrl": proxy_url,
            },
        }
    except UnblockUnavailable as e:
        return {
            "status": 500,
            "body": {
                "code": 500,
                "msg": str(e) or "unblock error",
                "data": [],
            },
        }
