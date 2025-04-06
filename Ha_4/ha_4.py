#Python Advanced: Домашнее задание 4
#Задача 1: Наполнение данными
#Добавьте в базу данных следующие категории и продукты
#Добавление категорий: Добавьте в таблицу categories следующие категории:
#Название: "Электроника", Описание: "Гаджеты и устройства."
#Название: "Книги", Описание: "Печатные книги и электронные книги."
#Название: "Одежда", Описание: "Одежда для мужчин и женщин."
#Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый продукт связан с соответствующей категорией:
#Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
#Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
#Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
#Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
#Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда
#Задача 2: Чтение данных
#Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все
# связанные с ней продукты, включая их названия и цены.
#Задача 3: Обновление данных
#Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.
#Задача 4: Агрегация и группировка
#Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.
#Задача 5: Группировка с фильтрацией
#Отфильтруйте и выведите только те категории, в которых более одного продукта.



from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Задача 1: Создание движка для SQLite в памяти
engine = create_engine("sqlite:///:memory:", echo=True)

# Базовый класс для моделей
Base = declarative_base()


# Задача 4: Определение модели категории
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    products = relationship("Product", back_populates="category")


# Задача 3: Определение модели продукта
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))  # Задача 5: Связь между таблицами

    category = relationship("Category", back_populates="products")


# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Задача 2: Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Задача 1: Наполнение данными
categories_data = [
    {"name": "Электроника", "description": "Гаджеты и устройства."},
    {"name": "Книги", "description": "Печатные книги и электронные книги."},
    {"name": "Одежда", "description": "Одежда для мужчин и женщин."}
]

categories = {cat["name"]: Category(**cat) for cat in categories_data}
session.add_all(categories.values())
session.commit()

products_data = [
    {"name": "Смартфон", "price": 299.99, "in_stock": True, "category": categories["Электроника"]},
    {"name": "Ноутбук", "price": 499.99, "in_stock": True, "category": categories["Электроника"]},
    {"name": "Научно-фантастический роман", "price": 15.99, "in_stock": True, "category": categories["Книги"]},
    {"name": "Джинсы", "price": 40.50, "in_stock": True, "category": categories["Одежда"]},
    {"name": "Футболка", "price": 20.00, "in_stock": True, "category": categories["Одежда"]}
]

session.add_all([Product(**prod) for prod in products_data])
session.commit()

# Задача 2: Чтение данных
categories = session.query(Category).all()
for category in categories:
    print(f"Категория: {category.name} ({category.description})")
    for product in category.products:
        print(f"  - {product.name}: {product.price} USD")

# Задача 3: Обновление данных
smartphone = session.query(Product).filter_by(name="Смартфон").first()
if smartphone:
    smartphone.price = 349.99
    session.commit()
    print("Цена смартфона обновлена.")

# Задача 4: Агрегация и группировка
category_counts = (
    session.query(Category.name, func.count(Product.id))
    .join(Product)
    .group_by(Category.id)
    .all()
)
print("Общее количество продуктов в каждой категории:")
for category, count in category_counts:
    print(f"{category}: {count}")

# Задача 5: Группировка с фильтрацией
filtered_categories = (
    session.query(Category.name)
    .join(Product)
    .group_by(Category.id)
    .having(func.count(Product.id) > 1)
    .all()
)
print("Категории с более чем одним продуктом:")
for category in filtered_categories:
    print(category[0])




