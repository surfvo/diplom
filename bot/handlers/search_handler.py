from aiogram import Bot, Dispatcher, types
from bot.keyboards import search_park_keyboard
from services import search_service, user_service
from services import lend_park_service
from datetime import datetime
from aiogram.utils.exceptions import MessageNotModified
import json
from settings import BotConfig
bot = Bot(token=BotConfig.token)


async def send_parkings(call: types.CallbackQuery):
    parking_places = await search_service.get_pps(call.from_user.id)

    for pp in parking_places:
        links = []
        links.append(pp.img_link_1 if pp.img_link_1 is not None else None)
        links.append(pp.img_link_2 if pp.img_link_2 is not None else None)
        links.append(pp.img_link_3 if pp.img_link_3 is not None else None)

        media = types.MediaGroup()
        for link in links:
            if link is not None:
                media.attach_photo(types.InputFile(link))
        await bot.send_media_group(call.message.chat.id, media=media)
        await bot.send_message(call.from_user.id, text=f'адрес: {pp.address}\n'
                                                       f'место: {pp.parking_number}\n'
                                                       f'ценна день: {pp.price_day}\n'
                                                       f'ценна неделя: {pp.price_week}\n'
                                                       f'ценна месяц: {pp.price_month}\n'
                                                       f'сдается с {pp.date_start} по {pp.date_end}\n'
                                                       f'Комментарий: {pp.comment}\n'
                                                       f'Номер телефона: {pp.phone}\n'
                                                       f'Телеграм: @{pp.name}\n'
                                                       f'-------------------------')


def register_search_park(dp: Dispatcher):
    dp.register_callback_query_handler(send_parkings, text='rent_a_park')