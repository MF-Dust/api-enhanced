"""
Cryptographic functions for NetEase Cloud Music API.

This module provides encryption and decryption functions for various
NetEase API encryption schemes: weapi, eapi, linuxapi, and xeapi.
"""

import hashlib
import hmac
import json
import os
import random
import re
import zlib
from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from config import (
    BASE62,
    EAPI_KEY,
    IV,
    LINUXAPI_KEY,
    PRESET_KEY,
    RSA_PUBLIC_KEY,
    XEAPI_SIGN_KEY,
    XEAPI_STATIC_KEY,
)


def _pad(text: bytes) -> bytes:
    """Apply PKCS7 padding to bytes."""
    pad_len = 16 - (len(text) % 16)
    return text + bytes([pad_len] * pad_len)


def _aes_cbc_encrypt(text: str, key: str, iv: str) -> str:
    """Encrypt text using AES-CBC mode."""
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    encrypted = cipher.encrypt(_pad(text.encode("utf-8")))
    return b64encode(encrypted).decode("utf-8")


def _aes_ecb_encrypt(text: str, key: str) -> str:
    """Encrypt text using AES-ECB mode, return hex string."""
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    encrypted = cipher.encrypt(_pad(text.encode("utf-8")))
    return encrypted.hex().upper()


def _aes_ecb_decrypt(ciphertext_hex: str, key: str) -> bytes:
    """Decrypt hex ciphertext using AES-ECB mode."""
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    encrypted = bytes.fromhex(ciphertext_hex)
    return cipher.decrypt(encrypted)


def aes_decrypt(ciphertext: str, key: str, iv: str = "", format: str = "base64") -> bytes:
    """
    AES-ECB decrypt with base64 or hex input.

    Args:
        ciphertext: Encrypted text in base64 or hex format
        key: Decryption key
        iv: Initialization vector (unused for ECB mode)
        format: Input format, either "base64" or "hex"

    Returns:
        Decrypted bytes
    """
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    if format == "base64":
        encrypted = b64decode(ciphertext)
    else:
        encrypted = bytes.fromhex(ciphertext)
    return cipher.decrypt(encrypted)


def _rsa_encrypt(text: str, public_key_pem: str) -> str:
    """Encrypt text using RSA public key (no padding)."""
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
    """
    Encrypt data using weapi encryption scheme.

    Args:
        data: Dictionary to encrypt

    Returns:
        Dictionary with 'params' and 'encSecKey' fields
    """
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
    """
    Encrypt data using linuxapi encryption scheme.

    Args:
        data: Dictionary to encrypt

    Returns:
        Dictionary with 'eparams' field
    """
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return {"eparams": _aes_ecb_encrypt(text, LINUXAPI_KEY)}


def eapi(url: str, data: dict) -> dict:
    """
    Encrypt data using eapi encryption scheme.

    Args:
        url: API endpoint URL
        data: Dictionary to encrypt

    Returns:
        Dictionary with 'params' field
    """
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    message = f"nobody{url}use{text}md5forencrypt"
    digest = hashlib.md5(message.encode("utf-8")).hexdigest()
    content = f"{url}-36cd479b6b5-{text}-36cd479b6b5-{digest}"
    return {"params": _aes_ecb_encrypt(content, EAPI_KEY)}


def eapi_res_decrypt(encrypted_params: str, aeapi: bool = False) -> dict | None:
    """
    Decrypt eapi response.

    Args:
        encrypted_params: Encrypted response parameters
        aeapi: Whether response is compressed with gzip

    Returns:
        Decrypted dictionary or None on error
    """
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
        from logger import log_error

        log_error("eapiResDecrypt error", exc=e)
        return None


