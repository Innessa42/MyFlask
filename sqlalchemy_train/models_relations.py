from sqlalchemy import (
    BigInteger,
    String,
    ForeignKey,
)

from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
)

from sqlalchemy_train import engine, Base


# O2M
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(20)
    )
    surname: Mapped[str] = mapped_column(
        String(25),
        default="No Surname", # на стороне ORM
        server_default="No Surname"
    )

    addresses: Mapped['Address'] = relationship( # [<obj1, obj2>, ..., obj33]
        'Address',
        back_populates='user'
    )
    profile: Mapped['Profile'] = relationship( # <obj>
        "Profile",
        back_populates="user",
        uselist=False
    )
    project_associations: Mapped['ProjectsToUsers'] = relationship("ProjectsToUsers", back_populates="user")


class ProjectsToUsers(Base):
    __tablename__ = "users_to_projects"
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id'),
        primary_key=True
    )
    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('project.id'),
        primary_key=True
    )

    user: Mapped['User'] = relationship("User", back_populates="project_associations")
    project: Mapped['Project'] = relationship("Project", back_populates="user_associations")


# M2M
class Project(Base):
    __tablename__ = 'project'
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(40)
    )

    user_associations: Mapped['ProjectsToUsers'] = relationship("ProjectsToUsers", back_populates="project")


class Address(Base):
    __tablename__ = 'address'
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    city: Mapped[str] = mapped_column(
        String(20)
    )
    country: Mapped[str] = mapped_column(
        String(30),
        unique=True
    )
    street: Mapped[str] = mapped_column(
        String(40)
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id')
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='addresses'
    )


# O2O
class Profile(Base):
    __tablename__ = 'profile'
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(75),
        unique=True,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id'),
        unique=True
    )

    user: Mapped['User'] = relationship(
        "User",
        back_populates="profile"
    )


Base.metadata.create_all(bind=engine)
