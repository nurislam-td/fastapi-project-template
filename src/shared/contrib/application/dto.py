from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class DTO:
    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
