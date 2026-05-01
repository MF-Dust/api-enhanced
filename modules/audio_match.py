import httpx

from option import create_option


async def handler(query: dict, request) -> dict:
    url = (
        f"https://interface.music.163.com/api/music/audio/match"
        f"?sessionId=0123456789abcdef&algorithmCode=shazam_v2"
        f"&duration={query.get('duration')}"
        f"&rawdata={query.get('audioFP')}"
        f"&times=1&decrypt=1"
    )
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=15.0)
        res_data = resp.json()
    return {
        "status": 200,
        "body": {
            "code": 200,
            "data": res_data.get("data"),
        },
    }
