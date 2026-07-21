from dataclasses import dataclass

from shared.auth.application.dto.jwt import JwtPairDTO, UserPayload
from shared.auth.application.exceptions import (
    IncorrectPasswordError,
    UserNotAuthenticatedError,
)
from shared.auth.application.ports.jwt import (
    IJwtEncoder,
    IJwtRepo,
)
from shared.auth.application.ports.password import IPasswordService
from shared.contrib.application.use_case import IHandler
from shared.user.application.ports.repo import IUserRepo


@dataclass
class LoginHandler(IHandler):
    user_repo: IUserRepo
    jwt_repo: IJwtRepo
    jwt_encoder: IJwtEncoder
    pwd: IPasswordService

    async def call(self, email: str, password: str) -> JwtPairDTO:
        try:
            user = await self.user_repo.get_user_by_email(email=email)
        except Exception as e:
            raise UserNotAuthenticatedError(email=email) from e

        if not self.pwd.check_pwd(password, user.password):
            raise IncorrectPasswordError()

        return self.jwt_encoder.create_user_tokens(UserPayload(user.id))
