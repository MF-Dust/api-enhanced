import hashlib
import json
import random
import zlib
from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long

from config import BASE62, EAPI_KEY, IV, LINUXAPI_KEY, PRESET_KEY, RSA_PUBLIC_KEY


def _pad(text: bytes) -> bytes:
    pad_len = 16 - (len(text) % 16)
    return text + bytes([pad_len] * pad_len)


def _aes_cbc_encrypt(text: str, key: str, iv: str) -> str:
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    encrypted = cipher.encrypt(_pad(text.encode("utf-8")))
    return b64encode(encrypted).decode("utf-8")


def _aes_ecb_encrypt(text: str, key: str) -> str:
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    encrypted = cipher.encrypt(_pad(text.encode("utf-8")))
    return encrypted.hex().upper()


def _aes_ecb_decrypt(ciphertext_hex: str, key: str) -> bytes:
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    encrypted = bytes.fromhex(ciphertext_hex)
    return cipher.decrypt(encrypted)


def _rsa_encrypt(text: str, public_key_pem: str) -> str:
    key = RSA.import_key(public_key_pem)
    n = key.n
    # Raw RSA: text^e mod n, no padding
    text_int = int.from_bytes(text.encode("utf-8"), "big")
    encrypted_int = pow(text_int, key.e, n)
    # Convert to hex, padded to key size
    byte_len = (key.size_in_bits() + 7) // 8
    encrypted_bytes = encrypted_int.to_bytes(byte_len, "big")
    return encrypted_bytes.hex()


def weapi(data: dict) -> dict:
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    secret_key = "".join(random.choice(BASE62) for _ in range(16))
    # First AES-CBC pass with preset key
    first_pass = _aes_cbc_encrypt(text, PRESET_KEY, IV)
    # Second AES-CBC pass with random key
    params = _aes_cbc_encrypt(first_pass, secret_key, IV)
    # RSA encrypt reversed secret key
    enc_sec_key = _rsa_encrypt(secret_key[::-1], RSA_PUBLIC_KEY)
    return {"params": params, "encSecKey": enc_sec_key}


def linuxapi(data: dict) -> dict:
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return {"eparams": _aes_ecb_encrypt(text, LINUXAPI_KEY)}


def eapi(url: str, data: dict) -> dict:
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    message = f"nobody{url}use{text}md5forencrypt"
    digest = hashlib.md5(message.encode("utf-8")).hexdigest()
    content = f"{url}-36cd479b6b5-{text}-36cd479b6b5-{digest}"
    return {"params": _aes_ecb_encrypt(content, EAPI_KEY)}


def eapi_res_decrypt(encrypted_params: str, aeapi: bool = False):
    try:
        decrypted = _aes_ecb_decrypt(encrypted_params, EAPI_KEY)
        if aeapi:
            decompressed = zlib.decompress(decrypted)
            return json.loads(decompressed)
        else:
            # Remove PKCS7 padding
            pad_len = decrypted[-1]
            decrypted = decrypted[:-pad_len]
            return json.loads(decrypted.decode("utf-8"))
    except Exception as e:
        print(f"eapiResDecrypt error: {e}")
        return None


def eapi_req_decrypt(encrypted_params: str):
    try:
        decrypted = _aes_ecb_decrypt(encrypted_params, EAPI_KEY)
        # Remove PKCS7 padding
        pad_len = decrypted[-1]
        decrypted = decrypted[:-pad_len]
        text = decrypted.decode("utf-8")
        import re
        match = re.match(r"(.*?)-36cd479b6b5-(.*?)-36cd479b6b5-(.*)", text)
        if match:
            url = match.group(1)
            data = json.loads(match.group(2))
            return {"url": url, "data": data}
        return None
    except Exception as e:
        print(f"eapiReqDecrypt error: {e}")
        return None
