from aiogram import Bot, Dispatcher, types
from bot.keyboards import owners_park_keyboards
from services import user_service, owners_park_service
from settings import BotConfig
from aiogram.utils.exceptions import MessageNotModified
import json

bot = Bot(token=BotConfig.token)


async def my_parks(call: types.CallbackQuery):
    keyboard = await owners_park_keyboards.my_park_list_keyboard(call.from_user.id)
    user_last_message = await user_service.get_user_last_message(call.from_user.id)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Ваши парковки", reply_markup=keyboard)


async def edit_parking(call: types.CallbackQuery):

    pp_id = call.data.replace('owners_park_id_', '')

    links = list(set(await owners_park_service.get_img_links(pp_id)))
    try:
        links.remove(None)
    except ValueError:
        pass
    print(links)
    print(len(links))
    if links and len(links) > 1:
        media = types.MediaGroup()
        for link in links:
            media.attach_photo(types.InputFile(link))
        await bot.send_media_group(call.message.chat.id, media=media)
        keyboard = await owners_park_keyboards.my_park_edit_keyboard(call.from_user.id, pp_id)
        message = await bot.send_message(chat_id=call.from_user.id, text='Редактирование Места', reply_markup=keyboard)
        await user_service.update_user_last_message(call.from_user.id, message['message_id'])
    elif links and len(links) == 1:
        await bot.send_photo(chat_id=call.from_user.id, photo=open(links[0], 'rb'))
        keyboard = await owners_park_keyboards.my_park_edit_keyboard(call.from_user.id, pp_id)
        message = await bot.send_message(chat_id=call.from_user.id, text='Редактирование Места', reply_markup=keyboard)
        await user_service.update_user_last_message(call.from_user.id, message['message_id'])

    else:
        user_last_message = await user_service.get_user_last_message(call.from_user.id)
        keyboard = await owners_park_keyboards.my_park_edit_keyboard(call.from_user.id, pp_id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                    text='Редактирование Места', reply_markup=keyboard)


