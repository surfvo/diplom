import json

from aioredis import Redis, from_url

from settings import RedisConfig
from schemas.paring_place_schema import ParkingPlaceBase


async def init_redis_pool() -> Redis:
    redis = await from_url(
        RedisConfig.URL,
        encoding="utf-8",
        db=RedisConfig.DB,
        decode_responses=True,
        password=RedisConfig.PASSWORD
    )
    return redis


async def get_pp_creation_data(tg_id):
    redis = await init_redis_pool()

    data = await redis.get(tg_id)

    if data is None:
        await redis.set(tg_id, json.dumps(ParkingPlaceBase(owner_id=tg_id).json()))
        return ParkingPlaceBase().json()
    try:
        return ParkingPlaceBase(**json.loads(data))
    except TypeError:
        return ParkingPlaceBase(**json.loads(json.loads(data)))


async def set_users_state_to_none(tg_id):
    redis = await init_redis_pool()

    try:
        data = ParkingPlaceBase(**json.loads(await redis.get(tg_id)))
    except TypeError:
        data = ParkingPlaceBase(**json.loads(json.loads(await redis.get(tg_id))))

    data.state = None

    await redis.set(tg_id, json.dumps(data.json()))


async def set_users_state(tg_id: str, state: str):
    redis = await init_redis_pool()

    try:
        data = ParkingPlaceBase(**json.loads(await redis.get(tg_id)))
    except TypeError:
        data = ParkingPlaceBase(**json.loads(json.loads(await redis.get(tg_id))))

    data.state = state

    await redis.set(tg_id, json.dumps(data.json()))


async def update_pp_data(tg_id, data, data_type):
    redis = await init_redis_pool()

    pp = json.loads(json.loads(await redis.get(tg_id)))

    pp[data_type] = data

    await redis.set(tg_id, json.dumps(pp))


async def drop_pp_creation_form(tg_id):
    redis = await init_redis_pool()

    await redis.set(tg_id, json.dumps(ParkingPlaceBase(owner_id=tg_id).json()))


async def get_pp_data_to_edit(pp_id):
    redis = await init_redis_pool()

    data = await redis.get(pp_id)
    if not data:
        return data
    try:
        return ParkingPlaceBase(**json.loads(data))
    except TypeError:
        return ParkingPlaceBase(**json.loads(json.loads(data)))


async def insert_pp_edit_data(key, data):
    redis = await init_redis_pool()

    await redis.set(key, json.dumps(data.json()))