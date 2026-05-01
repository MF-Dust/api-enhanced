from option import create_option


async def handler(query: dict, request) -> dict:
    return {
        "code": 200,
        "status": 200,
        "body": {
            "code": 200,
            "data": {
                "version": "4.32.0",
            },
        },
    }
