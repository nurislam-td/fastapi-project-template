from pydantic import BaseModel, EmailStr, Field

from shared.auth.application.dto.user import Gender


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(examples=["String03@"])


class SignUpSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(examples=["String03@"])
    gender: Gender
    age: int | None = None
