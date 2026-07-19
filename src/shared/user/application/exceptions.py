from dataclasses import dataclass, field
from typing import ClassVar, Literal

from contrib.application.exceptions import AppError


@dataclass(frozen=True, eq=False, slots=True)
class UserNotExistsError(AppError):
    reason_code: ClassVar[Literal["USER_NOT_EXISTS"]] = "USER_NOT_EXISTS"
    email: str | None = field(default=None)
    id: int | None = field(default=None)

    @property
    def message(self):
        not_exists_msg = ""
        if self.email:
            not_exists_msg = f"with that email {self.email}"
        if self.id:
            not_exists_msg = f"with that id {self.id}"
        return f"User {not_exists_msg} not exists"


@dataclass(frozen=True, eq=False, slots=True)
class UserAlreadyExistsError(AppError):
    reason_code: ClassVar[Literal["USER_ALREADY_EXISTS"]] = "USER_ALREADY_EXISTS"
    email: str | None = field(default=None)
    id: int | None = field(default=None)

    @property
    def message(self):
        not_exists_msg = ""
        if self.email:
            not_exists_msg = f"with that email {self.email}"
        if self.id:
            not_exists_msg = f"with that id {self.id}"
        return f"User {not_exists_msg} already exists"


@dataclass(frozen=True, eq=False, slots=True)
class IncorrectPasswordError(AppError):
    reason_code: ClassVar[Literal["INCORRECT_PASSWORD"]] = "INCORRECT_PASSWORD"

    @property
    def message(self):
        return "Incorrect password"
