#Python Advanced: Домашнее задание 3
#Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.
#Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.
#Задача 3: Определите модель продукта Product со следующими типами колонок:
#id: числовой идентификатор
#name: строка (макс. 100 символов)
#price: числовое значение с фиксированной точностью
#in_stock: логическое значение
#Задача 4: Определите связанную модель категории Category со следующими типами колонок:
#id: числовой идентификатор
#name: строка (макс. 100 символов)
#description: строка (макс. 255 символов)
#Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id.


from sqlalchemy import create_engine, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Mapped, mapped_column

engine = create_engine("sqlite:///:memory:", echo=True, echo_pool=True)

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255))

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column( Numeric(8,2), nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))  # Задача 5: Связь между таблицами

    category = relationship("Category", back_populates="products")


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()
session.close()

















