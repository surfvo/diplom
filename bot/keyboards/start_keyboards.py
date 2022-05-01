from aiogram import types


async def create_main_menu_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    buttons = [
        types.InlineKeyboardButton(text='Снять парковку 🅿️', callback_data='rent_a_park'),
        types.InlineKeyboardButton(text='Сдать парковку 💸', callback_data='lend_a_park'),
        types.InlineKeyboardButton(text='Мои парковки 🏡', callback_data='my_park'),

    ]

    keyboard.add(*buttons)

    return keyboard
