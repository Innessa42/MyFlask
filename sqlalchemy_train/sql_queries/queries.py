from typing import Type, Any
import json

from sqlalchemy import func, and_, or_, not_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, DataError

from sqlalchemy_train.sql_queries.models import User, Role, Comment, News
from sqlalchemy_train.sql_queries.db_connection import DBConnection
from sqlalchemy_train.sql_queries import engine


def create_new_role(session: Session, data: dict[str, str]) -> Role:
    try:
        role = Role(**data) # Role(name="NEW ROLE")
        session.add(role)
        session.commit() # Role(name="new role")
        session.refresh(role)

        return role
    except (IntegrityError, DataError) as err:
        session.rollback()
        raise err


def create_user(session: Session, data: dict[str, Any]) -> User:
    try:
        user = User(**data)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
    except (IntegrityError, DataError) as err:
        session.rollback()
        raise err


def get_all_roles(session: Session) -> list[Type[Role]] | None:
    all_roles = session.query(Role).all() # SELECT * FROM Role;
    # all_roles = session.query(Role.name) # SELECT role.name FROM Role;

    if all_roles:
        return all_roles


def get_users_by_rating(session: Session, req_rating: float) -> list[User]:
    users = session.query(User).filter(User.rating >= req_rating).all()

    return users


