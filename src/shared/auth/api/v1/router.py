from typing import Any

from fastapi import APIRouter

from shared.auth.api.v1.schemas import LoginSchema, SignUpSchema
from shared.auth.application.dto.jwt import JwtPairDTO
from shared.auth.application.dto.user import SignUpDTO
from shared.auth.application.use_cases.login import LoginHandler
from shared.auth.application.use_cases.signup import SignUpHandler

router = APIRouter()


class Depends[T]:  # it is temporary stub
    async def call(self, *args, **kwargs) -> Any: ...


@router.post("/login")
async def login(login: LoginSchema, handler: Depends[LoginHandler]) -> JwtPairDTO:
    jwt = await handler.call(email=login.email, password=login.password)
    return jwt


@router.post("/signup", status_code=201)
async def signup(signup: SignUpSchema, handler: Depends[SignUpHandler]) -> JwtPairDTO:
    dto = SignUpDTO(**signup.model_dump())
    return await handler.call(dto)
