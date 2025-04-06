from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import List, Optional

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


# Функции для работы с категориями вопросов
def create_category(name: str):
    category = QuestionCategory(name=name)
    session.add(category)
    session.commit()
    return category


def get_categories():
    return session.query(QuestionCategory).all()


def update_category(category_id: int, new_name: str):
    category = session.query(QuestionCategory).filter(QuestionCategory.id == category_id).first()
    if category:
        category.name = new_name
        session.commit()
    return category


def delete_category(category_id: int):
    category = session.query(QuestionCategory).filter(QuestionCategory.id == category_id).first()
    if category:
        session.delete(category)
        session.commit()
    return category


# Функции для работы с вопросами
def create_question(text: str, category_id: int):
    category = session.query(QuestionCategory).filter(QuestionCategory.id == category_id).first()
    if not category:
        raise ValueError("Invalid category ID")
    question = Question(text=text, category_id=category_id)
    session.add(question)
    session.commit()
    return question


def get_questions():
    return session.query(Question).all()


# Пример работы
if __name__ == "__main__":
    cat1 = create_category("Общие вопросы")
    cat2 = create_category("Технические вопросы")

    print("Созданные категории:", get_categories())

    q1 = create_question("Что такое Python?", cat1.id)
    q2 = create_question("Как работает SQLAlchemy?", cat2.id)

    print("Список вопросов:", get_questions())
