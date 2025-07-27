# Хэндлеры для обработки сообщений пользователя
from aiogram import F
from aiogram.types import Message, CallbackQuery

import keyboards.inline_keyboard as kb
from keyboards.reply_keyboard import main_menu
from keyboards.bilder_keyboard import categories, items

import database_voltgrom.requests as rq
from utils import calculate_power, user_data
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


# Обработка текстовых сообщений
@router.message(F.text == "О нашей продукции")
async def info_message(message: Message):
    await message.reply(text=f"{message.from_user.first_name}, выберите что Вас интересует:",
                        reply_markup=kb.product_info)


@router.message(F.text == "Рассчитать мощность стабилизатора")
async def power_message(message: Message):
    await message.reply(text=f"Выберите способ расчёта:",
                        reply_markup=kb.change_by_)


@router.message(F.text == "Дополнительные услуги")
async def service_message(message: Message):
    await message.reply(
        text="Наша команда специалистов рада предоставить следующие услуги:\n\n"
             "1. Обмотка/Перемотка трансформаторов;\n"
             "2. Ремонт стабилизаторов любой марки и модели;\n"
             "3. Установка стабилизаторов.\n\n"
             "P.S. Работаем как с физическими, так и с юридическими лицами.",
        reply_markup=main_menu
    )


@router.message(F.text == "Цены и ассортимент")
async def catalog(message: Message, session: AsyncSession):
    await message.answer(text="Чтобы узнать цену, выберите количество фаз: ",
                         reply_markup=await categories(session))


# Обработка колбэков главного меню
@router.callback_query(F.data == 'common_info')
async def common_message(callback: CallbackQuery):
    await callback.answer("Вы выбрали 'Общая информация'")
    await callback.message.answer(
        text="Общая информация: \n\nАвтоматический cтабилизатор напряжения VoltGrom "
             "предназначен для обеспечения стабильным "
             "напряжением подключенных к нему устройств. Широко "
             "используется в бытовых и промышленных сферах для "
             "защиты техники от аварийных скачков "
             "электроэнергии. Данная модель оборудована "
             "светодиодной индикацией и цифровыми дисплеями для "
             "удобного контроля состояния устройства.",
        reply_markup=main_menu
    )


@router.callback_query(F.data == 'tech_specific')
async def tech_specific_message(callback: CallbackQuery):
    await callback.answer("Вы выбрали 'Технические характеристики'")
    await callback.message.answer(
        text="Технические характеристики\n\nВходное напряжение: 90-280 V\nВыходное напряжение: 220 V (+ -"
             "8%)\nКоличество фаз: 1, 3\nМощность 3, 5, 6, 10, 15, 20, 25, "
             "30 kVa\nТИП ступенчатые релейные(шаг 15 V)",
        reply_markup=main_menu
    )


@router.callback_query(F.data == 'condition')
async def tech_specific_message(callback: CallbackQuery):
    await callback.answer("Вы выбрали 'Условия гарантии'")
    await callback.message.answer(
        text="Условия гарантии\n\n1 год - полная гарантия, \n2 года - сервисная.",
        reply_markup=main_menu
    )


@router.callback_query(F.data == 'contact_info')
async def back_message(callback: CallbackQuery):
    await callback.answer("Наши контакты")
    phone_number = +998909661612
    await callback.message.answer(
        text="Контактная информация:\n\nТелефон: {phone} Андрей Викторович"
             "\nРежим работы: Пн-Сб. 9:00- 17:00".format(phone=phone_number),
        reply_markup=main_menu
    )
    await callback.message.answer_location(latitude=41.312377, longitude=69.316523)


# Колбэк для возврата в главное меню
@router.callback_query(F.data == 'back')
async def back_message(callback: CallbackQuery):
    await callback.answer("Вы действительно хотите вернуться в главное меню?", show_alert=True)
    await callback.message.answer(
        text="Выберите что Вас интересует:",
        reply_markup=main_menu
    )


# Колбэки для выбора товара
@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery, session: AsyncSession):
    await callback.answer("Вы выбрали стабилизатор по количеству фаз")
    await callback.message.answer('Теперь выберите стабилизатор по мощности:',
                                  reply_markup=await items(callback.data.split('_')[1], session))


@router.callback_query(F.data.startswith('item_'))
async def item(callback: CallbackQuery, session: AsyncSession):
    item_data = await rq.get_item(int(callback.data.split('_')[1]), session)
    await callback.answer("Вы выбрали стабилизатор по мощности")
    await callback.message.answer_photo(photo=item_data.image,
                                        caption=f"Название: стабилизатор переменного тока Voltgrom{item_data.name}\nОписание: {item_data.description}\n\nЦена: {item_data.price}$")


# Колбэки для калькулятора мощности
@router.callback_query(lambda c: c.data == "calculate_power")
async def process_calculate_power(callback: CallbackQuery):
    await callback.answer(" ")
    await callback.message.answer(text="Выберите устройства для расчета мощности:", reply_markup=kb.devices_keyboard)


@router.callback_query(lambda c: c.data.startswith('device_'))
async def process_device_power(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    device_name = callback_query.data.split('_')[1]

    # Сохраняем выбранное устройство для пользователя
    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id][device_name] = user_data[user_id].get(device_name, 0) + 1

    await callback_query.answer(f"Добавлен {device_name}.")


@router.callback_query(lambda c: c.data == "calculate_total_power")
async def process_calculate_total_power(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id not in user_data or not user_data[user_id]:
        await callback_query.answer(text="Сначала выберите устройства для расчета мощности.")
        return

    devices = user_data[user_id]
    total_power = round(calculate_power(devices), 2)
    total_power_kW = round(total_power / 1000, 2)

    await callback_query.answer(text=f"Общая мощность выбранных устройств: {total_power} Вт.")
    await callback_query.message.answer(text=f"Вам необходим стабилизатор мощностью не менее: {total_power_kW} кВА",
                                        reply_markup=main_menu)
    del user_data[user_id]

