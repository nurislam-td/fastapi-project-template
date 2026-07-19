from typing import Any, Protocol

from shared.auth.application.dto.jwt import JwtPairDTO, UserPayload


class IJwtEncoder(Protocol):
    def create_pair(self, payload: dict[str, Any]) -> JwtPairDTO: ...
    def create_user_tokens(self, payload: UserPayload) -> JwtPairDTO: ...


class IJwtDecoder(Protocol):
    def decode_refresh(self, refresh_token: str) -> dict[str, Any]: ...
    def decode_access(self, access_token: str) -> dict[str, Any]: ...


class IJwtRepo(Protocol):
    async def get_by_user_id(self, user_id: int) -> JwtPairDTO: ...
