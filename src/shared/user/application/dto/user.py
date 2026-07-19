from dataclasses import dataclass
from enum import StrEnum, auto
from uuid import UUID

from shared.contrib.application.dto import DTO


class Gender(StrEnum):
    MALE = auto()
    FEMALE = auto()
    OTHER = auto()


@dataclass(slots=True, frozen=True)
class UserDTO(DTO):
    id: UUID
    email: str
    password: bytes
    first_name: str
    last_name: str
    gender: Gender
    age: int | None = None


@dataclass(slots=True, frozen=True)
class CreateUserDTO(DTO):
    email: str
    password: bytes
    first_name: str
    last_name: str
    gender: Gender
    age: int | None = None
