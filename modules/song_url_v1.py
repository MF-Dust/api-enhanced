import os
from option import create_option
import config as cfg
from unblock import match_id


async def handler(query: dict, request) -> dict:
    data = {
        "ids": f"[{query.get('id', '')}]",
        "level": query.get("level", "standard"),
        "encodeType": "flac",
    }
    if query.get("unblock") == "true":
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
                    "msg": "Warning: Customizing unblock sources is not supported on this endpoint. Please use `/song/url/match` instead.",
                    "data": [{
                        "id": int(query.get("id", 0)),
                        "url": url,
                        "type": "flac",
                        "level": query.get("level", "standard"),
                        "freeTrialInfo": "null",
                        "fee": 0,
                        "proxyUrl": proxy_url,
                    }],
                },
                "cookie": [],
            }
        except Exception as e:
            return {
                "status": 500,
                "body": {"code": 500, "msg": str(e), "data": []},
            }
    if query.get("level") == "sky":
        data["immerseType"] = "c51"
    return await request("/api/song/enhance/player/url/v1", data, create_option(query))
