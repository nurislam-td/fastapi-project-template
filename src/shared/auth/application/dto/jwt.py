from dataclasses import dataclass
from uuid import UUID

from shared.contrib.application.dto import DTO


@dataclass(slots=True, frozen=True)
class JwtPairDTO(DTO):
    access_token: str
    refresh_token: str


@dataclass(slots=True, frozen=True)
class UserPayload(DTO):
    user_id: UUID
