import logging
import os
import re
from io import BytesIO

from option import create_option

logger = logging.getLogger(__name__)


def _sanitize_filename(name: str) -> str:
    base = re.sub(r"\.[^.]+$", "", name)
    return base.replace(" ", "").replace(".", "_")


async def handler(query: dict, request) -> dict:
    from plugins.song_upload import song_upload

    song_file = query.get("songFile")
    if not song_file:
        return {
            "status": 500,
            "body": {
                "msg": "请上传音乐文件",
                "code": 500,
            },
        }

    filename = _sanitize_filename(song_file.get("name", "unknown.mp3"))
    bitrate = 999000

    file_data = song_file.get("data", b"")
    file_md5 = song_file.get("md5", "")
    file_size = song_file.get("size", len(file_data))

    try:
        res = await request(
            "/api/cloud/upload/check",
            {
                "bitrate": str(bitrate),
                "ext": "",
                "length": file_size,
                "md5": file_md5,
                "songId": "0",
                "version": 1,
            },
            create_option(query),
        )

        artist = ""
        album = ""
        song_name = ""

        try:
            import mutagen

            metadata = mutagen.File(BytesIO(file_data)) if file_data else None
            tags = metadata.tags if metadata else None
            if tags:
                title = tags.get("TIT2") or tags.get("\xa9nam") or tags.get("title")
                album_tag = tags.get("TALB") or tags.get("\xa9alb") or tags.get("album")
                artist_tag = tags.get("TPE1") or tags.get("\xa9ART") or tags.get("artist")
                if title:
                    song_name = str(title[0] if isinstance(title, list) else title)
                if album_tag:
                    album = str(album_tag[0] if isinstance(album_tag, list) else album_tag)
                if artist_tag:
                    artist = str(artist_tag[0] if isinstance(artist_tag, list) else artist_tag)
        except Exception as error:
            logger.info(f"元数据解析错误: {error}")

        token_res = await request(
            "/api/nos/token/alloc",
            {
                "bucket": "",
                "ext": filename.rsplit(".", 1)[-1] if "." in filename else "",
                "filename": filename,
                "local": False,
                "nos_product": 3,
                "type": "audio",
                "md5": file_md5,
            },
            create_option(query),
        )

        if not token_res.get("body", {}).get("result") or not token_res["body"]["result"].get("resourceId"):
            logger.error(f"Token分配失败: {token_res.get('body')}")
            return {
                "status": 500,
                "body": {
                    "code": 500,
                    "msg": "获取上传token失败",
                    "detail": token_res.get("body"),
                },
            }

        if res.get("body", {}).get("needUpload"):
            logger.info("需要上传，开始上传流程...")
            try:
                upload_info = await song_upload(query, request)
                logger.info(f"上传完成: {upload_info}")
            except Exception as upload_error:
                logger.error(f"上传失败: {upload_error}")
                return {
                    "status": 500,
                    "body": {
                        "code": 500,
                        "msg": "上传失败",
                    },
                }
        else:
            logger.info("文件已存在，跳过上传")

        res2 = await request(
            "/api/upload/cloud/info/v2",
            {
                "md5": file_md5,
                "songid": res.get("body", {}).get("songId"),
                "filename": song_file.get("name", filename),
                "song": song_name or filename,
                "album": album or "未知专辑",
                "artist": artist or "未知艺术家",
                "bitrate": str(bitrate),
                "resourceId": token_res["body"]["result"]["resourceId"],
            },
            create_option(query),
        )

        if res2.get("body", {}).get("code") != 200:
            logger.error(f"云盘信息上传失败: {res2.get('body')}")
            return {
                "status": res2.get("status", 500),
                "body": {
                    "code": res2.get("body", {}).get("code", 500),
                    "msg": res2.get("body", {}).get("msg", "上传云盘信息失败"),
                    "detail": res2.get("body"),
                },
            }

        res3 = await request(
            "/api/cloud/pub/v2",
            {"songid": res2.get("body", {}).get("songId")},
            create_option(query),
        )

        return {
            "status": 200,
            "body": {
                **res.get("body", {}),
                **res3.get("body", {}),
            },
            "cookie": res.get("cookie"),
        }
    except Exception as e:
        logger.error(f"云盘上传异常: {e}")
        return {
            "status": 500,
            "body": {
                "code": 500,
                "msg": str(e),
            },
        }
    finally:
        temp_path = song_file.get("tempFilePath") if isinstance(song_file, dict) else None
        if temp_path:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
