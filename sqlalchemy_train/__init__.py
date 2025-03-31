__all__ = (
    "engine",
    "Base"
)


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


engine = create_engine(
    # url="sqlite:///../relations.db"
    url="sqlite:///:memory:"
)

Base = declarative_base()
