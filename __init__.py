import importlib
import sys
from pathlib import Path
from typing import Any, Awaitable, Callable

PACKAGE_DIR = Path(__file__).resolve().parent
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

MODULE_DIR = PACKAGE_DIR / "modules"
_module_names = sorted(
    p.stem for p in MODULE_DIR.glob("*.py")
    if p.stem != "__init__" and not p.stem.startswith("_")
)


def construct_server():
    from server import app
    return app


def serve(host: str = "0.0.0.0", port: int = 3000, **kwargs):
    import uvicorn
    return uvicorn.run("server:app", host=host, port=port, **kwargs)


def _make_module_callable(name: str) -> Callable[[dict | None, Any], Awaitable[dict]]:
    async def call(query: dict | None = None, request=None) -> dict:
        from request import ncm_request

        mod = importlib.import_module(f"modules.{name}")
        handler = getattr(mod, "handler")
        return await handler(query or {}, request or ncm_request)

    call.__name__ = name
    return call


def __getattr__(name: str):
    if name in _module_names:
        func = _make_module_callable(name)
        globals()[name] = func
        return func
    raise AttributeError(name)


__all__ = ["construct_server", "serve", *_module_names]
