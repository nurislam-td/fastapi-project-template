from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from shared.settings import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.ENV == "local",
)
sessionmaker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)
