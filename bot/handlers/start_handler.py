from aiogram import Bot, Dispatcher, types
from bot.keyboards import start_keyboards
from services import user_service

from settings import BotConfig

bot = Bot(token=BotConfig.token)


async def main_menu(message: types.Message):
    keyboard = await start_keyboards.create_main_menu_keyboard()

    mes = await message.answer(text='Главное меню', reply_markup=keyboard)
    await bot.delete_message(message.chat.id, message.message_id)

    await user_service.create_user(message.from_user.id, message.from_user.username, mes['message_id'])


async def main_menu_callback(call: types.CallbackQuery):
    keyboard = await start_keyboards.create_main_menu_keyboard()

    user_last_message = await user_service.get_user_last_message(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=user_last_message,
                                text="Главное меню", reply_markup=keyboard)


def register_main_menu(dp: Dispatcher):
    dp.register_message_handler(main_menu, commands="start", state="*", content_types=types.ContentTypes.ANY)
    dp.register_callback_query_handler(main_menu_callback, text='main_menu')
