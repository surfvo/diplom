from services.managers import pg_manager, redis_manager


async def create_user(user_id: int, name: str, last_m_id: int):
    await pg_manager.create_user(user_id, name, last_m_id)


async def get_user_last_message(tg_id: int):
    user = await pg_manager.get_user(tg_id)
    print(user)
    return user['last_message']


async def state_to_none(tg_id):
    await redis_manager.set_users_state_to_none(tg_id)


async def set_user_state(tg_id: str, state: str):
    await redis_manager.set_users_state(tg_id, state)


async def get_user_state(tg_id):
    return (await redis_manager.get_pp_creation_data(tg_id)).state


async def get_users_parks_data(tg_id):
    return await pg_manager.get_users_parks(tg_id)


async def update_user_last_message(user_tg_id, last_message):
    await pg_manager.update_user_last_message(user_tg_id, last_message)


async def get_last_bot_message():
    return await pg_manager.get_last_bot_message()
