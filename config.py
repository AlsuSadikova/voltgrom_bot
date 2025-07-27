# Здесь хранятся конфигурации
from aiogram.types import BotCommand


private = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Вывести справку"),
        BotCommand(command="feedback", description="Оставить заявку на обратную связь"),
        BotCommand(command="about_dew", description="Разработчик бота")
    ]


SQL_ALCHEMY="sqlite+aiosqlite:///db.sqlite3"





