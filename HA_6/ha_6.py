from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

# Создание FastAPI-приложения
app = FastAPI()

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


# Pydantic-схемы
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class QuestionCategoryBase(BaseModel):
    name: str


class QuestionCategoryResponse(QuestionCategoryBase):
    id: int

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    text: str
    category_id: int


class QuestionResponse(QuestionBase):
    id: int
    category: QuestionCategoryResponse

    class Config:
        orm_mode = True


# API-эндпоинты для категорий вопросов
@app.post("/categories", response_model=QuestionCategoryResponse)
def create_category(category: QuestionCategoryBase):
    db_category = QuestionCategory(**category.dict())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@app.get("/categories", response_model=List[QuestionCategoryResponse])
def get_categories():
    return session.query(QuestionCategory).all()


@app.put("/categories/{id}", response_model=QuestionCategoryResponse)
def update_category(id: int, category: QuestionCategoryBase):
    db_category = session.query(QuestionCategory).filter(QuestionCategory.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    session.commit()
    session.refresh(db_category)
    return db_category


@app.delete("/categories/{id}")
def delete_category(id: int):
    db_category = session.query(QuestionCategory).filter(QuestionCategory.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(db_category)
    session.commit()
    return {"message": "Category deleted"}


# API-эндпоинты для вопросов
@app.get("/questions", response_model=List[QuestionResponse])
def get_questions():
    return session.query(Question).all()


@app.post("/questions", response_model=QuestionResponse)
def create_question(question: QuestionBase):
    category = session.query(QuestionCategory).filter(QuestionCategory.id == question.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category ID")
    db_question = Question(**question.dict())
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question