def eapi_req_decrypt(encrypted_params: str) -> dict | None:
    """
    Decrypt eapi request parameters.

    Args:
        encrypted_params: Encrypted request parameters

    Returns:
        Dictionary with 'url' and 'data' fields, or None on error
    """
    try:
        decrypted = _aes_ecb_decrypt(encrypted_params, EAPI_KEY)
        # Remove PKCS7 padding
        pad_len = decrypted[-1]
        decrypted = decrypted[:-pad_len]
        text = decrypted.decode("utf-8")
        match = re.match(r"(.*?)-36cd479b6b5-(.*?)-36cd479b6b5-(.*)", text)
        if match:
            url = match.group(1)
            data = json.loads(match.group(2))
            return {"url": url, "data": data}
        return None
    except Exception as e:
        from logger import log_error

        log_error("eapiReqDecrypt error", exc=e)
        return None


# ============================================================
# xeapi encryption/decryption
# ============================================================


def _aes_ecb_encrypt_bytes(key: bytes, plaintext: bytes) -> bytes:
    """AES-ECB encrypt raw bytes (no hex encoding)."""
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(_pad(plaintext))


def _aes_ecb_decrypt_bytes(key: bytes, ciphertext: bytes) -> bytes:
    """AES-ECB decrypt raw bytes."""
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)


def _create_x25519_public_key(raw_key: bytes):
    """Create an X25519 public key from 32 raw bytes using SPKI format."""

    # RFC 8410 SPKI header for id-X25519
    spki_prefix = bytes.fromhex("302a300506032b656e032100")
    der = spki_prefix + raw_key
    from cryptography.hazmat.primitives.serialization import load_der_public_key

    return load_der_public_key(der)


def _derive_x25519_aes_key(shared_secret: bytes, ephemeral_public_key: bytes) -> bytes:
    """Derive AES key from X25519 shared secret using HKDF-like HMAC chain."""
    import hashlib

    prk = hmac.new(b"\x00" * 32, shared_secret, hashlib.sha256).digest()
    okm = hmac.new(prk, ephemeral_public_key + b"\x01", hashlib.sha256).digest()
    return okm[:16]


