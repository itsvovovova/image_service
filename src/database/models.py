from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

# Создаем базовый класс
class Base(DeclarativeBase):
    pass


# Создаем модель, объекты которого будут в бд
class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    user_token: Mapped[str]
    photo: Mapped[bytes]
    filter: Mapped[str]
    result: Mapped[bytes]
    status: Mapped[str]

# Аналогично, пароль тут хэшированный
class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(primary_key=True, index=True)
    password: Mapped[str]