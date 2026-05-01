import importlib
import json
import hashlib
import re
import tempfile
import time
from pathlib import Path
from urllib.parse import unquote

from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

import config as cfg
from utils import cookie_to_json
from request import ncm_request, RequestError

app = FastAPI(title="PyNCMAPI", version="0.1.0")

# Cache for API responses
_response_cache: dict[str, tuple[float, dict]] = {}
CACHE_TTL = 120  # 2 minutes


def _get_cache_key(request: Request, cookies: dict) -> str:
    return f"{request.url.hostname}{request.url.path}?{request.url.query}{json.dumps(cookies, sort_keys=True)}"


def _get_cached(cache_key: str) -> dict | None:
    if cache_key in _response_cache:
        ts, data = _response_cache[cache_key]
        if time.time() - ts < CACHE_TTL:
            return data
        del _response_cache[cache_key]
    return None


def _set_cache(cache_key: str, data: dict):
    _response_cache[cache_key] = (time.time(), data)


def _cacheable_request(request: Request) -> bool:
    content_type = request.headers.get("content-type", "")
    return "multipart/form-data" not in content_type


def _https_cookie(request: Request, cookie: str) -> str:
    if request.url.scheme == "https" and "samesite=" not in cookie.lower():
        return f"{cookie}; SameSite=None; Secure"
    return cookie


# CORS middleware
def _parse_cors_origins(cors_str: str) -> list[str] | None:
    if not cors_str:
        return None
    origins = [o.strip() for o in cors_str.split(",") if o.strip()]
    return origins if origins else None


_cors_origins = _parse_cors_origins(cfg.CORS_ALLOW_ORIGIN)


@app.middleware("http")
async def cors_and_cache_middleware(request: Request, call_next):
    path = request.url.path
    public_candidate = (Path(__file__).parent / "public" / path.lstrip("/")).resolve()
    public_root = (Path(__file__).parent / "public").resolve()

    # Skip static files
    if (
        path == "/"
        or "." in path.split("/")[-1]
        or (public_root == public_candidate or public_root in public_candidate.parents)
        and (public_candidate.is_file() or (public_candidate / "index.html").is_file())
    ):
        return await call_next(request)

    # CORS headers
    origin = request.headers.get("origin")
    if _cors_origins:
        if "*" in _cors_origins:
            allow_origin = "*"
        elif origin and origin in _cors_origins:
            allow_origin = origin
        else:
            allow_origin = None
    else:
        allow_origin = origin or "*"

    # Handle OPTIONS preflight
    if request.method == "OPTIONS":
        response = Response(status_code=204)
        if allow_origin:
            response.headers["Access-Control-Allow-Origin"] = allow_origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "X-Requested-With,Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "PUT,POST,GET,DELETE,OPTIONS"
        return response

    response = await call_next(request)

    if allow_origin:
        response.headers["Access-Control-Allow-Origin"] = allow_origin
        if allow_origin != "*":
            response.headers["Vary"] = "Origin"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json; charset=utf-8"

    return response


# Parse cookies from Cookie header
def _parse_cookies(request: Request) -> dict:
    cookie_header = request.headers.get("cookie", "")
    if not cookie_header:
        return {}
    result = {}
    for pair in re.split(r";\s+|\s+$", cookie_header):
        if not pair:
            continue
        idx = pair.find("=")
        if idx < 1 or idx == len(pair) - 1:
            continue
        key = unquote(pair[:idx]).strip()
        value = unquote(pair[idx + 1:]).strip()
        result[key] = value
    return result


# Load module definitions
SPECIAL_ROUTES = {
    "daily_signin": "/daily_signin",
    "fm_trash": "/fm_trash",
    "personal_fm": "/personal_fm",
}


def _filename_to_route(filename: str) -> str:
    name = filename.replace(".py", "")
    if name in SPECIAL_ROUTES:
        return SPECIAL_ROUTES[name]
    return "/" + name.replace("_", "/")


async def _upload_to_file_dict(upload) -> dict:
    data = await upload.read()
    await upload.seek(0)
    suffix = Path(upload.filename or "").suffix
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        tmp.write(data)
        temp_path = tmp.name
    finally:
        tmp.close()
    return {
        "name": upload.filename or "upload",
        "mimetype": upload.content_type or "application/octet-stream",
        "data": data,
        "size": len(data),
        "md5": hashlib.md5(data).hexdigest(),
        "tempFilePath": temp_path,
    }


async def _normalize_form(form) -> dict:
    body = {}
    for key, value in form.multi_items():
        if hasattr(value, "filename") and hasattr(value, "read"):
            body[key] = await _upload_to_file_dict(value)
        else:
            body[key] = value
    return body


