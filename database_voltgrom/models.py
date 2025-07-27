# Производим необходимые импорты
from typing import Optional

from sqlalchemy import DateTime, Float, String, Text, func, BigInteger, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime


# Создаём родительский базовый класс
class Base(AsyncAttrs, DeclarativeBase):
    pass
    # created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    # updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


# Модель для категории товара
class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))

    text = {'Category:name': 'Введите количество фаз заново'}


# Модель для значений категории товара
class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(125))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    image: Mapped[str] = mapped_column(String(125))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    # category: Mapped['Category'] = relationship(backref='items')

    # texts = {
    #     'Item:name': 'Введите название заново:',
    #     'Item:description': 'Введите описание заново:',
    #     'Item:price': 'Введите стоимость заново:',
    #     'Item:image': 'Этот стейт последний, поэтому...',
    # }


# модель для пользователя
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)


# модель для клиента
class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now())
    updated: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    name: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)
    item_name: Mapped[str] = mapped_column(String(150), nullable=True)



