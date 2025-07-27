# Создание билдер клавиатуры
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from database_voltgrom.requests import get_categories, get_category_item


# Функция для выбора стабилизаторов по количеству фаз
async def categories(session: AsyncSession):
    all_categories = await get_categories(session)
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='back'))
    return keyboard.adjust(2).as_markup()


# Функция для выбора стабилизаторов по мощности
async def items(category_id, session: AsyncSession):
    all_items = await get_category_item(category_id, session)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='back'))
    return keyboard.adjust(2).as_markup()
