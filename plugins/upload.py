import hashlib
import httpx
from option import create_option


async def image_upload(query: dict, request) -> dict:
    """Image upload to NetEase NOS storage."""
    img_file = query.get("imgFile", {})
    ext = img_file.get("name", "").rsplit(".", 1)[-1] if "." in img_file.get("name", "") else "jpg"
    bucket = "yyimgs"

    # Allocate upload token
    token_res = await request(
        "/api/nos/token/alloc",
        {
            "bucket": bucket,
            "ext": ext,
            "filename": img_file.get("name", "image.jpg"),
            "local": False,
            "nos_product": 3,
            "type": "image",
        },
        create_option(query, "weapi"),
    )

    if not token_res.get("body", {}).get("result", {}).get("objectKey"):
        return {
            "status": 500,
            "body": {"code": 500, "msg": "获取上传token失败", "detail": token_res.get("body")},
        }

    object_key = token_res["body"]["result"]["objectKey"].replace("/", "%2F")

    # Get LBS endpoint
    try:
        async with httpx.AsyncClient() as client:
            lbs_resp = await client.get(
                f"https://wanproxy.127.net/lbs?version=1.0&bucketname={bucket}",
                timeout=10.0,
            )
            lbs = lbs_resp.json()
    except Exception as e:
        return {
            "status": 500,
            "body": {"code": 500, "msg": "获取上传服务器地址失败", "detail": str(e)},
        }

    if not lbs.get("upload") or not lbs["upload"][0]:
        return {
            "status": 500,
            "body": {"code": 500, "msg": "获取上传服务器地址无效", "detail": lbs},
        }

    # Upload image
    upload_url = f"{lbs['upload'][0]}/{bucket}/{object_key}?offset=0&complete=true&version=1.0"
    file_data = img_file.get("data", b"")
    if hasattr(file_data, "read"):
        file_data = file_data.read()

    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                upload_url,
                content=file_data,
                headers={
                    "x-nos-token": token_res["body"]["result"]["token"],
                    "Content-Type": img_file.get("mimetype", "image/jpeg"),
                    "Content-Length": str(len(file_data)),
                },
                timeout=60.0,
            )
    except Exception as e:
        return {
            "status": 500,
            "body": {"code": 500, "msg": "图片上传失败", "detail": str(e)},
        }

    return token_res


async def upload(query: dict, request) -> dict:
    token_res = await image_upload(query, request)
    result = token_res.get("body", {}).get("result", {})
    return {
        "url_pre": "https://p1.music.126.net/" + result.get("objectKey", ""),
        "imgId": result.get("docId"),
    }
