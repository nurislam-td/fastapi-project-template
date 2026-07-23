from dataclasses import dataclass

from shared.features.auth.application.converters.auth_user import create_user_converter
from shared.features.auth.application.dto.jwt import JwtPairDTO, UserPayload
from shared.features.auth.application.dto.user import SignUpDTO
from shared.features.auth.application.exceptions import UserAlreadyExistsError
from shared.features.auth.application.ports.jwt import IJwtEncoder
from shared.features.auth.application.ports.password import IPasswordService
from shared.contrib.application.use_case import IHandler, IUnitOfWork
from shared.features.user.application.ports.repo import IUserRepo


@dataclass(frozen=True, slots=True)
class SignUpHandler(IHandler):
    user_service: IUserRepo
    jwt_service: IJwtEncoder
    pwd: IPasswordService
    uow: IUnitOfWork

    async def call(self, create_user: SignUpDTO) -> JwtPairDTO:
        if await self.user_service.check_user_email_exists(email=create_user.email):
            raise UserAlreadyExistsError(email=create_user.email)
        user_id = await self.user_service.create_user(
            create_user_converter(create_user, self.pwd)
        )
        pair = self.jwt_service.create_user_tokens(UserPayload(user_id=user_id))
        await self.uow.commit()
        return pair
