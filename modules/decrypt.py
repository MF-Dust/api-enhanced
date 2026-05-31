from base64 import b64decode

from crypto import eapi_req_decrypt, eapi_res_decrypt, aes_decrypt, xeapi_res_decrypt

LINUXAPI_KEY = "rFgB&h#%2?^eDg:Q"


async def handler(query: dict, request) -> dict:
    crypto = query.get("crypto", "eapi")
    data = query.get("data") or query.get("hexString", "")
    is_req = query.get("isReq", "true") != "false"

    if not data:
        return {
            "status": 400,
            "body": {"code": 400, "message": "data is required"},
        }

    try:
        if crypto == "eapi":
            pure_hex = data.replace(" ", "")
            result = eapi_req_decrypt(pure_hex) if is_req else eapi_res_decrypt(pure_hex)

        elif crypto == "weapi":
            if is_req:
                return {
                    "status": 400,
                    "body": {
                        "code": 400,
                        "message": (
                            "weapi 请求解密需要 RSA 私钥，暂不支持；"
                            "仅支持 weapi 返回数据解密（e_r=true 时与 eapi 相同）"
                        ),
                    },
                }
            pure_hex = data.replace(" ", "")
            result = eapi_res_decrypt(pure_hex)

        elif crypto == "linuxapi":
            if is_req:
                pure_hex = data.replace(" ", "")
                decrypted = aes_decrypt(pure_hex, LINUXAPI_KEY, "", "hex")
                import json
                result = json.loads(decrypted.decode("utf-8"))
            else:
                import json
                result = json.loads(data) if isinstance(data, str) else data

        elif crypto == "xeapi":
            if is_req:
                return {
                    "status": 400,
                    "body": {
                        "code": 400,
                        "message": (
                            "xeapi 请求解密涉及 X25519 ECDH 密钥交换，流程复杂，暂不支持；"
                            "仅支持 xeapi 返回数据解密"
                        ),
                    },
                }
            buf = b64decode(data)
            result = xeapi_res_decrypt(buf)

        elif crypto == "api":
            import json
            result = json.loads(data) if isinstance(data, str) else data

        else:
            return {
                "status": 400,
                "body": {"code": 400, "message": f"未知加密方式: {crypto}"},
            }

        return {
            "status": 200,
            "body": {"code": 200, "data": result},
        }
    except Exception as e:
        return {
            "status": 400,
            "body": {"code": 400, "message": f"解密失败: {e}"},
        }
