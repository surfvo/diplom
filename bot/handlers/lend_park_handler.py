from aiogram import Bot, Dispatcher, types
from bot.keyboards import start_keyboards, owners_park_keyboards, lend_park_keyboard
from services import user_service #, owners_park_service
from services import lend_park_service
from datetime import datetime
from aiogram.utils.exceptions import MessageNotModified
import json
from settings import BotConfig
# from main import bot
bot = Bot(token=BotConfig.token)


async def start_parking_creation(call: types.CallbackQuery):
    keyboard = await lend_park_keyboard.create_lend_park_keyboard(call.from_user.id)

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Создание парковочного места", reply_markup=keyboard)


async def address_creation(call: types.CallbackQuery):
    await user_service.set_user_state(call.from_user.id, 'address_creation')

    keyboard = await lend_park_keyboard.parking_creation_address_keyboard()

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Введите адресс парковки", reply_markup=keyboard)


async def price_creation(call: types.CallbackQuery):
    # user_service.set_user_state(call.from_user.id, 'address_creation')

    keyboard = await lend_park_keyboard.parking_creation_price_keyboard(call.from_user.id)

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Выберите возможные варианты съема и укажите цену", reply_markup=keyboard)


async def price_day_creation(call: types.CallbackQuery):
    await user_service.set_user_state(call.from_user.id, 'price_day_creation')
    user_last_message = await user_service.get_user_last_message(call.from_user.id)

    keyboard = types.InlineKeyboardMarkup(row_width=2).add(types.InlineKeyboardButton(text='Назад',
                                                                                      callback_data='price'))

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Ввидите цену за день", reply_markup=keyboard)


async def price_week_creation(call: types.CallbackQuery):
    await user_service.set_user_state(call.from_user.id, 'price_week_creation')
    user_last_message = await user_service.get_user_last_message(call.from_user.id)

    keyboard = types.InlineKeyboardMarkup(row_width=2).add(types.InlineKeyboardButton(text='Назад',
                                                                                      callback_data='price'))

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Ввидите цену за неделю", reply_markup=keyboard)


async def price_month_creation(call: types.CallbackQuery):
    await user_service.set_user_state(call.from_user.id, 'price_month_creation')
    user_last_message = await user_service.get_user_last_message(call.from_user.id)

    keyboard = types.InlineKeyboardMarkup(row_width=2).add(types.InlineKeyboardButton(text='Назад',
                                                                                      callback_data='price'))

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Ввидите цену за месяц", reply_markup=keyboard)


async def date_start_creating(call: types.CallbackQuery):
    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await user_service.set_user_state(call.from_user.id, 'date_start_creating')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Напишите с какой даты вы хотите сдавать парковочное место в формате: 2022-02-24",
                                reply_markup=await lend_park_keyboard.parking_creation_plug_keyboard())


async def date_end_creating(call: types.CallbackQuery):
    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await user_service.set_user_state(call.from_user.id, 'date_end_creating')

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Напишите по какую дату вы хотите сдавать парковочное место в формате: 2022-02-24",
                                reply_markup=await lend_park_keyboard.parking_creation_plug_keyboard())


async def phone_creation(call: types.CallbackQuery):
    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await user_service.set_user_state(call.from_user.id, 'phone_creation')

    keyboard = await lend_park_keyboard.phone_creation_keyboard()

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                text="Введите номер в формате 78005553535 или 88005553535", reply_markup=keyboard)


async def comment_creation(call: types.CallbackQuery):
    place_data = await lend_park_service.get_pp_creation_data(call.from_user.id)

    if place_data.comment:
        user_last_message = await user_service.get_user_last_message(call.from_user.id)
        await user_service.set_user_state(call.from_user.id, 'comment')

        keyboard = await lend_park_keyboard.parking_creation_plug_keyboard()

        await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                    text=f"Ваш комментарий: {place_data.comment}", reply_markup=keyboard)
    else:
        user_last_message = await user_service.get_user_last_message(call.from_user.id)
        await user_service.set_user_state(call.from_user.id, 'comment')

        keyboard = await lend_park_keyboard.parking_creation_plug_keyboard()

        await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                    text="Комментарий", reply_markup=keyboard)


async def parking_img_creation(call: types.CallbackQuery):
    keyboard = await lend_park_keyboard.images_creation(call.from_user.id)

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Добавление фото парковки", reply_markup=keyboard)


async def img_link_creation(call: types.CallbackQuery):
    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await user_service.set_user_state(call.from_user.id, call.data)

    keyboard = await lend_park_keyboard.parking_creation_photo_plug_keyboard()

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                text="Отправьте фото", reply_markup=keyboard)


async def decline_pp_creation(call: types.CallbackQuery):
    await lend_park_service.drop_pp_creation_form(call.from_user.id)
    try:
        keyboard = await lend_park_keyboard.create_lend_park_keyboard(call.from_user.id)

        user_last_message = await user_service.get_user_last_message(call.from_user.id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                    text="Создание парковочного места", reply_markup=keyboard)
    except MessageNotModified:
        pass


async def accept_pp_creation(call: types.CallbackQuery):
    data = await lend_park_service.get_pp_creation_data(call.from_user.id)
    if data.address is None or data.parking_number is None:
        await call.answer(text="Не указан аддрес или номер паркинга", show_alert=True)
    else:
        await lend_park_service.accept_pp_creation_form(call.from_user.id)
        keyboard = await start_keyboards.create_main_menu_keyboard()

        user_last_message = await user_service.get_user_last_message(call.from_user.id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                    text="Главное меню", reply_markup=keyboard)


async def parking_number_creation(call: types.CallbackQuery):
    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await user_service.set_user_state(call.from_user.id, call.data)

    keyboard = await lend_park_keyboard.parking_creation_plug_keyboard()

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                text="Укажите номер парковочного места", reply_markup=keyboard)


def register_lend_park(dp: Dispatcher):
    dp.register_callback_query_handler(start_parking_creation, text='lend_a_park')
    dp.register_callback_query_handler(address_creation, text='address')
    dp.register_callback_query_handler(parking_number_creation, text='parking_number')

    dp.register_callback_query_handler(price_creation, text='price')
    dp.register_callback_query_handler(price_day_creation, text='day_price')
    dp.register_callback_query_handler(price_week_creation, text='week_price')
    dp.register_callback_query_handler(price_month_creation, text='month_price')

    dp.register_callback_query_handler(date_start_creating, text='date_start')
    dp.register_callback_query_handler(date_end_creating, text='date_end')
    dp.register_callback_query_handler(phone_creation, text='phone')
    dp.register_callback_query_handler(comment_creation, text='comment')
    dp.register_callback_query_handler(parking_img_creation, text='img')
    dp.register_callback_query_handler(img_link_creation, text_startswith='img_link_')
    dp.register_callback_query_handler(decline_pp_creation, text='decline_pp_creation')
    dp.register_callback_query_handler(accept_pp_creation, text='accept_pp_creation')
