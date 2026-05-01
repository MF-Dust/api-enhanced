from option import create_option


async def handler(query: dict, request) -> dict:
    data = {
        "refer": "inbox_invite",
        "roomId": query.get("roomId"),
        "inviterId": query.get("inviterId"),
    }
    return await request(
        "/api/listen/together/play/invitation/accept",
        data,
        create_option(query),
    )
