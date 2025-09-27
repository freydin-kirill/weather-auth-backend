import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class Token(BaseModel):
    """Response schema with access token."""

    access_token: str
    token_type: str


class SUserRead(BaseModel):
    """Base schema for reading user data."""

    email: EmailStr = Field(max_length=50, description="User's email address")
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="User's first name",
    )
    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="User's last name",
    )
    phone_number: str | None = Field(
        default=None,
        min_length=1,
        max_length=15,
        description="User's phone number in the format '+1234567890'",
    )


class SUserRegister(SUserRead):
    """Schema for user registration."""

    password: str = Field(min_length=8, max_length=50, description="User's password")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str | None) -> str | None:
        """Validate phone number format."""

        if value is None:
            return None
        if not re.match(r"^\+\d{1,15}$", value):
            raise ValueError("Incorrect phone number format")
        return value
