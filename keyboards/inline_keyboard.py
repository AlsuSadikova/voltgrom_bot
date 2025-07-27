# Создание инлайн клавиатуры
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


product_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Общая информация", callback_data='common_info')],
    [InlineKeyboardButton(text="Технические характеристики", callback_data="tech_specific")],
    [InlineKeyboardButton(text="Перейти на сайт", url="https://grom.uz")],
    [InlineKeyboardButton(text="Условия гарантии", callback_data="condition")],
    [InlineKeyboardButton(text="Контактная информация", callback_data="contact_info")],
    [InlineKeyboardButton(text="->Вернуться в главное меню", callback_data="back")]]
)


devices_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Телевизор - 300 Вт", callback_data="device_TV")],
    [InlineKeyboardButton(text="Тостер - 800 Вт", callback_data="device_toaster")],
    [InlineKeyboardButton(text="Электро-чайник - 2000 Вт", callback_data="device_kettle")],
    [InlineKeyboardButton(text="Компьютер - 500 Вт", callback_data="device_PC")],
    [InlineKeyboardButton(text="Кофеварка - 1000 Вт", callback_data="device_coffeeMaker")],
    [InlineKeyboardButton(text="Принтер - 500 Вт", callback_data="device_printer")],
    [InlineKeyboardButton(text="Холодильник - 600 Вт", callback_data="device_fridge")],
    [InlineKeyboardButton(text="СВЧ-печь - 1400 Вт", callback_data="device_microwave")],
    [InlineKeyboardButton(text="Утюг - 1700 Вт", callback_data="device_iron")],
    [InlineKeyboardButton(text="Вентиляторы - 1000 Вт", callback_data="device_fans")],
    [InlineKeyboardButton(text="Фен для волос - 1200 Вт", callback_data="device_hairDryer")],
    [InlineKeyboardButton(text="Обогреватель - 1500 Вт", callback_data="device_heater")],
    [InlineKeyboardButton(text="Стиральная машина - 2500 Вт", callback_data="device_washingMachine")],
    [InlineKeyboardButton(text="Пылесос - 1700 Вт", callback_data="device_vacuum")],
    [InlineKeyboardButton(text="Духовка - 2000 Вт", callback_data="device_oven")],
    [InlineKeyboardButton(text="Освещение - 1000 Вт", callback_data="device_lighting")],
    [InlineKeyboardButton(text="Кондиционер - 1500 Вт", callback_data="device_airConditioner")],
    [InlineKeyboardButton(text="Электро-плита - 3000 Вт", callback_data="device_electricStove")],
    [InlineKeyboardButton(text="Бойлер - 1500 Вт", callback_data="device_boiler")],
    [InlineKeyboardButton(text="Дрель - 800 Вт", callback_data="device_drill")],
    [InlineKeyboardButton(text="Электро-точило - 900 Вт", callback_data="device_grinder")],
    [InlineKeyboardButton(text="Перфоратор - 1200 Вт", callback_data="device_perforator")],
    [InlineKeyboardButton(text="Дисковая пила - 1300 Вт", callback_data="device_circularSaw")],
    [InlineKeyboardButton(text="Электро-лобзик - 700 Вт", callback_data="device_jigsaw")],
    [InlineKeyboardButton(text="Шлифовальная машина - 1700 Вт", callback_data="device_sander")],
    [InlineKeyboardButton(text="Электро-рубанок - 900 Вт", callback_data="device_planer")],
    [InlineKeyboardButton(text="Компрессор - 2000 Вт", callback_data="device_compressor")],
    [InlineKeyboardButton(text="Водяной насос - 1000 Вт", callback_data="device_waterPump")],
    [InlineKeyboardButton(text="Газонокосилка - 1500 Вт", callback_data="device_lawnMower")],
    [InlineKeyboardButton(text="Электро-моторы - 1500 Вт", callback_data="device_electricMotors")],
    [InlineKeyboardButton(text="Проточный нагреватель - 5000 Вт", callback_data="device_flowHeater")],
    [InlineKeyboardButton(text="Сварочный аппарат - 2300 Вт", callback_data="device_weldingMachine")],
    [InlineKeyboardButton(text="Рассчитать общую мощность", callback_data="calculate_total_power")],
    [InlineKeyboardButton(text="->Назад", callback_data="back")]
    ]
)


change_by_ = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="По электроприборам", callback_data="calculate_power")],
    [InlineKeyboardButton(text="По силе тока", callback_data="current")],
    [InlineKeyboardButton(text="->Вернуться в главное меню", callback_data="back")]])


phase_change_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Однофазные', callback_data="single_phase")],
    [InlineKeyboardButton(text='Трёхфазные', callback_data="three_phase")],
    [InlineKeyboardButton(text="->Вернуться в главное меню", callback_data="back")]])