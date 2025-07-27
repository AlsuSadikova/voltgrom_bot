# Хэндлер, отображающий информацию о разработчике бота
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router


router = Router()


@router.message(Command('about_dew'))
async def bot_about_dew(message: Message):
    await message.reply(text="@AlsuSadikova")
