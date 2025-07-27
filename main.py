# Производим необходимые импорты
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from database_voltgrom.enginy import create_db, session_maker, drop_db

from middlewares.db_middleware import DataBaseSession

from handlers.custom_handlers import api_handlers, custom, user_group, admin_panel
from handlers.default_handlers import about_dew, help, start, feedback

from config import private



#  Инициализация бота и диспетчера
bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# bot.my_admins_list = []
dp = Dispatcher()

# Подключение роутеров для обработки событий
dp.include_routers(api_handlers.api_router, custom.router,
                   about_dew.router, help.router, start.router,
                   feedback.router, admin_panel.admin_router)


async def on_startup(bot):

#    await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')


# Функция для запуска бота
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


# Точка запуска
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
