from collections.abc import AsyncGenerator

from diwire import Container, Lifetime, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from setup.db.session import sessionmaker
from shared.auth.application.ports.jwt import IJwtEncoder
from shared.auth.infrastructure.adapters.jwt import JwtService
from shared.contrib.application.use_case import IUnitOfWork
from shared.contrib.utils.logger import get_logger
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


def provide_jwt_service() -> IJwtEncoder:
    return JwtService()


container = Container()


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
container.add(
    JwtService,
    provides=IJwtEncoder,
    scope=Scope.REQUEST,
    lifetime=Lifetime.SCOPED,
)
container.compile()
