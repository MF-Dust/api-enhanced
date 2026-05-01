from option import create_option
from utils import is_one

resource_type_map = {
    "0": "R_SO_4_",
    "1": "R_MV_5_",
    "2": "A_PL_0_",
    "3": "R_AL_3_",
    "4": "A_DJ_1_",
    "5": "R_VI_62_",
    "6": "A_EV_2_",
    "7": "A_DR_14_",
}


async def handler(query: dict, request) -> dict:
    t = "like" if is_one(query.get("t")) else "unlike"
    res_type = resource_type_map.get(str(query.get("type", "")), "")
    thread_id = res_type + str(query.get("id", ""))
    if res_type == "A_EV_2_":
        thread_id = query.get("threadId", thread_id)
    data = {
        "threadId": thread_id,
    }
    return await request(
        f"/api/resource/{t}", data, create_option(query, "weapi")
    )
