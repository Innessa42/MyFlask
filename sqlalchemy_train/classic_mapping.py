from sqlalchemy import (
    create_engine,
    Table, Column, String, Text, Numeric
)
from sqlalchemy.orm import declarative_base, registry

Base = declarative_base()

sqla_engine = create_engine(
    url="sqlite:///../example.db",
    echo=True,
    echo_pool=True,
)

# Classic mapping style

Register = registry()
metadata = Register.metadata

news_table = Table(
    'news',
    metadata,
    Column('title', String(50), unique=True),
    Column('description', Text, nullable=True),
    Column('rating', Numeric(3, 2)),
)


class News:
    def __init__(self, title: str, description: str, rating: float) -> None:
        self.title = title
        self.description = description
        self.rating = rating


Register.map_imperatively(News, news_table)
Register.metadata.create_all(bind=sqla_engine)

# metadata: {
#     "tables": (table1(id(BigInteger, ...)), table2(), ..., table15),
#     "conn_type": ...,
#     "conn_engine": "...",
# }
