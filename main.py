import logging
import asyncio


from bot.handlers import start_handler, lend_park_handler, message_processing_handler,\
    owners_park_handler, search_handler


from settings import BotConfig

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BotConfig.token)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    start_handler.register_main_menu(dp)
    lend_park_handler.register_lend_park(dp)
    message_processing_handler.register_process_message(dp)
    owners_park_handler.register_owners_park(dp)
    search_handler.register_search_park(dp)

    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
