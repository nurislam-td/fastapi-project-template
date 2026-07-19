from typing import Any, Protocol


class IUnitOfWork(Protocol):
    async def commit(self) -> None: ...


class IHandler(Protocol):
    uow: IUnitOfWork

    async def call(self, *args, **kwargs) -> Any: ...
