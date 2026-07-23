from shared.features.auth.application.dto.user import SignUpDTO
from shared.features.auth.application.ports.password import IPasswordService
from shared.features.user.application.dto.user import CreateUserDTO as UserCreateUserDTO
from shared.features.user.application.dto.user import Gender as UserGender


def create_user_converter(auth: SignUpDTO, pwd: IPasswordService) -> UserCreateUserDTO:
    return UserCreateUserDTO(
        email=auth.email,
        password=pwd.encrypt_pwd(auth.password),
        first_name=auth.first_name,
        last_name=auth.last_name,
        gender=UserGender(auth.gender.value),
        age=auth.age,
    )
