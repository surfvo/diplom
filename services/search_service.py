from services.managers import redis_manager, pg_manager


async def get_pps(user_id):
    pps = await pg_manager.get_pps(user_id)
    return pps