def _load_modules():
    modules_dir = Path(__file__).parent / "modules"
    if not modules_dir.exists():
        return

    for py_file in sorted(modules_dir.glob("*.py")):
        if py_file.name.startswith("_"):
            continue

        module_name = py_file.stem
        route = _filename_to_route(py_file.name)

        try:
            mod = importlib.import_module(f"modules.{module_name}")
            handler = getattr(mod, "handler", None)
            if handler is None:
                continue

            # Create a closure for the handler
            def make_route_handler(h):
                async def route_handler(request: Request):
                    # Parse cookies from header
                    req_cookies = _parse_cookies(request)
                    cache_key = _get_cache_key(request, req_cookies)
                    cached = _get_cached(cache_key) if _cacheable_request(request) else None
                    if cached is not None:
                        resp = JSONResponse(
                            content=cached.get("body", {}),
                            status_code=cached.get("status", 200),
                        )
                        for cookie in cached.get("cookie", []):
                            resp.headers.append("set-cookie", _https_cookie(request, cookie))
                        return resp

                    # Parse query params
                    query_params = dict(request.query_params)

                    # Parse body
                    body = {}
                    content_type = request.headers.get("content-type", "")
                    if "application/json" in content_type:
                        try:
                            body = await request.json()
                        except Exception:
                            pass
                    elif "application/x-www-form-urlencoded" in content_type:
                        try:
                            form = await request.form()
                            body = dict(form)
                        except Exception:
                            pass
                    elif "multipart/form-data" in content_type:
                        try:
                            form = await request.form()
                            body = await _normalize_form(form)
                        except Exception:
                            pass

                    # Parse cookie string in query/body to object
                    for item in [query_params, body]:
                        if isinstance(item.get("cookie"), str):
                            item["cookie"] = cookie_to_json(unquote(item["cookie"]))

                    # Merge all into query
                    query = {"cookie": req_cookies, **query_params, **body}

                    # Inject client IP
                    client_ip = request.client.host if request.client else ""
                    if client_ip.startswith("::ffff:"):
                        client_ip = client_ip[7:]
                    if client_ip == "::1" or not client_ip:
                        client_ip = cfg.CN_IP

                    # Create request wrapper
                    async def request_wrapper(url, data, options):
                        options = options or {}
                        if not options.get("randomCNIP"):
                            options = {**options, "ip": client_ip}
                        return await ncm_request(url, data, options)

                    try:
                        module_response = await h(query, request_wrapper)

                        # Song URL unblock
                        if request.url.path == "/song/url/v1" and cfg.ENABLE_GENERAL_UNBLOCK == "true":
                            try:
                                from unblock import match_id
                                song = module_response["body"]["data"][0]
                                if song.get("freeTrialInfo") is not None or not song.get("url") or song.get("fee") in (1, 4):
                                    result = await match_id(query.get("id"))
                                    song["url"] = result["data"]["url"]
                                    song["freeTrialInfo"] = None
                                    if "kuwo" in song["url"] and cfg.ENABLE_PROXY == "true" and cfg.PROXY_URL:
                                        song["proxyUrl"] = cfg.PROXY_URL + song["url"]
                            except Exception:
                                pass

                        # Build response
                        resp = JSONResponse(
                            content=module_response.get("body", {}),
                            status_code=module_response.get("status", 200),
                        )

                        # Set cookies
                        cookies = module_response.get("cookie", [])
                        if not query.get("noCookie") and cookies:
                            for cookie in cookies:
                                resp.headers.append("set-cookie", _https_cookie(request, cookie))

                        # Handle redirect
                        if module_response.get("redirectUrl"):
                            return RedirectResponse(
                                url=module_response["redirectUrl"],
                                status_code=module_response.get("status", 302),
                            )

                        if resp.status_code == 200 and _cacheable_request(request):
                            _set_cache(cache_key, {
                                "status": resp.status_code,
                                "body": module_response.get("body", {}),
                                "cookie": cookies if not query.get("noCookie") else [],
                            })
                        return resp

                    except RequestError as e:
                        body = e.body or {"code": 404, "data": None, "msg": "Not Found"}
                        if isinstance(body, dict) and body.get("code") == "301":
                            body["msg"] = "需要登录"
                        resp = JSONResponse(content=body, status_code=e.status)
                        if not query.get("noCookie"):
                            for cookie in e.cookie:
                                resp.headers.append("set-cookie", _https_cookie(request, cookie))
                        return resp

                    except Exception as e:
                        return JSONResponse(
                            content={"code": 500, "msg": str(e)},
                            status_code=500,
                        )

                return route_handler

            app.add_api_route(
                route,
                make_route_handler(handler),
                methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            )

        except Exception as e:
            print(f"Failed to load module {module_name}: {e}")


# Load all modules first (routes take priority over static mount)
_load_modules()

# Mount static files (if public directory exists)
# Use /static prefix to avoid catching API routes
_public_dir = Path(__file__).parent / "public"
if _public_dir.exists():
    app.mount("/static", StaticFiles(directory=str(_public_dir)), name="static")

    # Serve index.html at root
    @app.get("/")
    async def serve_index():
        index_path = _public_dir / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {"message": "PyNCMAPI is running"}

    @app.get("/{static_path:path}", include_in_schema=False)
    async def serve_public_file(static_path: str):
        target = (_public_dir / static_path).resolve()
        public_root = _public_dir.resolve()
        if public_root == target or public_root not in target.parents:
            return JSONResponse(status_code=404, content={"code": 404, "msg": "Not Found"})
        if target.is_file():
            return FileResponse(str(target))
        index_path = target / "index.html"
        if index_path.is_file():
            return FileResponse(str(index_path))
        return JSONResponse(status_code=404, content={"code": 404, "msg": "Not Found"})
