from aiogram import types
from services.lend_park_service import get_pp_creation_data
from services.user_service import state_to_none


async def create_lend_park_keyboard(tg_id):
    place_data = await get_pp_creation_data(tg_id)
    await state_to_none(tg_id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text="Адрес", callback_data="address"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.address is None
            else place_data.address, callback_data="address"),
        types.InlineKeyboardButton(text="Номер паркинга", callback_data="parking_number"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.parking_number is None
            else place_data.parking_number, callback_data="parking_number"),

        types.InlineKeyboardButton(text="Цена", callback_data="price"),
        types.InlineKeyboardButton(
            "️🌕" if (place_data.price_day is None and place_data.price_week is None and place_data.price_month is None)
            else 'Ценна указана', callback_data="price"),

        types.InlineKeyboardButton(text="Дата старта", callback_data="date_start"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.date_start is None
            else place_data.date_start, callback_data="date_start"),

        types.InlineKeyboardButton(text="Дата оканчания", callback_data="date_end"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.date_end is None
            else place_data.date_end, callback_data="date_end"),

        types.InlineKeyboardButton(text="Фото парковки", callback_data="img"),
        types.InlineKeyboardButton("️🌕" if (place_data.img_link_1 is None and place_data.img_link_2 is None
                                            and place_data.img_link_3 is None)
                                   else 'Фото приложено', callback_data="img"),
        types.InlineKeyboardButton(text="Телефон", callback_data="phone"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.phone is None
            else place_data.phone, callback_data="phone"),
        types.InlineKeyboardButton(text="Комментарий", callback_data="comment"),
        types.InlineKeyboardButton(
            "️🌕" if place_data.comment is None
            else 'Комментарий указан', callback_data="comment"),

        types.InlineKeyboardButton(text='Отменить', callback_data="decline_pp_creation"),
        types.InlineKeyboardButton(text='Сохранить', callback_data="accept_pp_creation"),
        types.InlineKeyboardButton(text='Назад', callback_data="main_menu")
    ]

    keyboard.add(*buttons)
    return keyboard


async def parking_creation_address_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data="lend_a_park"))
    return keyboard


async def parking_creation_price_keyboard(tg_id):
    place_data = await get_pp_creation_data(tg_id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text="Цена за день", callback_data="day_price"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.price_day is None
                   else place_data.price_day, callback_data="day_price"),

               types.InlineKeyboardButton(text="Цена за неделю", callback_data="week_price"),
               types.InlineKeyboardButton(
                   "🌕" if place_data.price_week is None
                   else place_data.price_week, callback_data="week_price"),

               types.InlineKeyboardButton(text="Цена за месяц", callback_data="month_price"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.price_month is None
                   else place_data.price_month, callback_data="month_price"), ]
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data="lend_a_park"))
    return keyboard


async def create_address_keyboard(locations):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for location in locations:
        keyboard.add(
            types.InlineKeyboardButton(text="{}, {}, {}".format(location.area, location.street, location.house),
                                       callback_data="location_chosen_{}_{}".format(location.x, location.y)))
    return keyboard


async def phone_creation_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data="lend_a_park"))
    return keyboard


async def parking_creation_plug_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data="lend_a_park"))
    return keyboard


async def images_creation(tg_id):
    place_data = await get_pp_creation_data(tg_id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text="Фото №1", callback_data="img_link_1"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.img_link_1 is None
                   else 'Фото приложено', callback_data="img_link_1"),

               types.InlineKeyboardButton(text="Фото №2", callback_data="img_link_2"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.img_link_2 is None
                   else 'Фото приложено', callback_data="img_link_2"),

               types.InlineKeyboardButton(text="Фото №3", callback_data="img_link_3"),
               types.InlineKeyboardButton(
                   "️🌕" if place_data.img_link_3 is None
                   else 'Фото приложено', callback_data="img_link_3"), ]
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data="lend_a_park"))
    return keyboard


async def parking_creation_photo_plug_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data="img"))
    return keyboard
