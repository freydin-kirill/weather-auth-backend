import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class SUserAuth(BaseModel):
    email: EmailStr = Field(max_length=50, description="User's email address")
    password: str = Field(min_length=8, max_length=50, description="User's password")


class SUserRegister(BaseModel):
    email: EmailStr = Field(max_length=50, description="User's email address")
    password: str = Field(min_length=8, max_length=50, description="User's password")
    first_name: str | None = Field(
        default=None, min_length=1, max_length=50, description="User's first name"
    )
    last_name: str | None = Field(
        default=None, min_length=1, max_length=50, description="User's last name"
    )
    phone_number: str | None = Field(
        default=None, min_length=1, max_length=15, description="User's phone number in the format '+1234567890'"
    )

    @classmethod
    @field_validator("phone_number")
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{1,15}$', values):
            raise ValueError("Phone number must start with '+' and contain digits")
        return values

