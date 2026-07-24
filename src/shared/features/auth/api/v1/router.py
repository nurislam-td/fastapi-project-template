from diwire import Injected, Scope, resolver_context
from fastapi import APIRouter

from shared.features.auth.api.v1.schemas import LoginSchema, SignUpSchema
from shared.features.auth.application.dto.jwt import JwtPairDTO
from shared.features.auth.application.dto.user import SignUpDTO
from shared.features.auth.application.use_cases.login import LoginHandler
from shared.features.auth.application.use_cases.signup import SignUpHandler

router = APIRouter()


@router.post("/login")
@resolver_context.inject(scope=Scope.REQUEST)
async def login(login: LoginSchema, handler: Injected[LoginHandler]) -> JwtPairDTO:
    return await handler.call(email=login.email, password=login.password)


@router.post("/signup", status_code=201)
@resolver_context.inject(scope=Scope.REQUEST)
async def signup(signup: SignUpSchema, handler: Injected[SignUpHandler]) -> JwtPairDTO:
    dto = SignUpDTO(**signup.model_dump())
    return await handler.call(dto)
