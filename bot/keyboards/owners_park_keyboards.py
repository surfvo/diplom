from aiogram import types
from services.user_service import state_to_none, get_users_parks_data
from services.owners_park_service import get_pp_data_to_edit


async def my_park_list_keyboard(tg_id):
    owners_parks = await get_users_parks_data(tg_id)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []

    for park in owners_parks:
        buttons.append(types.InlineKeyboardButton(text=f"{park.address}, {park.parking_number}",
                                                  callback_data=f"owners_park_id_{park.id}"))
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='main_menu'))
    return keyboard


async def my_park_edit_keyboard(tg_id, pp_id):
    await state_to_none(tg_id)
    place_data = await get_pp_data_to_edit(pp_id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text="Адрес", callback_data=f"edit_address_{pp_id}"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.address is None
            else place_data.address, callback_data=f"edit_address_{pp_id}"),
        types.InlineKeyboardButton(text="Номер паркинга", callback_data=f"edit_parking_number_{pp_id}"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.parking_number is None
            else place_data.parking_number, callback_data=f"edit_parking_number_{pp_id}"),

        types.InlineKeyboardButton(text="Цена", callback_data=f"edit_price_{pp_id}"),
        types.InlineKeyboardButton(
            "️🌕" if (
                    place_data.price_day is None and place_data.price_week is None
                    and place_data.price_month is None)
            else 'Ценна указана', callback_data=f"edit_price_{pp_id}"),

        types.InlineKeyboardButton(text="Дата старта", callback_data=f"edit_date_start_{pp_id}"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.date_start is None
            else place_data.date_start.strftime('%Y-%m-%d'), callback_data=f"edit_date_start_{pp_id}"),

        types.InlineKeyboardButton(text="Дата оканчания", callback_data=f"edit_date_end_{pp_id}"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.date_end is None
            else place_data.date_end.strftime('%Y-%m-%d'), callback_data=f"edit_date_end_{pp_id}"),

        types.InlineKeyboardButton(text="Фото парковки", callback_data=f"edit_img_{pp_id}"),
        types.InlineKeyboardButton("️🌕" if (place_data.img_link_1 is None and place_data.img_link_2 is None
                                            and place_data.img_link_3 is None)
                                   else 'Фото приложено', callback_data=f"edit_img_{pp_id}"),
        types.InlineKeyboardButton(text="Телефон", callback_data=f"edit_phone_{pp_id}"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.phone is None
            else place_data.phone, callback_data=f"edit_phone_{pp_id}"),
        types.InlineKeyboardButton(text="Комментарий", callback_data=f"edit_comment_{pp_id}"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.comment is None
            else 'Комментарий указан', callback_data=f"edit_comment_{pp_id}"),

        types.InlineKeyboardButton(text='Отменить', callback_data=f"edit_decline_pp_creation_{pp_id}"),
        types.InlineKeyboardButton(text='Сохранить', callback_data=f"edit_accept_pp_creation_{pp_id}"),
        types.InlineKeyboardButton(text='Назад', callback_data="my_park")
    ]

    keyboard.add(*buttons)
    return keyboard


async def parking_edit_keyboard_plug(pp_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"edit_park_back_{pp_id}"))
    return keyboard


async def edit_address_keyboard(locations, pp_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for location in locations:
        keyboard.add(types.InlineKeyboardButton(text="{}, {}, {}".format(location.area, location.street,
                                                                         location.house),
                                                callback_data="edit_location_chosen_{}_{}_{}".format(location.x,
                                                                                                     location.y,
                                                                                                     pp_id)))
    return keyboard


async def edit_parking_price_keyboard(pp_id):
    place_data = await get_pp_data_to_edit(pp_id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text="Цена за день", callback_data=f"edit_day_price_{pp_id}"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.price_day is None
                   else place_data.price_day, callback_data=f"edit_day_price_{pp_id}"),

               types.InlineKeyboardButton(text="Цена за неделю", callback_data=f"edit_week_price_{pp_id}"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.price_week is None
                   else place_data.price_week, callback_data=f"edit_week_price_{pp_id}"),

               types.InlineKeyboardButton(text="Цена за месяц", callback_data=f"edit_month_price_{pp_id}"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.price_month is None
                   else place_data.price_month, callback_data=f"edit_month_price_{pp_id}"), ]
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"edit_park_back_{pp_id}"))
    return keyboard


async def parking_edit_price_keyboard_plug(pp_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"edit_price_{pp_id}"))
    return keyboard


async def edit_images_keyboard(pp_id):
    place_data = await get_pp_data_to_edit(pp_id)

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text="Фото №1", callback_data=f"edit_link_img_1{pp_id}"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.img_link_1 is None
                   else 'Фото приложено', callback_data=f"edit_link_img_1_{pp_id}"),

               types.InlineKeyboardButton(text="Фото №2", callback_data=f"edit_link_img_2_{pp_id}"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.img_link_2 is None
                   else 'Фото приложено', callback_data=f"edit_link_img_2_{pp_id}"),

               types.InlineKeyboardButton(text="Фото №3", callback_data=f"edit_link_img_3_{pp_id}"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.img_link_3 is None
                   else 'Фото приложено', callback_data=f"edit_link_img_3_{pp_id}"), ]
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"edit_park_back_{pp_id}"))
    return keyboard


async def edit_parking_photo_plug_keyboard(pp_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"edit_img_{pp_id}"))
    return keyboard
