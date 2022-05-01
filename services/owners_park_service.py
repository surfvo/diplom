import os
from services.managers import redis_manager, pg_manager


async def get_img_links(pp_id):
    return await pg_manager.get_img_links(pp_id)


async def get_pp_data_to_edit(pp_id):
    data = await redis_manager.get_pp_data_to_edit('pp_id'+pp_id)
    if data is None:
        data = await pg_manager.get_pp_data_by_pp_id(pp_id)
        await redis_manager.insert_pp_edit_data('pp_id'+pp_id, data)
        return await redis_manager.get_pp_data_to_edit('pp_id' + pp_id)

    return data


async def update_pp_data(pp_id, data, state):
    await redis_manager.update_pp_data('pp_id'+pp_id, data, state)


def get_pp_data(pp_id):
    db: Session = get_db()

    data = db.query(ParkingPlace).filter(ParkingPlace.id == pp_id).first

    db.close()
    return data


def drop_pp_edit(pp_id):
    db: Session = get_db()

    db.query(ParkingPlace).filter_by(edit=pp_id).delete()

    db.commit()
    db.close()


def accept_pp_edit(pp_id):
    db: Session = get_db()

    images = get_img_links(pp_id)

    updated_img_links = db.query(ParkingPlace.img_link_1, ParkingPlace.img_link_2, ParkingPlace.img_link_3) \
        .filter(ParkingPlace.edit == pp_id).first()

    if updated_img_links != images:
        for i in range(2):
            if images[i] != updated_img_links[i]:
                os.remove(images[i])

    db.query(ParkingPlace).filter(ParkingPlace.edit == pp_id).update({'published': True, 'edit': None},
                                                                     synchronize_session='fetch')

    db.query(ParkingPlace).filter_by(id=pp_id).delete()

    db.commit()
    db.close()
