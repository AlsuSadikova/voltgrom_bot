from database_voltgrom.models import User, Category, Item, Client
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update


# Добавление новых пользователей
async def set_user(tg_id: int, session: AsyncSession):
    user = session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        session.add(User(tg_id=tg_id))
        await session.commit()


# Добавление новых клиентов
async def set_name_phone(session: AsyncSession, data: dict):
    clients = Client(
        name=data['name'],
        phone=str(data['phone_num'])
    )

    session.add(clients)
    await session.commit()


async def orm_add_product(session: AsyncSession, data: dict):
    obj = Item(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],
        category=data["category"]
    )
    session.add(obj)
    await session.commit()


#
# async def get_clients(session: AsyncSession):
#     return await session.scalars(select(User))


# Просмотр категорий товаров
async def orm_get_products(session: AsyncSession):
    query = select(Item)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, item_id: int):
    query = select(Item).where(Item.id == item_id)
    result = await session.execute(query)
    return result.scalar()


async def get_categories(session: AsyncSession):
    return await session.scalars(select(Category))


# Просмотр значений категорий товаров
async def get_category_item(category_id, session: AsyncSession):
    return await session.scalars(select(Item).where(Item.category == category_id))


# Просмотр выбранного товара
async def get_item(item_id: int, session: AsyncSession):
    return await session.scalar(select(Item).where(Item.id == item_id))


async def orm_update_product(session: AsyncSession, item_id: int, data):
    query = update(Item).where(Item.id == item_id).values(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],
        category=data["category"])
    await session.execute(query)
    await session.commit()


async def orm_delete_product(item_id: int, session: AsyncSession):
    query = delete(Item).where(Item.id == item_id)
    await session.execute(query)
    await session.commit()
