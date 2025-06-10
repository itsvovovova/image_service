from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]
    photo: Mapped[bytes]
    filter: Mapped[str]
    result: Mapped[bytes]
    status: Mapped[str]

class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(primary_key=True, index=True)
    password: Mapped[str]