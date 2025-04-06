from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Задача 1: Создание движка для SQLite в памяти
engine = create_engine("sqlite:///:memory:", echo=True)

# Базовый класс для моделей
Base = declarative_base()


# Задача 4: Определение модели категории продуктов
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    products = relationship("Product", back_populates="category")


# Определение модели категории вопросов
class QuestionCategory(Base):
    __tablename__ = "question_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    questions = relationship("Question", back_populates="category")


# Задача 3: Определение модели продукта
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))  # Связь между таблицами

    category = relationship("Category", back_populates="products")


# Определение модели вопроса
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("question_categories.id"))  # Связь с категорией вопросов

    category = relationship("QuestionCategory", back_populates="questions")


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

# Добавление категорий вопросов
question_categories_data = [
    {"name": "Общие знания"},
    {"name": "Наука"},
    {"name": "История"}
]

question_categories = {cat["name"]: QuestionCategory(**cat) for cat in question_categories_data}
session.add_all(question_categories.values())
session.commit()

# Добавление вопросов
questions_data = [
    {"text": "Что такое электрический ток?", "category": question_categories["Наука"]},
    {"text": "Кто написал 'Войну и мир'?", "category": question_categories["История"]},
    {"text": "Какая планета ближе всего к Солнцу?", "category": question_categories["Наука"]}
]

session.add_all([Question(**question) for question in questions_data])
session.commit()

# Задача 2: Чтение данных
categories = session.query(Category).all()
for category in categories:
    print(f"Категория: {category.name} ({category.description})")
    for product in category.products:
        print(f"  - {product.name}: {product.price} USD")

# Вывод категорий вопросов и их вопросов
question_categories = session.query(QuestionCategory).all()
for q_cat in question_categories:
    print(f"Категория вопросов: {q_cat.name}")
    for question in q_cat.questions:
        print(f"  - {question.text}")

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
