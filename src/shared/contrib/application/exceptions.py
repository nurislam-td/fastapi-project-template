from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True, eq=False)
class AppError(Exception):
    reason_code: ClassVar[str] = "UNKNOWN_REASON"  # code name for error

    @property
    def message(self) -> str:  # field for presentation
        return "AppError"
