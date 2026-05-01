from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "cellphone": query.get("phone"),
        "countrycode": query.get("countrycode"),
    }
    return await request(
        "/api/cellphone/existence/check", data, create_option(query)
    )
