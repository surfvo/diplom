import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import MessageNotModified

from bot.keyboards import lend_park_keyboard, owners_park_keyboards
from services import user_service, lend_park_service, owners_park_service
from settings import BotConfig
from datetime import datetime

bot = Bot(token=BotConfig.token)


async def process_message(message: types.Message):
    state = await user_service.get_user_state(message.chat.id)
    last_message = await user_service.get_user_last_message(message.chat.id)
    await user_service.state_to_none(message.chat.id)

    if state == 'address_creation':
        address = message.text

        await lend_park_service.add_parking_data(message.chat.id, address, 'address')

        keyboard = await lend_park_keyboard.create_lend_park_keyboard(message.chat.id)

        await bot.edit_message_text(text="Создание парковочного места", chat_id=message.chat.id,
                                    message_id=last_message, reply_markup=keyboard)
    elif state == 'date_start_creating':
        date = message.text

        try:
            datetime.strptime(date, '%Y-%m-%d')

            await lend_park_service.add_parking_data(message.chat.id, date, 'date_start')

            keyboard = await lend_park_keyboard.create_lend_park_keyboard(message.chat.id)

            await bot.edit_message_text(text="Создание парковочного места", chat_id=message.chat.id,
                                        message_id=last_message, reply_markup=keyboard)
        except ValueError:
            await user_service.set_user_state(message.from_user.id, 'date_start_creating')
            await bot.edit_message_text(chat_id=message.chat.id, message_id=last_message,
                                        text="Вы написали не в правильном формате. "
                                        "Напишите с какой даты вы хотите сдавать парковочное"
                                             " место в формате: 2022-02-24",
                                        reply_markup=await lend_park_keyboard.parking_creation_plug_keyboard())
    elif state == 'date_end_creating':
        date = message.text
        try:
            datetime.strptime(date, '%Y-%m-%d')

            await lend_park_service.add_parking_data(message.chat.id, date, 'date_end')

            keyboard = await lend_park_keyboard.create_lend_park_keyboard(message.chat.id)

            await bot.edit_message_text(text="Создание парковочного места", chat_id=message.chat.id,
                                        message_id=last_message, reply_markup=keyboard)
        except ValueError:
            await user_service.set_user_state(message.from_user.id, 'date_end_creating')
            await bot.edit_message_text(chat_id=message.chat.id, message_id=last_message,
                                        text="Вы написали не в правильном формате. "
                                        "Напишите по какую дату вы хотите сдавать парковочное"
                                             " место в формате: 2022-02-24",
                                        reply_markup=await lend_park_keyboard.parking_creation_plug_keyboard())

    elif state == 'price_day_creation':
        data = message.text

        try:
            data = int(data)
            await lend_park_service.add_parking_data(message.chat.id, data, 'price_day')

            keyboard = await lend_park_keyboard.parking_creation_price_keyboard(message.chat.id)

            await bot.edit_message_text(text="Выберите возможные варианты съема и укажите цену",
                                        chat_id=message.chat.id,
                                        message_id=last_message, reply_markup=keyboard)
        except ValueError:
            await user_service.set_user_state(message.chat.id, 'price_day_creation')
            pass

    elif state == 'price_week_creation':
        data = message.text
        try:
            data = int(data)
            await lend_park_service.add_parking_data(message.chat.id, data, 'price_week')

            keyboard = await lend_park_keyboard.parking_creation_price_keyboard(message.chat.id)

            await bot.edit_message_text(text="Выберите возможные варианты съема и укажите цену",
                                        chat_id=message.chat.id,
                                        message_id=last_message, reply_markup=keyboard)
        except ValueError:
            await user_service.set_user_state(message.chat.id, 'price_week_creation')
            pass
    elif state == 'price_month_creation':
        data = message.text
        try:
            data = int(data)
            await lend_park_service.add_parking_data(message.chat.id, data, 'price_month')

            keyboard = await lend_park_keyboard.parking_creation_price_keyboard(message.chat.id)

            await bot.edit_message_text(text="Выберите возможные варианты съема и укажите цену",
                                        chat_id=message.chat.id,
                                        message_id=last_message, reply_markup=keyboard)

        except ValueError:
            await user_service.set_user_state(message.chat.id, 'price_month_creation')
            pass

    elif state == 'phone_creation':

        number = message.text

        if len(number) != 11:
            await user_service.set_user_state(message.from_user.id, 'phone_creation')

            keyboard = await lend_park_keyboard.phone_creation_keyboard()

            await bot.edit_message_text(chat_id=message.from_user.id, message_id=last_message,
                                        text="Вы ввели номер не коректно, "
                                             "пожалуйста введите номер в формате 78005553535 или 88005553535",
                                        reply_markup=keyboard)
        else:
            try:
                int(number)
                await lend_park_service.add_parking_data(message.chat.id, number, 'phone')

                keyboard = await lend_park_keyboard.create_lend_park_keyboard(message.chat.id)

                await bot.edit_message_text(text="Создание парковочного места", chat_id=message.chat.id,
                                            message_id=last_message, reply_markup=keyboard)
            except ValueError:
                await user_service.set_user_state(message.from_user.id, 'phone_creation')

                keyboard = await lend_park_keyboard.phone_creation_keyboard()

                await bot.edit_message_text(chat_id=message.from_user.id, message_id=last_message,
                                            text="Вы ввели номер не коректно, "
                                                 "пожалуйста введите номер в формате 78005553535 или 88005553535",
                                            reply_markup=keyboard)

    elif state == 'comment':
        comment = message.text

        if len(comment) > 300:
            await user_service.set_user_state(message.chat.id, 'comment')

            keyboard = types.InlineKeyboardMarkup(row_width=2). \
                add(types.InlineKeyboardButton(text='Назад', callback_data='lend_a_park'))

            await bot.edit_message_text(chat_id=message.chat.id, message_id=last_message,
                                        text="Ваш комментарий слишком длинный, "
                                             "максимальное количество символов равно тремста, "
                                             "введите комментарий заново",
                                        reply_markup=keyboard)

        else:
            await lend_park_service.add_parking_data(message.chat.id, comment, 'comment')

            keyboard = await lend_park_keyboard.create_lend_park_keyboard(message.chat.id)

            await bot.edit_message_text(text="Создание парковочного места", chat_id=message.chat.id,
                                        message_id=last_message, reply_markup=keyboard)
    elif state == 'img_link_1':
        data = await lend_park_service.get_pp_creation_data(message.from_user.id)

        if data.img_link_1:
            os.remove(data.img_link_1)

        destination = await message.photo[-1].download(destination_dir='img')

        await lend_park_service.add_parking_data(message.chat.id, destination.name, 'img_link_1')

        keyboard = await lend_park_keyboard.images_creation(message.from_user.id)

        await bot.edit_message_text(chat_id=message.from_user.id, message_id=last_message,
                                    text="Отправьте фото", reply_markup=keyboard)

    elif state == 'img_link_2':
        data = await lend_park_service.get_pp_creation_data(message.from_user.id)

        if data.img_link_2:
            os.remove(data.img_link_2)

        destination = await message.photo[-1].download(destination_dir='img')

        await lend_park_service.add_parking_data(message.chat.id, destination.name, 'img_link_2')

        keyboard = await lend_park_keyboard.images_creation(message.from_user.id)

        await bot.edit_message_text(chat_id=message.from_user.id, message_id=last_message,
                                    text="Отправьте фото", reply_markup=keyboard)

    elif state == 'img_link_3':
        data = await lend_park_service.get_pp_creation_data(message.from_user.id)

        if data.img_link_3:
            os.remove(data.img_link_3)

        destination = await message.photo[-1].download(destination_dir='img')

        await lend_park_service.add_parking_data(message.chat.id, destination.name, 'img_link_3')

        keyboard = await lend_park_keyboard.images_creation(message.from_user.id)

        await bot.edit_message_text(chat_id=message.from_user.id, message_id=last_message,
                                    text="Отправьте фото", reply_markup=keyboard)
    elif state == 'parking_number':
        await lend_park_service.add_parking_data(message.chat.id, message.text, 'parking_number')

        keyboard = await lend_park_keyboard.create_lend_park_keyboard(message.chat.id)

        await bot.edit_message_text(text="Создание парковочного места", chat_id=message.chat.id,
                                    message_id=last_message, reply_markup=keyboard)

    # start edit
    try:
        if state.startswith('edit_'):
            pp_id = state.split('_')[-1]
            if state.startswith('edit_address_'):

                address = message.text

                await owners_park_service.update_pp_data(pp_id, address, 'address')

                keyboard = await owners_park_keyboards.my_park_edit_keyboard(message.chat.id, pp_id)

                await bot.edit_message_text(text="Создание парковочного места", chat_id=message.chat.id,
                                            message_id=last_message, reply_markup=keyboard)
            elif state.startswith('edit_parking_number_'):

                await owners_park_service.update_pp_data(pp_id, message.text, 'parking_number')

                keyboard = await owners_park_keyboards.my_park_edit_keyboard(message.chat.id, pp_id)

                await bot.edit_message_text(text="Создание парковочного места", chat_id=message.chat.id,
                                            message_id=last_message, reply_markup=keyboard)
            elif state.startswith('edit_day_price_'):

                data = message.text
                try:
                    data = int(data)
                    await owners_park_service.update_pp_data(pp_id, data, 'price_day')

                    keyboard = await owners_park_keyboards.edit_parking_price_keyboard(pp_id)

                    await bot.edit_message_text(text="Выберите возможные варианты съема и укажите цену",
                                                chat_id=message.chat.id,
                                                message_id=last_message, reply_markup=keyboard)
                except ValueError:
                    await user_service.set_user_state(message.chat.id, f'edit_price_day_{pp_id}')
                    pass
            elif state.startswith('edit_week_price_'):
                data = message.text
                try:
                    data = int(data)
                    await owners_park_service.update_pp_data(pp_id, data, 'price_week')

                    keyboard = await owners_park_keyboards.edit_parking_price_keyboard(pp_id)

                    await bot.edit_message_text(text="Выберите возможные варианты съема и укажите цену",
                                                chat_id=message.chat.id,
                                                message_id=last_message, reply_markup=keyboard)
                except ValueError:
                    await user_service.set_user_state(message.chat.id, f'edit_price_week_{pp_id}')
                    pass
            elif state.startswith('edit_month_price_'):
                data = message.text
                try:
                    data = int(data)
                    await owners_park_service.update_pp_data(pp_id, data, 'price_month')

                    keyboard = await owners_park_keyboards.edit_parking_price_keyboard(pp_id)

                    await bot.edit_message_text(text="Выберите возможные варианты съема и укажите цену",
                                                chat_id=message.chat.id,
                                                message_id=last_message, reply_markup=keyboard)

                except ValueError or MessageNotModified:
                    await user_service.set_user_state(message.chat.id, f'edit_price_month_{pp_id}')
                    pass
            elif state.startswith('edit_phone_'):

                number = message.text

                if len(number) != 11:
                    await user_service.set_user_state(message.from_user.id, state)

                    keyboard = await owners_park_keyboards.parking_edit_keyboard_plug(pp_id)

                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=last_message,
                                                text="Вы ввели номер не корректно, "
                                                     "пожалуйста введите номер в формате 78005553535 или 88005553535",
                                                reply_markup=keyboard)

                else:
                    try:
                        int(number)
                        await owners_park_service.update_pp_data(pp_id, number, 'phone')

                        keyboard = await owners_park_keyboards.my_park_edit_keyboard(message.chat.id, pp_id)

                        await bot.edit_message_text(text="Редактирование Места", chat_id=message.chat.id,
                                                    message_id=last_message, reply_markup=keyboard)
                    except ValueError:
                        await user_service.set_user_state(message.from_user.id, state)

                        keyboard = await owners_park_keyboards.parking_edit_keyboard_plug(pp_id)

                        await bot.edit_message_text(chat_id=message.from_user.id, message_id=last_message,
                                                    text="Вы ввели номер не корректно, "
                                                         "пожалуйста введите номер в формате 78005553535 или "
                                                         "88005553535",
                                                    reply_markup=keyboard)
            elif state.startswith('edit_comment_'):
                comment = message.text

                if len(comment) > 300:
                    await user_service.set_user_state(message.chat.id, 'comment')

                    keyboard = types.InlineKeyboardMarkup(row_width=2).\
                        add(types.InlineKeyboardButton(text='Назад', callback_data=f'edit_park_back_{pp_id}'))

                    await bot.edit_message_text(chat_id=message.chat.id, message_id=last_message,
                                                text="Ваш комментарий слишком длинный, "
                                                     "максимальное количество символов равное трёмста, "
                                                     "введите комментарий заново",
                                                reply_markup=keyboard)

                else:
                    await owners_park_service.update_pp_data(pp_id, comment, 'comment')

                    keyboard = await owners_park_keyboards.my_park_edit_keyboard(message.chat.id, pp_id)

                    await bot.edit_message_text(text="Редактирование Места", chat_id=message.chat.id,
                                                message_id=last_message, reply_markup=keyboard)
            elif state.startswith('edit_link_img_'):
                img_number = state.split('_')[-2]

                data = await lend_park_service.get_pp_creation_data(message.from_user.id)
                data_updated = await owners_park_service.get_pp_data_to_edit(pp_id)
                if img_number == 1:
                    if data.img_link_1 != data_updated.img_link_1:
                        os.remove(data_updated.img_link)
                elif img_number == 2:
                    if data.img_link_2 != data_updated.img_link_2:
                        os.remove(data_updated.img_link)
                elif img_number == 3 != data_updated.img_link_3:
                    if data.img_link_2:
                        os.remove(data_updated.img_link)
                destination = await message.photo[-1].download(destination_dir='img')

                await owners_park_service.update_pp_data(pp_id, destination.name, f'img_link_{img_number}')

                keyboard = await owners_park_keyboards.edit_images_keyboard(pp_id)

                await bot.edit_message_text(chat_id=message.from_user.id, message_id=last_message,
                                            text="Выберите и отправьте фото", reply_markup=keyboard)
            elif state.startswith('edit_date_start_'):
                date = message.text

                await owners_park_service.update_pp_data(pp_id, date, 'date_create')

                keyboard = await owners_park_keyboards.my_park_edit_keyboard(message.chat.id, pp_id)

                await bot.edit_message_text(text="Создание парковочного места", chat_id=message.chat.id,
                                            message_id=last_message, reply_markup=keyboard)
            elif state.startswith('edit_date_end_'):
                pass


    except (AttributeError, MessageNotModified):
        pass
    await bot.delete_message(message.chat.id, message.message_id)


def register_process_message(dp: Dispatcher):
    dp.register_message_handler(process_message, state='*', content_types=types.ContentTypes.ANY)
