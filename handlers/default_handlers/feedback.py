# Хэндлер, для сбора информации о клиенте(ФСМ)
import os

from aiogram import F

from aiogram.filters import StateFilter, Command
from aiogram.filters.logic import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from database_voltgrom.requests import set_name_phone
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply_keyboard import button_phone, main_menu
from states.registration import UserInfo
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession


router = Router()


# Запрашиваем имя и контакт для связи с потенциальным клиентом
@router.message(Command("feedback"))
@router.message(F.text == 'Оформить заявку на обратную связь')
async def start_reg(message: Message, state: FSMContext):
    """
    Start command. Here we are starting state
    """

    await state.set_state(UserInfo.name)
    await message.answer('Введите имя:')


@router.message(or_f(Command("отмена")), (F.text.casefold() == "отмена"))
async def cancel_handler(message: Message) -> None:
    await message.answer("Действия отменены", reply_markup=main_menu)


@router.message(UserInfo.name, F.text)
async def get_name(message: Message, state: FSMContext):
    """
    State 1. Will process when user's state is MyStates.name.
    """
    await state.update_data(name=message.text)
    await state.set_state(UserInfo.phone_num)
    await message.answer('Введите номер телефона +', reply_markup=button_phone)


@router.message(UserInfo.name)
async def get_name(message: Message):
    """
    State 1. Will process when user's state is MyStates.name.
    """
    await message.answer('Вы ввели недопустимые данные. Введите имя:')


@router.message(UserInfo.phone_num, F.contact | F.text)
async def ready_for_answer(message: Message, state: FSMContext, session: AsyncSession):
    """
    State 3. Will process when user's state is MyStates.age.
    """
    if message.contact:
        phone_num = message.contact.phone_number
    else:
        phone_num = message.text
    await state.update_data(phone_num=phone_num)

    data = await state.get_data()

    await message.bot.send_message(chat_id=444690052,
                                   text=f"Новый заказ:\nИмя: {data['name']}\nТелефон: {data['phone_num']}")
    await message.reply(
        f"Регистрация прошла успешно!\nВаше имя: {data['name']}\nНомер телефона: {data['phone_num']}\nНаши специалисты "
        f"свяжутся с Вами в ближайшее время", reply_markup=main_menu)

    new_order = await set_name_phone(session, data)
    # await set_name_phone(session, data)
    await state.clear()


#     # Отправляем данные о клиенте администратору
#   await bot.send_message(message_chat_id='ADMIN_ID', text=f"Новый заказ {datetime.now}: {data['name']}\nНомер телефона: {data['phone_num']}")
