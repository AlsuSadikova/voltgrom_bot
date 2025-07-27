# Хэндлер, срабатывающий при запуске бота
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

import filters
from database_voltgrom.requests import set_user
import keyboards.reply_keyboard as kb
from aiogram import Router

from handlers.custom_handlers.admin_panel import ADMIN_KB

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    # Ловим телеграм айди пользователя
    await set_user(message.from_user.id, session)
    await message.reply(f"Привет, {message.from_user.first_name}!",
                        reply_markup=kb.main_menu)