with DBConnection(engine) as session:
    # data = {
    #     "first_name": "John",
    #     "last_name": "Green",
    #     "email": "john.green@gmail.com",
    #     "password": "s8fDg9sd$r8sd$76ftaS%dfg0sD78fg^s68Sd7547As6978",
    #     "phone": "+995 557 873 424",
    #     "role_id": 3
    # }
    #
    # try:
    #     user = create_user(session=session, data=data)
    #     print("User created successfully.")
    #     print(user)
    # except Exception as err:
    #     print(err)

    # ==================================================================
    #
    # ==================================================================
    # role_data = {
    #     "name": "client"
    # }
    #
    # try:
    #     role = create_new_role(session=session, data=role_data)
    #     print("Role was created successfully.")
    #     print(role)
    # except Exception as err:
    #     print(err)

    # ==================================================================
    #
    # ==================================================================

    # GET USERS BY RATING

    # users = get_users_by_rating(session=session, req_rating=4.5)
    #
    # for user in users:
    #     print(user.email, user.rating)

    # ==================================================================
    #
    # ==================================================================

    # users_with_w_in_last_name = session.query(User).filter(
    #     User.last_name.like("W%")
    # ).all()
    #
    # if users_with_w_in_last_name:
    #     for user in users_with_w_in_last_name:
    #         print(user.last_name)

    # ==================================================================
    #
    # ==================================================================

    # BEETWEEN

    # users_with_ranged_rating = session.query(User).filter(
    #     User.rating.between(5, 7)
    # ).all()
    #
    # if users_with_ranged_rating:
    #     for user in users_with_ranged_rating:
    #         print(f"{user.email=}  {user.rating=}")

    # ==================================================================
    #
    # ==================================================================

    # IN_ OPERATOR

    # req_names = ("Elizabeth", "Michele", "David")
    # users_in_list_names = session.query(User).filter(
    #     User.first_name.in_(req_names)
    # )
    #
    # if users_in_list_names:
    #     for user in users_in_list_names:
    #         print(f"{user.email=}  {user.first_name=}")

    # ==================================================================
    #
    # ==================================================================

    # NOT_ OPERATOR

    # not_authors = session.query(User).filter(
    #     not_(User.role_id == 3)
    # ).all()
    #
    # if not_authors:
    #     for user in not_authors:
    #         print(f"{user.email=}  {user.role_id=}   {user.rating}")

    # ==================================================================
    #
    # ==================================================================

    # ORDERING

    # not_authors = session.query(User).filter(
    #     User.role_id == 3
    # ).order_by(desc(User.rating), User.created_at).all()
    #
    # if not_authors:
    #     for user in not_authors:
    #         print(f"{user.role_id=}  {user.created_at=}   {user.rating}")


    # ==================================================================
    #
    # ==================================================================

    # AGGREGATION && GROUP

    # moderated_news = session.query(
    #     func.count(News.id)
    # ).filter(News.moderated == 1).scalar()
    #
    # print(f"Count of moderated news = {moderated_news}")

    # news_by_users = session.query(
    #     News.author_id,
    #     func.count(News.id).label("count_of_news")
    # ).group_by(News.author_id).all()
    #
    # if news_by_users:
    #     for news in news_by_users:
    #         print(f"{news.author_id=}  {news.count_of_news=}")

    # ALIASED FOR TABLES

    # us: User = aliased(element=User, name="us")
    #
    # count_of_users = session.query(
    #     us.role_id,
    #     func.count(us.id).label("count_of_users")
    # ).group_by(us.role_id).all()
    #
    # if count_of_users:
    #     for user in count_of_users:
    #         print(f"{user.role_id=}  {user.count_of_users=}")

    # ==================================================================
    #
    # ==================================================================

    # HAVING

    # users_id_with_news_more_than_3 = session.query(
    #     News.author_id,
    #     func.count(News.id).label("count_of_news")
    # ).group_by(News.author_id).having(func.count(News.id) > 4).all()
    #
    # if users_id_with_news_more_than_3:
    #     for news in users_id_with_news_more_than_3:
    #         print(f"{news.author_id=}  {news.count_of_news=}")

    # ==================================================================
    #
    # ==================================================================

    # SUBQUERIES

    # req_role = session.query(
    #     Role.id
    # ).filter(Role.name == "author").scalar_subquery()
    #
    # authors: list[User] = session.query(
    #     User.email,
    #     User.role_id,
    #     User.rating
    # ).filter(
    #     User.role_id == req_role
    # ).all()
    #
    # if authors:
    #     for author in authors:
    #         print(author.email, author.role_id, author.rating)

    # req_role = session.query(
    #     Role.id
    # ).filter(Role.name == "author").scalar_subquery()
    #
    # avg_rating = session.query(
    #     func.avg(User.rating).label("average_rating")
    # ).scalar_subquery()
    #
    # authors: list[User] = session.query(
    #     User.email,
    #     User.role_id,
    #     User.rating
    # ).filter(
    #     User.role_id == req_role,
    #     User.rating > avg_rating
    # ).all()
    #
    # if authors:
    #     for author in authors:
    #         print(author.email, author.role_id, author.rating)

    # ==================================================================
    #
    # ==================================================================

    # JOINS

    # разные подходы к JOIN - загрузке:
    #
    # joinedload() (загрузка через JOIN)
    # subqueryload() (загрузка через подзапросы)
    # selectinload() (загрузка через отдельный SELECT IN)
    # Явный JOIN в запросе с .join()

    # .join() и .outerjoin() явно влияют на состав запроса и фильтрацию данных.

    # Если нужно явно фильтровать данные по связанным объектам или условиям,
    # или если нужно добавить колонки в общий запрос - нужно использовать именно JOIN

    # .join() используется в запросах именно для фильтрации данных.
    # # Не влияет напрямую на то, как объекты связи загружаются (lazy/eager).


    # JOINEDLOAD

    # joinedload() – способ жадной загрузки (eager loading) данных для объектов отношений.
    # НЕ ВЛИЯЕТ на условия выборки, только на то, ЧТО ПОДГРУЗИТСЯ в результирующие объекты.

    # Если нужны данные связных таблиц после выборки - можно юзать joinedload()


    # users_and_news = (
    #     #     session.query(User) # определяется запрос к модели User
    #     #     .options( # для того, чтобы смочь воспользоваться жадной подгрузкой - добавляем опции к запросу
    #     #         joinedload(User.news) # вызываем метод жадной загрузки данных через поле relationship
    #     #     )
    #     #     .all()
    #     # )
    #     #
    #     # json_data = [
    #     #     {
    #     #         "id": user.id,
    #     #         "first_name": user.first_name,
    #     #         "last_name": user.last_name,
    #     #         "email": user.email,
    #     #         "phone": user.phone,
    #     #         "role_id": user.role_id,
    #     #         "deleted": user.deleted,
    #     #         "news": [
    #     #             {
    #     #                 "id": n.id,
    #     #                 "title": n.title,
    #     #                 "moderated": n.moderated,
    #     #                 "created_at": datetime.strftime(n.created_at, "%Y-%m-%d %H:%M:%S"),
    #     #             }
    #     #             for n in user.news
    #     #         ],
    #     #     }
    #     #     for user in users_and_news
    #     # ]
    #     #
    #     # print(json.dumps(json_data, indent=4))

    # users_and_news = (
    #     session.query(User)
    #     .join(User.role)
    #     .filter(Role.name == "author")
    #     .options(
    #         joinedload(User.news).joinedload(News.comments)
    #     )
    #     .all()
    # )
    #
    # json_data = [
    #     {
    #         "id": user.id,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "email": user.email,
    #         "phone": user.phone,
    #         "role_id": user.role_id,
    #         "deleted": user.deleted,
    #         "news": [
    #             {
    #                 "id": n.id,
    #                 "title": n.title,
    #                 "moderated": n.moderated,
    #                 "created_at": datetime.strftime(n.created_at, "%Y-%m-%d %H:%M:%S"),
    #                 "comments": [
    #                     {
    #                         "id": c.id,
    #                         "body": c.body,
    #                         "deleted": c.deleted,
    #                         "created_at": datetime.strftime(c.created_at, "%Y-%m-%d %H:%M:%S")
    #                     }
    #                     for c in n.comments
    #                 ]
    #             }
    #             for n in user.news
    #         ],
    #     }
    #     for user in users_and_news
    # ]
    #
    # print(json.dumps(json_data, indent=4))


    # Получить список авторов, под каждого автора только модерированные новости, под каждую новость все комментарии
    # users_and_news = (
    #     session.query(User)
    #     .join(User.role)
    #     .join(User.news)
    #     .filter(Role.name == "author", News.moderated == 1)
    #     .options(
    #         contains_eager(User.news).joinedload(News.comments)
    #     ).all()
    # )
    #
    # json_data = [
    #     {
    #         "id": user.id,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "email": user.email,
    #         "phone": user.phone,
    #         "role_id": user.role_id,
    #         "deleted": user.deleted,
    #         "news": [
    #             {
    #                 "id": n.id,
    #                 "title": n.title,
    #                 "moderated": n.moderated,
    #                 "created_at": datetime.strftime(n.created_at, "%Y-%m-%d %H:%M:%S"),
    #                 "comments": [
    #                     {
    #                         "id": c.id,
    #                         "body": c.body,
    #                         "deleted": c.deleted,
    #                         "created_at": datetime.strftime(c.created_at, "%Y-%m-%d %H:%M:%S")
    #                     }
    #                     for c in n.comments
    #                 ]
    #             }
    #             for n in user.news
    #         ],
    #     }
    #     for user in users_and_news
    # ]
    #
    # print(json.dumps(json_data, indent=4))

    # ==================================================================
    #
    # ==================================================================

    # ==================================================================
    #
    # ==================================================================

    authors = (
        session.query(User)
        .join(Role, User.role_id == Role.id)
        .filter(Role.name == 'admin')
        .all()
    )

    print(authors)
