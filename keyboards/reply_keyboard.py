# Создание реплай клавиатуры
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from sqlalchemy.sql.functions import user

import filters
from keyboards.keyboard_maker import get_keyboard

main_menu = get_keyboard(
    "О нашей продукции",
    "Рассчитать мощность стабилизатора",
    "Дополнительные услуги",
    "Цены и ассортимент",
    "Оформить заявку на обратную связь",
    placeholder="Выберите что Вас интересует:",
    sizes=(2,)
)

# main_menu_admin = get_keyboard("О нашей продукции",
#                                "Рассчитать мощность стабилизатора",
#                                "Дополнительные услуги",
#                                "Цены и ассортимент",
#                                "Оформить заявку на обратную связь",
#                                "/admin",
#                                placeholder="Выберите что Вас интересует:",
#                                sizes=(2,))

button_phone = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Отправить контакт: ", request_contact=True)],
        ],
        resize_keyboard=True
)


