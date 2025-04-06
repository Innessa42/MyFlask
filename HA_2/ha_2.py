#Python Advanced: Домашнее задание 2
#Разработать систему регистрации пользователя, используя Pydantic для валидации
# входных данных, обработки вложенных структур и сериализации. Система должна
# обрабатывать данные в формате JSON.
#Задачи:
#Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
#Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic,
# валидирует данные, и в случае успеха сериализует объект обратно в JSON и возвращает его.
#Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
#Написать несколько примеров JSON строк для проверки различных сценариев валидации:
# успешные регистрации и случаи, когда валидация не проходит (например возраст
# не соответствует статусу занятости).

#Модели:
#Address: Должен содержать следующие поля:
#city: строка, минимум 2 символа.
#street: строка, минимум 3 символа.
#house_number: число, должно быть положительным.
#User: Должен содержать следующие поля:
#name: строка, должна быть только из букв, минимум 2 символа.
#age: число, должно быть между 0 и 120.
#email: строка, должна соответствовать формату email.
#is_employed: булево значение, статус занятости пользователя.
#address: вложенная модель адреса.
#Валидация:
#Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65 лет.
#
#
## Пример JSON данных для регистрации пользователя
#
#json_input = """{
#
#    "name": "John Doe",
#
#    "age": 70,
#
#    "email": "john.doe@example.com",
#
#    "is_employed": true,
#
#    "address": {
#
#        "city": "New York",
#
#        "street": "5th Avenue",
#
#        "house_number": 123
#
#    }
#
#}"""

from pydantic import BaseModel, EmailStr, Field, ValidationError, validator, field_validator
import json

class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)

class User(BaseModel):
    name: str = Field(..., min_length=2, pattern=r'^[A-Za-z\s]+$')
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("is_employed")
    @classmethod
    def check_employment(cls, is_employed, values):
        age = values.data.get("age")
        if is_employed and (age is None or age < 18 or age > 65):
            raise ValueError("Employed users must be between 18 and 65 years old.")
        return is_employed

def process_user_registration(json_string: str):
    try:
        user = User.model_validate_json(json_string)
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        return json.dumps({"errors": [err["msg"] for err in e.errors()]}, indent=4)


valid_json = '''{
    "name": "klaudi Lopez",
    "age": 30,
    "email": "klaudi.lopez@example.com",
    "is_employed": true,
    "address": {
        "city": "London",
        "street": "Baker Street",
        "house_number": 221
    }
}'''

invalid_json = '''{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}'''

print("Valid Input Test:")
print(process_user_registration(valid_json))
print("\nInvalid Input Test:")
print(process_user_registration(invalid_json))