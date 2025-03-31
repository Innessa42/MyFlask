# ========================================================================================
# Base intro
# ========================================================================================

# from pydantic import BaseModel

# DTOs (Data Transfer Object)
# class Address(BaseModel):
#     city: str
#     street: str
#     house_number: int


# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#     is_active: bool
    # address: Address


# address = Address(
#     city=[2, 4, 6],
#     street=222,
#     house_number={2, 3, 45}
# )

# user = User(
#     id=1,
#     name="Dima",
#     age=23,
#     is_active=True,
#     address=address
# )

# ========================================================================================
# Work with JSON
# ========================================================================================
# user_json = '{"id": 1, "name": "David", "age": 23, "is_active": true}'
# user = User.model_validate_json(user_json)
#
# print(user)

# print(user.address.street)

# print(User.name)


# my_var: int
#
# print(my_var)


# '{"name": "Vlad"}' -> {"name": "Vlad"}


# ========================================================================================
# Inheritance with Pydantic
# ========================================================================================

# from pydantic import BaseModel
#
#
# class User(BaseModel):
#     first_name: str
#     last_name: str
#     age: int
#
#
# class Admin(User):
#     salary_rating: float
#
#
# class Moderator(User):
#     phone: str
#
#
# user = User(
#     first_name='Vlad',
#     last_name="Black",
#     age=23
# )
#
# print(user)
#
# admin = Admin(
#     first_name='Jessika',
#     last_name="Black",
#     age=27,
#     salary_rating=2.4,
# )
# print(admin)
#
# moder = Moderator(
#     first_name='Mila',
#     last_name="Green",
#     age=31,
#     phone='+1234567890',
# )
# print(moder)



# ========================================================================================
# Work with `Field` function and additional field validation
# ========================================================================================
# from pydantic import BaseModel, Field
#
#
# class User(BaseModel):
#     first_name: str = Field(
#         min_length=4,
#         max_length=15,
#         description="Name of user"
#     )
#     last_name: str = Field(
#         default="Black",
#         min_length=2,
#         max_length=30,
#     )
#     age: int = Field(
#         gt=0,
#         lt=100
#     )
#
#
# user = User(
#     first_name='John',
#     age=19
# )
#
# print(user)

# ========================================================================================
# Custom Validators && `field_validator` decorator
# ========================================================================================

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
    ValidationError,
    ValidationInfo,
    model_validator
)


# class User(BaseModel):
#     name: str = Field(
#         min_length=4,
#         max_length=15
#     )
#     age: int = Field(
#         gt=0,
#         lt=100
#     )
#     email: EmailStr
#     is_employed: bool

    # @field_validator('is_employed', 'age')
    # @classmethod
    # def check_is_employed(cls, values):
    #     ...
    #
    #     if <is_employed>:
    #         ...
    #     if <age>:
    #         ...
    #
    #     if <is_employed> to <age>:
    #         ...
    #
    #     return values


#     @field_validator('email')
#     @classmethod
#     def check_email_domain(cls, value: str) -> str: # value="test.email@gmail.com"
#         allowed_domains = {"gmail.com",}
#         raw_domain = value.split('@')[-1]
#
#         if raw_domain not in allowed_domains:
#             raise ValueError(f"Email must be from one of the following domains: {', '.join(allowed_domains)}")
#
#         return value
#
#
#
# json_user = """{"name": "Andre","age": 17,"email": "a.21@gmail.com"}"""
#
# user = User.model_validate_json(json_user)
#
# print(user.model_dump_json(indent=4))


# json_data = [
#     """{"name": "Andre","age": 21,"email": "a.21@gmail.com"}""",
#     """{"name": "Andre","age": 22,"email": "a.22@gmail.com"}""",
#     """{"name": "Andre","age": 23,"email": "a.23@gmail.com"}""",
#     """{"name": "Andre","age": 24,"email": "a.24@test.com"}""",
#     """{"name": "Andre","age": 25,"email": "a.25@gmail.com"}""",
#     """{"name": "Andre","age": 25,"email": "a.25@test.com"}"""
# ]
#
# for us in json_data:
#     try:
#         user = User.model_validate_json(us)
#         print(user)
#     except ValidationError as err:
#         print(err)
#
#
# print("WE ARE IN THE SYSTEM!!!")


# ========================================================================================
# Custom Validators && `field_validator` decorator
# ========================================================================================
# from pydantic import BaseModel, Field, model_validator, ValidationError, EmailStr
# from typing import Union


# class User(BaseModel):
#     user_name: str = Field(min_length=4)
#     email: EmailStr
#     password: str = Field(min_length=9)


    # @model_validator(mode='before')
    # @classmethod
    # def check_raw_data(cls, data: dict[str, str]) -> dict[str, str]:
    #     repeat_password = data.pop('repeat_password')
    #     password = data.get('password')
    #
    #     if password != repeat_password:
    #         raise ValueError("Пароли должны совпадать")
    #
    #     return data

    # @model_validator(mode='after')
    # def additional_validation(self):
    #     if self.user_name == "Vlad":
    #         raise ValueError('...')

    # @model_validator(mode='wrap')
    # def val(cls):
    #     var1
    #     var2
    #     ...
    #     if ...:
    #         ...
    #
    #     User()
    #
    #     if ...:
    #         ...
    #     ...
    #     user.<field> = ...


# json_data = [
#     """{"user_name": "Vlad", "email": "test.email@gmail.com", "password": "as8df7gtsd87fg5sd76fg", "repeat_password": "as8df7gtsd8776fg"}"""
# ]
#
#
# for obj in json_data:
#     try:
#         user = User.model_validate_json(obj)
#         print(user)
#     except ValidationError as err:
#         print(err)


# ========================================================================================
# Field aliases
# ========================================================================================

# from pydantic import BaseModel, Field, AliasChoices
#
#
# class Item(BaseModel):
#     in_stock: bool = Field(
#         validation_alias=AliasChoices(
#             'in_stock',
#             'available',
#             'Is available',
#             'In Stock',
#             'is-available'
#         )
#     )
#     price: float
#
#
# # json_data = '{"name": "Laptop", "available": true}'
# # json_data = '{"name": "Laptop", "in_stock": true}'
#
# json_data = [
#     """{"in_stock": true, "price": 1.1}""",
#     """{"available": false, "price": 1.2}""",
#     """{"Is available": false, "price": 13.3}""",
#     """{"In Stock": false, "price": 14.22}""",
#     """{"is-available": false, "price": 14.22}"""
# ]
#
#
# for obj in json_data:
#     try:
#         item = Item.model_validate_json(obj)
#         print(item)
#     except ValidationError as err:
#         print(err)


# ========================================================================================
# Field aliases
# ========================================================================================

from pydantic import BaseModel, Field, AliasChoices


class Event(BaseModel):
    title: str

    class Config:
       validate_assignment = True
       str_strip_whitespace = True
       str_min_length = 5


event = Event(title="     Summary 1       ")

print(event)
event.title = 'Hi'
print(event)
