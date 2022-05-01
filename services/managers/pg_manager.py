import asyncpg
from datetime import datetime

from settings import PostgreSqlConfig
from datetime import datetime
from schemas.paring_place_schema import ParkingPlaceBase


async def connect():
    conn = await asyncpg.connect(PostgreSqlConfig.DATABASE_URL)
    return conn


async def create_user(user_id: int, name: str, last_m_id: int):
    cur = await connect()

    await cur.execute("insert into users (tg_id, name, last_message) values($1, $2, $3) "
                      "on conflict (tg_id) do update set last_message = $3",
                      user_id, name, last_m_id)

    await cur.close()


async def get_user(tg_id: int):
    cur = await connect()

    user = await cur.fetch("select * from users where tg_id = $1", tg_id)

    await cur.close()

    return user[0]


async def insert_new_pp(data):
    cur = await connect()
    try:
        date_end = datetime.strptime(data.date_end, '%Y-%m-%d')
    except TypeError:
        date_end = None
    try:
        date_start = datetime.strptime(data.date_start, '%Y-%m-%d')
    except TypeError:
        date_start = None
    print(data.owner_id)
    await cur.execute("insert into parking_place (address, parking_number, img_link_1,"
                      " img_link_2, img_link_3, verify_img, price_day, price_week, price_month, date_start, "
                      "date_end, phone, comment, owner_id) values ($1, $2, $3, $4, $5, $6,"
                      "$7, $8, $9, $10, $11, $12, $13, $14)", data.address, data.parking_number, data.img_link_1,
                      data.img_link_2, data.img_link_3, data.verify_img, data.price_day, data.price_week,
                      data.price_month, date_start,
                      date_end, data.phone, data.comment, data.owner_id)
    await cur.close()



async def get_users_parks(tg_id):
    cur = await connect()

    parks = await cur.fetch("select * from parking_place "
                            "join users on users.tg_id = parking_place.owner_id "
                            "where owner_id = $1", tg_id)
    await cur.close()
    data = []
    for park in parks:
        data.append(ParkingPlaceBase(**park))
    return data


async def get_img_links(pp_id):
    curr = await connect()

    links = await curr.fetch("select img_link_1, img_link_2, img_link_3 from parking_place where id = $1", int(pp_id))
    links = links[0]

    # return ParkingPlaceBase(img_link_1=links['img_link_1'], img_link_2=links['img_link_2'],img_link_3=links['img_link_3'])
    return links


async def get_pp_data_by_pp_id(pp_id):
    cur = await connect()

    data = await cur.fetch('select * from parking_place where id = $1', int(pp_id))

    return ParkingPlaceBase(**data[0])


async def get_pps(user_id):
    cur = await connect()
    pps = await cur.fetch("select id, verified, address, parking_number, img_link_1, img_link_2, img_link_3, "
                          "verify_img, price_day, price_week,price_month,date_start,phone, comment, owner_id, "
                          "date_end, users.name from parking_place "
                          "join users on owner_id = tg_id "
                          "where owner_id != $1", user_id)
    data = []
    for park in pps:
        data.append(ParkingPlaceBase(**park))
    print(data)
    await cur.close()
    return data


async def update_user_last_message(user_id, last_m):
    cur = await connect()
    await cur.execute("update users set last_message = $1 where tg_id = $2", last_m + 1, user_id)
    await cur.close()


async def get_last_bot_message():
    cur = await connect()

    lm = await cur.fetch("select max(last_message) from users")

    return lm['max']

