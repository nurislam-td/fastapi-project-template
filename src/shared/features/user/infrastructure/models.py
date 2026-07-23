from sqlalchemy.orm import Mapped, mapped_column

from shared.contrib.infrastructure.models import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[bytes]
    first_name: Mapped[str]
    last_name: Mapped[str]
    gender: Mapped[str]
    age: Mapped[int | None] = mapped_column(default=None)
