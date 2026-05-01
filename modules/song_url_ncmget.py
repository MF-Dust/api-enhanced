import os

from option import create_option


async def handler(query: dict, request) -> dict:
    try:
        from unblockneteasemusic import match_id
        result = await match_id(query.get("id"), query.get("source"))
        proxy = os.environ.get("PROXY_URL", "")
        use_proxy = os.environ.get("ENABLE_PROXY", "false")
        if result.get("data", {}).get("url") and "kuwo" in result["data"]["url"]:
            result["proxyUrl"] = (
                proxy + result["data"]["url"] if use_proxy == "true" else result["data"]["url"]
            )
        return {
            "status": 200,
            "body": {
                "code": 200,
                "data": result.get("data", {}).get("url"),
                "proxyUrl": result.get("proxyUrl", ""),
            },
        }
    except Exception as e:
        return {
            "status": 500,
            "body": {
                "code": 500,
                "msg": str(e) or "unblock error",
                "data": [],
            },
        }