def xeapi_sign(timestamp: str, nonce: str) -> str:
    """
    Generate HMAC-SHA256 signature for xeapi.

    Args:
        timestamp: Timestamp string
        nonce: Random nonce string

    Returns:
        Base64-encoded signature
    """
    message = str(timestamp) + nonce
    sig = hmac.new(
        XEAPI_SIGN_KEY.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return b64encode(sig).decode("utf-8")


def xeapi_mid_transform(ciphertext: bytes) -> bytes:
    """
    Apply XOR and rotation transform for xeapi mid-layer.

    Args:
        ciphertext: Encrypted bytes to transform

    Returns:
        Transformed bytes
    """
    random_bytes = os.urandom(16)
    xored = bytearray(len(ciphertext))
    for i in range(len(ciphertext)):
        xored[i] = ciphertext[i] ^ random_bytes[i & 0x0F]
    b64 = b64encode(bytes(xored))
    rot = random_bytes[0] % len(b64) if len(b64) > 0 else 0
    return random_bytes + b64[rot:] + b64[:rot]


def xeapi_encrypt_s(dynamic_key: bytes, public_key_state: dict, os_name: str = "android") -> bytes:
    """
    Perform X25519 ECDH + AES-128-GCM encryption for xeapi S field.

    Args:
        dynamic_key: Dynamic encryption key
        public_key_state: Server public key state
        os_name: Operating system name

    Returns:
        Encrypted S field bytes
    """
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

    peer_raw = b64decode(public_key_state["publicKey"])
    peer_key = _create_x25519_public_key(peer_raw)

    private_key = X25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Export raw 32-byte ephemeral public key
    from cryptography.hazmat.primitives.serialization import (
        Encoding,
        PublicFormat,
    )

    ephemeral_der = public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    ephemeral_raw = ephemeral_der[-32:]

    shared_secret = private_key.exchange(peer_key)
    aes_key = _derive_x25519_aes_key(shared_secret, ephemeral_raw)

    iv = os.urandom(12)
    sk = public_key_state.get("sk", "")
    plaintext = f"{b64encode(dynamic_key).decode()}|{os_name}|{sk}".encode()

    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
    encrypted, tag = cipher.encrypt_and_digest(plaintext)

    return ephemeral_raw + iv + encrypted + tag


def build_xeapi_plaintext(uri: str, data: dict, options: dict | None = None) -> str:
    """
    Build JSON plaintext for xeapi encryption.

    Args:
        uri: API endpoint URI
        data: Request data dictionary
        options: Optional request options

    Returns:
        JSON string for encryption
    """
    options = options or {}
    fields = {}

    content_type = options.get("content_type", "application/x-www-form-urlencoded;charset=utf-8")
    media_type = content_type.split(";")[0].strip().lower()
    if media_type != "application/x-www-form-urlencoded":
        fields["contentType"] = content_type

    method = options.get("method", "POST").upper()
    if method != "POST":
        fields["method"] = method

    from urllib.parse import urlparse

    parsed = urlparse(uri if uri.startswith("http") else f"https://interface.music.163.com{uri}")
    if parsed.query:
        fields["queryString"] = parsed.query

    if data is not None:
        body_data = {k: v for k, v in data.items() if k != "e_r"}
        from urllib.parse import urlencode

        body = urlencode(body_data).encode("utf-8")
        fields["body"] = b64encode(body).decode("utf-8")

    if "queryString" in fields:
        fields["queryString"] += "&e_r=true"
    else:
        fields["queryString"] = "e_r=true"

    return json.dumps(fields, separators=(",", ":"))


def xeapi(uri: str, data: dict, options: dict | None = None) -> dict:
    """
    Perform full xeapi encryption.

    Args:
        uri: API endpoint URI
        data: Request data dictionary
        options: Optional encryption options including publicKeyState, sessionKey, sessionId

    Returns:
        Dictionary with B, S, R encrypted fields

    Raises:
        ValueError: If publicKeyState is not provided in options
    """
    options = options or {}
    public_key_state = options.get("publicKeyState")
    if not public_key_state:
        raise ValueError("xeapi publicKeyState is required")

    active_session_key = options.get("sessionKey")
    if active_session_key:
        if isinstance(active_session_key, str):
            active_session_key = active_session_key.encode("utf-8")
    else:
        active_session_key = None

    active_session_id = options.get("sessionId", "")
    dynamic_key = active_session_key or os.urandom(16)

    plaintext = build_xeapi_plaintext(uri, data, options).encode("utf-8")

    b = _aes_ecb_encrypt_bytes(
        dynamic_key,
        xeapi_mid_transform(_aes_ecb_encrypt_bytes(XEAPI_STATIC_KEY, plaintext)),
    )
    s = xeapi_encrypt_s(dynamic_key, public_key_state, options.get("os", "android"))
    r = _aes_ecb_encrypt_bytes(
        XEAPI_STATIC_KEY,
        f"{public_key_state.get('version', '')}|{active_session_id if active_session_key else ''}".encode(),
    )

    return {
        "B": b64encode(b).decode("utf-8"),
        "S": b64encode(s).decode("utf-8"),
        "R": b64encode(r).decode("utf-8"),
    }


def xeapi_res_decrypt(body: bytes) -> dict:
    """
    Decrypt xeapi response body.

    Args:
        body: Encrypted response body bytes

    Returns:
        Decrypted dictionary
    """
    decrypted = _aes_ecb_decrypt_bytes(EAPI_KEY.encode("utf-8"), body)
    # Check for gzip magic bytes
    if len(decrypted) >= 2 and decrypted[0] == 0x1F and decrypted[1] == 0x8B:
        decrypted = zlib.decompress(decrypted)
    return json.loads(decrypted.decode("utf-8"))


def xeapi_decrypt_public_key(encrypted_data: str) -> dict:
    """
    Decrypt xeapi public key received from server.

    Args:
        encrypted_data: Base64-encoded encrypted public key

    Returns:
        Decrypted public key dictionary
    """
    ciphertext = b64decode(encrypted_data)
    decrypted = _aes_ecb_decrypt_bytes(XEAPI_STATIC_KEY, ciphertext)
    return json.loads(decrypted.decode("utf-8"))
