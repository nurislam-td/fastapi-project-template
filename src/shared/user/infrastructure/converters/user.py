from shared.user.application.dto.user import Gender, UserDTO
from shared.user.infrastructure.models import User


def user_converter(user: User) -> UserDTO:
    return UserDTO(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=Gender(user.gender),
        age=user.age,
        password=user.password,
    )
