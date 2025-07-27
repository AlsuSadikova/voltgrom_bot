# Класс, для сбора информации о клиенте(ФСМ)
from aiogram.fsm.state import StatesGroup, State


class UserInfo(StatesGroup):
    name = State()
    phone_num = State()





