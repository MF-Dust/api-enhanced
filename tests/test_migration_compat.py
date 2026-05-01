import importlib
import asyncio
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import server


@pytest.fixture(autouse=True)
def clear_cache():
    server._response_cache.clear()


def test_module_name_parity_with_node_modules():
    root = Path(__file__).resolve().parents[2]
    js = {p.stem for p in (root / "module").glob("*.js")}
    py = {
        p.stem for p in (root / "PyNCMAPI" / "modules").glob("*.py")
        if p.stem != "__init__"
    }
    assert js == py


def test_special_routes_match_node_express_paths():
    client = TestClient(server.app)
    routes = {route.path for route in server.app.routes}
    assert "/fm_trash" in routes
    assert "/personal_fm" in routes
    assert "/ugc/user/devote" in routes
    assert client.get("/fm/trash").status_code == 404


def test_static_files_are_served_from_public_root():
    client = TestClient(server.app)
    response = client.get("/login.html")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_successful_api_responses_are_cached(monkeypatch):
    calls = []

    async def fake_request(url, data, options):
        calls.append((url, data, options))
        return {"status": 200, "body": {"code": 200, "calls": len(calls)}, "cookie": []}

    monkeypatch.setattr(server, "ncm_request", fake_request)
    client = TestClient(server.app)

    first = client.get("/album?id=cache-test")
    second = client.get("/album?id=cache-test")

    assert first.json() == {"code": 200, "calls": 1}
    assert second.json() == {"code": 200, "calls": 1}
    assert len(calls) == 1


def test_https_set_cookie_gets_samesite_secure(monkeypatch):
    async def fake_request(url, data, options):
        return {
            "status": 200,
            "body": {"code": 200},
            "cookie": ["MUSIC_U=abc; Path=/"],
        }

    monkeypatch.setattr(server, "ncm_request", fake_request)
    client = TestClient(server.app, base_url="https://testserver")

    response = client.get("/album?id=cookie-test")
    assert "SameSite=None; Secure" in response.headers["set-cookie"]


def test_multipart_upload_is_normalized_for_modules(monkeypatch):
    seen = {}

    async def fake_request(url, data, options):
        if url == "/api/playlist/cover/update":
            seen.update(data)
        return {
            "status": 200,
            "body": {"code": 200, "result": {"objectKey": "cover/key.jpg", "docId": "42", "token": "nos-token"}},
            "cookie": [],
        }

    class FakeResponse:
        def json(self):
            return {"upload": ["https://upload.example"]}

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, *args, **kwargs):
            return FakeResponse()

        async def post(self, *args, **kwargs):
            return FakeResponse()

    upload_mod = importlib.import_module("plugins.upload")
    monkeypatch.setattr(server, "ncm_request", fake_request)
    monkeypatch.setattr(upload_mod.httpx, "AsyncClient", FakeClient)

    client = TestClient(server.app)
    response = client.post(
        "/playlist/cover/update",
        data={"id": "123"},
        files={"imgFile": ("cover.jpg", b"image-bytes", "image/jpeg")},
    )

    assert response.status_code == 200
    assert seen == {"id": "123", "coverImgId": "42"}


def test_request_merges_custom_headers(monkeypatch):
    import request as request_mod

    captured = {}

    class FakeHeaders:
        def multi_items(self):
            return []

    class FakeResponse:
        status_code = 200
        headers = FakeHeaders()
        content = b'{"code":200}'
        text = '{"code":200}'

        def json(self):
            return {"code": 200}

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, target_url, content, headers):
            captured.update(headers)
            return FakeResponse()

    monkeypatch.setattr(request_mod.httpx, "AsyncClient", FakeClient)
    asyncio.run(
        request_mod.ncm_request(
            "/api/test",
            {"x": 1},
            {"crypto": "api", "headers": {"x-nos-token": "token"}},
        )
    )
    assert captured["x-nos-token"] == "token"


def test_package_entrypoint_exposes_module_callables(monkeypatch):
    root = Path(__file__).resolve().parents[2]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    import PyNCMAPI

    async def fake_request(url, data, options):
        return {"status": 200, "body": {"code": 200, "url": url}, "cookie": []}

    result = asyncio.run(PyNCMAPI.login_status({}, fake_request))
    assert result["body"]["data"]["url"] == "/api/w/nuser/account/get"
    assert PyNCMAPI.construct_server() is server.app
