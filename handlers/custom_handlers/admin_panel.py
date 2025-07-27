from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database_voltgrom.models import Category, Item
from database_voltgrom.requests import orm_add_product, get_category_item, orm_get_products, orm_delete_product, \
    orm_get_product, orm_update_product
from filters.chat_types import ChatTypeFilter, IsAdmin

from keyboards.keyboard_maker import get_keyboard, get_callback_btns

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB = get_keyboard(
    "Добавить стабилизатор",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2,)
)


# Код ниже для машины состояний (FSM)
class AddProduct(StatesGroup):
    # Шаги состояний
    category = State()
    name = State()
    description = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        'AddProduct:category': 'Выберите категорию:',
        'AddProduct:name': 'Введите название заново:',
        'AddProduct:description': 'Введите описание заново:',
        'AddProduct:price': 'Введите стоимость заново:',
        'AddProduct:image': 'Этот стейт последний, поэтому...',
    }


@admin_router.message(Command('admin'))
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB, )


@admin_router.message(F.text == "Ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    try:
        products = await orm_get_products(session)
        for product in products:
            await message.answer_photo(
                product.image,
                caption=f"<strong>{product.name}\ </strong>\nВходное напряжение: 90-280 V\nВыходное напряжение: 220 V "
                        f"(+ - 8%)\nКоличество фаз: 1, 3\nМощность 3, 5, 6, 10, 15, 20, 25,30 kVa\nТИП ступенчатые "
                        f"релейные(шаг 15 V)\nСтоимость: {round(product.price, 2)}$.",
                reply_markup=get_callback_btns(
                    btns={
                        "Удалить": f"delete_{product.id}",
                        "Изменить": f"change_{product.id}",
                    }
                ),
            )
        await message.answer("ОК, вот список товаров ⏫")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(int(product_id), session)

    await callback.answer("Товар удален")
    await callback.message.answer("Товар удален!")


@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product_callback(
        callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]

    product_for_change = await orm_get_product(session, int(product_id))

    AddProduct.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        "Введите количество фаз", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.category)


# Становимся в состояние ожидания ввода категории стабилизаторов
@admin_router.message(StateFilter(None), F.text == "Добавить стабилизатор")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите количество фаз", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.category)


# Хендлер отмены и сброса состояния должен быть всегда именно хдесь,
# после того как только встали в состояние номер 1 (элементарная очередность фильтров)
@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


# Вернутся на шаг назад (на прошлое состояние)
@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.category:
        await message.answer('Предыдущего шага нет, или введите количество фаз или напишите "отмена"')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}")
            return
        previous = step


# Ловим данные для состояния name и потом меняем состояние на description
@admin_router.message(AddProduct.category, or_f(F.text, F.text == "."))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(category=AddProduct.product_for_change.category)
    elif message.text == "1":
        await state.update_data(category=1)
    elif message.text == "3":
        await state.update_data(category=2)
    else:
        await message.answer("Вы ввели не допустимые данные, введите заново")
        return
    await message.answer("Введите мощность стабилизатора")
    await state.set_state(AddProduct.name)


# Хендлер для отлова некорректных вводов для состояния name
@admin_router.message(AddProduct.category)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите заново")


# Хендлер для отлова некорректных вводов для состояния name
@admin_router.message(AddProduct.name, or_f(F.text, F.text == "."))
async def add_name2(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        await state.update_data(name=message.text + "кВа")
    await message.answer("Введите описание")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите заново")


# Ловим данные для состояния description и потом меняем состояние на price
@admin_router.message(AddProduct.description, or_f(F.text, F.text == "."))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Введите цену")
    await state.set_state(AddProduct.price)


# Хендлер для отлова некорректных вводов для состояния description
@admin_router.message(AddProduct.description)
async def add_description2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст описания товара")


# Ловим данные для состояния price и потом меняем состояние на image
@admin_router.message(AddProduct.price, or_f(F.text, F.text == "."))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Введите корректное значение цены")
            return

        await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)


# Хендлер для отлова некорректного ввода для состояния price
@admin_router.message(AddProduct.price)
async def add_price2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите стоимость товара")


# Ловим данные для состояния image и потом выходим из состояний
@admin_router.message(AddProduct.image, or_f(F.photo, F.text == "."))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == ".":
        await state.update_data(image=AddProduct.product_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
        await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    if AddProduct.product_for_change:
        await orm_update_product(session, AddProduct.product_for_change.id, data)
    else:
        await orm_add_product(session, data)
    await message.answer("Товар добавлен/изменен", reply_markup=ADMIN_KB)
    await message.answer(str(data))
    await state.clear()

    AddProduct.product_for_change = None


@admin_router.message(AddProduct.image)
async def add_image2(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото")
