# from typing import Annotated

# from auth.application.dto.user import UserDTO
# from auth.application.exceptions import UserNotAuthenticatedError
# from fastapi import Depends
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# security = HTTPBearer()


# async def get_current_token(
#     auth: HTTPAuthorizationCredentials = Depends(security),
# ) -> str:
#     token = auth.credentials
#     return token


# async def validate_token(token: Annotated[str, Depends(get_current_token)]) -> UserDTO:
#     ioc = get_ioc()
#     async with ioc(scope=Scope.REQUEST) as di:
#         jwt = await di.get(IJwtService)
#         user_service = await di.get(IUserService)
#         user_id = jwt.decode_access(token).get("user_id", 0)
#         if user := await user_service.get_maybe_user_by_id(user_id):
#             return user
#         raise UserNotAuthenticatedError(id=user_id)
