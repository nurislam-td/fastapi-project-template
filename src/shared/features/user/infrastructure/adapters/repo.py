from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.features.user.application.dto.user import CreateUserDTO, UserDTO
from shared.features.user.application.exceptions import UserNotExistsError
from shared.features.user.application.ports.repo import IUserRepo
from shared.features.user.infrastructure.converters.user import user_converter
from shared.features.user.infrastructure.models import User


@dataclass(slots=True, eq=False, repr=False)
class UserRepo(IUserRepo):
    session: AsyncSession

    async def get_user_by_email(self, email: str) -> UserDTO:
        q = select(User).where(User.email == email)
        u = (await self.session.execute(q)).scalar_one_or_none()
        if u is None:
            raise UserNotExistsError(email=email)
        return user_converter(u)

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        q = select(User).where(User.id == user_id)
        u = (await self.session.execute(q)).scalar_one()
        return user_converter(u)

    async def get_maybe_user_by_id(self, user_id: int) -> UserDTO | None:
        q = select(User).where(User.id == user_id)
        u = (await self.session.execute(q)).scalar_one_or_none()
        return user_converter(u) if u else u

    async def check_user_email_exists(self, email: str) -> bool:
        q = select(User.id).where(User.email == email)
        u = await self.session.scalar(q)
        return u is not None

    async def create_user(self, user: CreateUserDTO) -> UUID:
        u = User(
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            gender=user.gender,
            age=user.age,
        )
        self.session.add(u)
        await self.session.flush()
        return u.id
