from typing import Protocol


class IPasswordService(Protocol):
    @staticmethod
    def encrypt_pwd(input_pwd: str) -> bytes: ...
    @staticmethod
    def check_pwd(input_pwd: str, db_pwd: bytes) -> bool: ...
