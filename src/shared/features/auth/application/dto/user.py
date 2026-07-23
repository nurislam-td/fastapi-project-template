from dataclasses import dataclass
from enum import StrEnum, auto

from shared.contrib.application.dto import DTO


class Gender(StrEnum):
    MALE = auto()
    FEMALE = auto()
    OTHER = auto()


@dataclass(slots=True, frozen=True)
class SignUpDTO(DTO):
    email: str
    password: str
    first_name: str
    last_name: str
    gender: Gender
    age: int | None = None
