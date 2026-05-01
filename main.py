import argparse
import asyncio
import sys

import uvicorn


def main():
    parser = argparse.ArgumentParser(description="PyNCMAPI - NetEase Cloud Music API")
    parser.add_argument("--port", type=int, default=None, help="Port to listen on")
    parser.add_argument("--host", type=str, default=None, help="Host to bind to")
    args = parser.parse_args()

    import config as cfg

    port = args.port or cfg.PORT
    host = args.host or cfg.HOST

    # Run startup config
    async def startup():
        from generate_config import generate_config
        await generate_config()
        print(f"Chinese IP: {cfg.CN_IP}")
        print(f"Device ID: {cfg.DEVICE_ID[:16]}...")

    asyncio.run(startup())

    # Start server
    print("""
╔═╗╔═╗╦    ╔═╗╔╗╔╦ ╦╔═╗╔╗╔╔═╗╔═╗╔╦╗
╠═╣╠═╝║    ║╣ ║║║╠═╣╠═╣║║║║  ║╣  ║║
╩ ╩╩  ╩    ╚═╝╝╚╝╩ ╩╩ ╩╝╚╝╚═╝╚═╝═╩╝
""")
    print(f"Server started @ http://{'localhost' if not host else host}:{port}")

    uvicorn.run(
        "server:app",
        host=host or "0.0.0.0",
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