async def edit_park_back(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_park_back_', '')

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    keyboard = await owners_park_keyboards.my_park_edit_keyboard(call.from_user.id, pp_id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text='Редактирование Места', reply_markup=keyboard)


async def edit_address(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_address_', '')

    await user_service.set_user_state(call.from_user.id, f'edit_address_{pp_id}')

    keyboard = await owners_park_keyboards.parking_edit_keyboard_plug(pp_id)

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Введите новый адресс", reply_markup=keyboard)


async def edit_choose_address(call: types.CallbackQuery):
    address = call.data
    user_last_message = await user_service.get_user_last_message(call.from_user.id)

    addresses = json.loads(call.message.as_json())['reply_markup']['inline_keyboard']

    for ad in addresses:
        if address in ad[0].values():
            await owners_park_service.update_pp_data(address[21:].split('_')[2], ad[0]['text'], 'address')
            await owners_park_service.update_pp_data(address[21:].split('_')[2], float(address[21:].split('_')[0]), 'x')
            await owners_park_service.update_pp_data(address[21:].split('_')[2], float(address[21:].split('_')[1]), 'y')

    keyboard = await owners_park_keyboards.my_park_edit_keyboard(call.from_user.id, address[16:].split('_')[3])
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                text="Создание парковочного места", reply_markup=keyboard)


async def edit_number_creation(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_parking_number_', '')

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await user_service.set_user_state(call.from_user.id, call.data)

    keyboard = await owners_park_keyboards.parking_edit_keyboard_plug(pp_id)

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                text="Укажите новый номер парковочного места", reply_markup=keyboard)


async def edit_price(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_price_', '')
    keyboard = await owners_park_keyboards.edit_parking_price_keyboard(pp_id)

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Выберите за какой период хотите изменить стоимость", reply_markup=keyboard)


async def edit_price_day(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_day_price_', '')

    await user_service.set_user_state(call.from_user.id, f'edit_day_price_{pp_id}')
    user_last_message = await user_service.get_user_last_message(call.from_user.id)

    keyboard = await owners_park_keyboards.parking_edit_price_keyboard_plug(pp_id)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Ввидите новую цену за день", reply_markup=keyboard)


async def edit_price_week(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_week_price_', '')

    await user_service.set_user_state(call.from_user.id, f'edit_week_price_{pp_id}')
    user_last_message = await user_service.get_user_last_message(call.from_user.id)

    keyboard = await owners_park_keyboards.parking_edit_price_keyboard_plug(pp_id)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Ввидите новую цену за неделю", reply_markup=keyboard)


async def edit_price_month(call: types.CallbackQuery):

    pp_id = call.data.replace('edit_month_price_', '')

    await user_service.set_user_state(call.from_user.id, f'edit_month_price_{pp_id}')
    user_last_message = await user_service.get_user_last_message(call.from_user.id)

    keyboard = await owners_park_keyboards.parking_edit_price_keyboard_plug(pp_id)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Ввидите цену цену за месяц", reply_markup=keyboard)


async def edit_date_start(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_date_start_', '')

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await user_service.set_user_state(call.from_user.id, f'edit_date_start_{pp_id}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Выберите дату с которой будете сдавать",
                                reply_markup=await DialogCalendar().start_calendar())


async def edit_date_end(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_date_end_', '')

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await user_service.set_user_state(call.from_user.id, f'edit_date_end_{pp_id}')

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Выберите дату по какую будете сдавать",
                                reply_markup=await DialogCalendar().start_calendar())


async def edit_phone(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_phone_', '')
    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await user_service.set_user_state(call.from_user.id, f'edit_phone_{pp_id}')

    keyboard = await owners_park_keyboards.parking_edit_keyboard_plug(pp_id)

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                text="Введите новый номер в формате 78005553535 или 88005553535", reply_markup=keyboard)


async def edit_comment(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_comment_', '')
    place_data = owners_park_service.get_pp_data_to_edit(pp_id)

    if place_data.comment:
        user_last_message = await user_service.get_user_last_message(call.from_user.id)
        await user_service.set_user_state(call.from_user.id, f'edit_comment_{pp_id}')

        keyboard = await owners_park_keyboards.parking_edit_keyboard_plug(pp_id)

        await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                    text=f"Ваш комментарий: {place_data.comment}", reply_markup=keyboard)
    else:
        user_last_message = await user_service.get_user_last_message(call.from_user.id)
        await user_service.set_user_state(call.from_user.id, f'edit_comment_{pp_id}')

        keyboard = await owners_park_keyboards.parking_edit_keyboard_plug(pp_id)

        await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                    text="Комментарий", reply_markup=keyboard)


async def edit_parking_img(call: types.CallbackQuery):
    pp_id = call.data.replace('edit_img_', '')
    keyboard = await owners_park_keyboards.edit_images_keyboard(pp_id)

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Добавление фото парковки", reply_markup=keyboard)


async def edit_img_link(call: types.CallbackQuery):
    pp_id = call.data.split('_')[-1]
    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await user_service.set_user_state(call.from_user.id, call.data)

    keyboard = await owners_park_keyboards.edit_parking_photo_plug_keyboard(pp_id)

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=user_last_message,
                                text="Отправьте новое фото", reply_markup=keyboard)


async def edit_decline_pp(call: types.CallbackQuery):
    pp_id = call.data.split('_')[-1]

    owners_park_service.drop_pp_edit(pp_id)

    try:
        keyboard = await owners_park_keyboards.my_park_edit_keyboard(call.from_user.id, pp_id)

        user_last_message = await user_service.get_user_last_message(call.from_user.id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                    text="Редактирование парковочного места", reply_markup=keyboard)
    except MessageNotModified:
        pass


async def edit_accept_pp(call: types.CallbackQuery):
    pp_id = call.data.split('_')[-1]
    # data = owners_park_service.get_pp_data(pp_id)
    updated_data = owners_park_service.get_pp_data_to_edit(pp_id)
    if updated_data.address is None and updated_data.parking_number:
        await call.answer(text="Не указан аддрес или номер паркинга", show_alert=True)
    else:
        owners_park_service.accept_pp_edit(pp_id)
        keyboard = await owners_park_keyboards.my_park_list_keyboard(call.from_user.id)

        user_last_message = await user_service.get_user_last_message(call.from_user.id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                    text="Ваши парковки", reply_markup=keyboard)
        await call.answer(text="Даннуе успешно сохранены", show_alert=True)


def register_owners_park(dp: Dispatcher):
    dp.register_callback_query_handler(my_parks, text="my_park")
    dp.register_callback_query_handler(edit_park_back, text_startswith='edit_park_back_')
    dp.register_callback_query_handler(edit_parking, text_startswith='owners_park_id_')

    dp.register_callback_query_handler(edit_address, text_startswith='edit_address_')
    dp.register_callback_query_handler(edit_choose_address, text_startswith='edit_location_chosen_')

    dp.register_callback_query_handler(edit_number_creation, text_startswith='edit_parking_number_')

    dp.register_callback_query_handler(edit_price, text_startswith='edit_price_')

    dp.register_callback_query_handler(edit_price_day, text_startswith='edit_day_price_')
    dp.register_callback_query_handler(edit_price_week, text_startswith='edit_week_price_')
    dp.register_callback_query_handler(edit_price_month, text_startswith='edit_month_price_')
    dp.register_callback_query_handler(edit_date_start, text_startswith='edit_date_start_')
    dp.register_callback_query_handler(edit_date_end, text_startswith='edit_date_end_')

    dp.register_callback_query_handler(edit_phone, text_startswith='edit_phone_')
    dp.register_callback_query_handler(edit_comment, text_startswith='edit_comment_')

    dp.register_callback_query_handler(edit_parking_img, text_startswith='edit_img_')
    dp.register_callback_query_handler(edit_img_link, text_startswith='edit_link_img_')

    dp.register_callback_query_handler(edit_decline_pp, text_startswith='edit_decline_pp_creation_')
    dp.register_callback_query_handler(edit_accept_pp, text_startswith='edit_accept_pp_creation_')
