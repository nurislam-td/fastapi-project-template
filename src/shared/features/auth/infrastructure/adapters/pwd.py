import bcrypt

from shared.features.auth.application.ports.password import IPasswordService


class PasswordService(IPasswordService):
    @staticmethod
    def encrypt_pwd(input_pwd: str) -> bytes:
        return bcrypt.hashpw(
            input_pwd.encode("utf-8"),
            bcrypt.gensalt(),
        )

    @staticmethod
    def check_pwd(input_pwd: str, db_pwd: bytes) -> bool:
        return bcrypt.checkpw(input_pwd.encode("utf-8"), db_pwd)
