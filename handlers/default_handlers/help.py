# Хэндлер, отображающий информацию о командах
from aiogram.types import Message
from aiogram.filters import Command

from config import private
from aiogram import Router


router = Router()


@router.message(Command('help'))
async def bot_help(message: Message):
    text = [f"/{command[1]} - {description[1]}" for command, description in private]
    await message.reply(text="\n".join(text))

