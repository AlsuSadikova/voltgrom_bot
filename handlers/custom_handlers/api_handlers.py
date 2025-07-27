# Хэндлеры по работе с Апи стороннего сайта
import os

import requests
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from keyboards.inline_keyboard import phase_change_keyboard
from keyboards.reply_keyboard import main_menu
from states.params_for_api import Params
from aiogram import Router, F
from dotenv import load_dotenv

load_dotenv()

api_router = Router()


@api_router.callback_query(lambda c: c.data == "current")
async def begin_process_current(callback: CallbackQuery, state=FSMContext):
    await callback.answer("Введите данные")
    await state.set_state(Params.current)
    await callback.message.answer('Введите номинал вводного автомата (A): ')


@api_router.message(Params.current)
async def get_volt(message: Message, state: FSMContext):
    try:
        await state.update_data(current=int(message.text))
        await state.set_state(Params.voltage)
        await message.answer('Введите входное напряжение (V):')
    except ValueError:
        await message.answer('Нужно ввести число: ')


@api_router.message(Params.voltage)
async def get_volt(message: Message, state: FSMContext):
    try:
        await state.update_data(voltage=int(message.text))
        await state.set_state(Params.phase)
        await message.answer('Введите количество фаз:', reply_markup=phase_change_keyboard)
    except ValueError:
        await message.answer('Нужно ввести число: ')


@api_router.callback_query(lambda c: c.data, Params.phase)
async def get_phase(callback: CallbackQuery, state: FSMContext):
    await callback.answer("производится расчёт по силе тока:")
    await state.update_data(phase=callback.data)
    await state.set_state(Params.phase)

    final_data = await state.get_data()
    cur = int(final_data['current'])
    volt = int(final_data['voltage'])
    phase_change = str(final_data['phase'])

    url = os.path.join(os.getenv('API_URL'), phase_change)
    querystring = {"current": f"{cur}", "voltage": f"{volt}", "powerfactor": "0.95"}

    headers = {
        "x-rapidapi-key": "2bdf41e5cbmshd92b71b9b2bb1c5p12ddd6jsn6bd8618bf266",
        "x-rapidapi-host": "electrical-units.p.rapidapi.com"
    }

    response = requests.get(url=url, headers=headers, params=querystring)

    answer_from_api = response.json()

    await callback.message.answer(
        text=f"Вам необходим стабилизатор мощностью не меньше {round(answer_from_api['power'] / 1000, 2)}кВА.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
    await callback.message.answer(
        text="Вернуться в главное меню",
        reply_markup=main_menu
    )


