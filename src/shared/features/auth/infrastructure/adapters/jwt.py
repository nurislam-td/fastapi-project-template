from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import jwt

from shared.features.auth.application.dto.jwt import JwtPairDTO, UserPayload
from shared.features.auth.application.ports.jwt import IJwtDecoder, IJwtEncoder


@dataclass(slots=True, eq=False, repr=False)
class JwtService(IJwtEncoder, IJwtDecoder):
    jwt_alg: str
    access_private_path: Path
    access_public_path: Path
    access_token_expire: int
    refresh_private_path: Path
    refresh_public_path: Path
    refresh_token_expire: int

    def _encode_jwt(
        self,
        payload: dict[str, Any],
        expire_seconds: int,
        key: str,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(tz=UTC)
        expire = now + timedelta(seconds=expire_seconds)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        return jwt.encode(payload=to_encode, key=key, algorithm=self.jwt_alg)

    def _decode_jwt(self, token: str, key: str) -> dict[str, Any]:
        return jwt.decode(jwt=token, key=key, algorithms=[self.jwt_alg])

    def create_pair(self, payload: dict[str, Any]) -> JwtPairDTO:
        access_token = self._encode_jwt(
            payload=payload,
            expire_seconds=self.access_token_expire,
            key=self.access_private_path.read_text(),
        )
        refresh_token = self._encode_jwt(
            payload=payload,
            expire_seconds=self.refresh_token_expire,
            key=self.refresh_private_path.read_text(),
        )
        return JwtPairDTO(access_token, refresh_token)

    def decode_refresh(self, refresh_token: str) -> dict[str, Any]:
        return self._decode_jwt(
            token=refresh_token,
            key=self.refresh_public_path.read_text(),
        )

    def decode_access(self, access_token: str) -> dict[str, Any]:
        return self._decode_jwt(
            token=access_token,
            key=self.access_public_path.read_text(),
        )

    def create_user_tokens(self, payload: UserPayload) -> JwtPairDTO:
        payload_dict = payload.as_dict()
        payload_dict = {**payload_dict, "user_id": str(payload.user_id)}
        return self.create_pair(payload_dict)
