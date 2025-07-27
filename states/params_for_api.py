# ФСМ для выбора мощности стабилизатора по силе тока
from aiogram.fsm.state import StatesGroup, State


class Params(StatesGroup):
    phase = State()
    current = State()
    voltage = State()
