from services.managers import redis_manager, pg_manager
import json


async def get_pp_creation_data(tg_id: int):
    return await redis_manager.get_pp_creation_data(tg_id)


async def add_parking_data(tg_id, data, data_type):
    await redis_manager.update_pp_data(tg_id, data, data_type)


async def drop_pp_creation_form(tg_id):
    await redis_manager.drop_pp_creation_form(tg_id)


async def accept_pp_creation_form(tg_id):
    data = await get_pp_creation_data(tg_id)

    await pg_manager.insert_new_pp(data)

    await redis_manager.drop_pp_creation_form(tg_id)

