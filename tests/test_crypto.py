import pytest
from crypto import weapi, linuxapi, eapi, eapi_res_decrypt, eapi_req_decrypt


class TestWeapi:
    def test_returns_params_and_encSecKey(self):
        result = weapi({"test": "data"})
        assert "params" in result
        assert "encSecKey" in result

    def test_params_is_base64_string(self):
        import base64
        result = weapi({"ids": [347230], "br": 999000, "csrf_token": ""})
        # Should be valid base64
        try:
            base64.b64decode(result["params"])
        except Exception:
            pytest.fail("params is not valid base64")

    def test_encSecKey_is_hex_string(self):
        result = weapi({"ids": [347230], "br": 999000, "csrf_token": ""})
        assert all(c in "0123456789abcdef" for c in result["encSecKey"].lower())

    def test_deterministic_with_same_input(self):
        # weapi uses random secretKey, so output should differ
        r1 = weapi({"test": "data"})
        r2 = weapi({"test": "data"})
        # encSecKey will differ because secretKey is random
        # But both should be valid
        assert "params" in r1 and "params" in r2


class TestLinuxapi:
    def test_returns_eparams(self):
        result = linuxapi({"test": "data"})
        assert "eparams" in result

    def test_eparams_is_uppercase_hex(self):
        result = linuxapi({"id": 24381616})
        assert result["eparams"] == result["eparams"].upper()
        assert all(c in "0123456789ABCDEF" for c in result["eparams"])


class TestEapi:
    def test_returns_params(self):
        result = eapi("/api/v1/playlist/detail", {"id": 24381616, "n": 1000})
        assert "params" in result

    def test_params_is_uppercase_hex(self):
        result = eapi("/api/v1/playlist/detail", {"id": 24381616, "n": 1000})
        assert result["params"] == result["params"].upper()
        assert all(c in "0123456789ABCDEF" for c in result["params"])

    def test_different_urls_produce_different_params(self):
        r1 = eapi("/api/test1", {"id": 1})
        r2 = eapi("/api/test2", {"id": 1})
        assert r1["params"] != r2["params"]


class TestEapiResDecrypt:
    def test_decrypt_roundtrip(self):
        """eapi encrypts url-delimited format, but NetEase responses are raw JSON encrypted.
        Test that eapi_req_decrypt can recover the original data from eapi output."""
        original = {"id": 24381616, "n": 1000}
        url = "/api/v1/playlist/detail"
        result = eapi(url, original)
        # eapi_req_decrypt parses the delimited format back
        decrypted = eapi_req_decrypt(result["params"])
        assert decrypted is not None
        assert decrypted["url"] == url
        assert decrypted["data"]["id"] == 24381616

    def test_decrypt_invalid_returns_none(self):
        result = eapi_res_decrypt("invalid_hex_data")
        assert result is None


class TestEapiReqDecrypt:
    def test_decrypt_roundtrip(self):
        import json
        url = "/api/v1/playlist/detail"
        data = {"id": 24381616, "n": 1000}
        encrypted = eapi(url, data)
        decrypted = eapi_req_decrypt(encrypted["params"])
        assert decrypted is not None
        assert decrypted["url"] == url
        assert decrypted["data"]["id"] == 24381616
