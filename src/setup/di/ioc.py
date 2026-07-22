from collections.abc import AsyncGenerator

from diwire import Container, Lifetime, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from setup.db.session import sessionmaker
from shared.auth.application.ports.jwt import IJwtEncoder
from shared.auth.application.ports.password import IPasswordService
from shared.auth.infrastructure.adapters.jwt import JwtService
from shared.auth.infrastructure.adapters.pwd import PasswordService
from shared.contrib.application.use_case import IUnitOfWork
from shared.contrib.utils.logger import get_logger
from shared.settings import get_settings
from shared.settings.base import Settings
from shared.user.application.ports.repo import IUserRepo
from shared.user.infrastructure.adapters.repo import UserRepo

logger = get_logger(__name__)


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with sessionmaker() as session:
            yield session
        logger.debug("db session closed")
    finally:
        logger.debug("db session factory closed")


async def provide_uow(session: AsyncSession) -> IUnitOfWork:
    return session


def provide_jwt_service(settings: Settings) -> IJwtEncoder:
    return JwtService(
        access_private_path=settings.ACCESS_PRIVATE_PATH,
        access_public_path=settings.ACCESS_PUBLIC_PATH,
        refresh_private_path=settings.REFRESH_PRIVATE_PATH,
        refresh_public_path=settings.REFRESH_PUBLIC_PATH,
        access_token_expire=settings.ACCESS_TOKEN_EXPIRE,
        refresh_token_expire=settings.REFRESH_TOKEN_EXPIRE,
        jwt_alg=settings.JWT_ALG,
    )


container = Container()


container.add_factory(
    get_settings,
    provides=Settings,
    scope=Scope.APP,
    lifetime=Lifetime.SCOPED,
)
container.add_generator(
    provide_db_session,
    provides=AsyncSession,
    scope=Scope.REQUEST,
    lifetime=Lifetime.SCOPED,
)
container.add_factory(
    provide_uow,
    provides=IUnitOfWork,
    scope=Scope.REQUEST,
    lifetime=Lifetime.SCOPED,
)

container.add(
    UserRepo,
    provides=IUserRepo,
    scope=Scope.REQUEST,
    lifetime=Lifetime.SCOPED,
)
container.add_factory(
    provide_jwt_service,
    provides=IJwtEncoder,
    scope=Scope.REQUEST,
    lifetime=Lifetime.SCOPED,
)
container.add(PasswordService, provides=IPasswordService)
container.compile()
