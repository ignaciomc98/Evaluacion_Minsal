from pydantic import BaseModel, EmailStr, Field, UUID4, field_validator
from typing import List
from datetime import datetime
from .phone import PhoneSchema
import re

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    phones: List[PhoneSchema]

    @field_validator("email", mode="before")
    def validate_email_domain(cls, value):
        allowed_domains = (".cl", ".com", ".org")
        if not any(value.endswith(domain) for domain in allowed_domains):
            raise ValueError("El correo debe ser válido y terminar en uno de los dominios: .cl, .com, .org")
        return value

    @field_validator("password", mode="before")
    def validate_password(cls, value):
        # Regex que exige:
        # - al menos una mayúscula
        # - al menos una minúscula
        # - al menos dos dígitos (en cualquier parte, no necesariamente consecutivos)
        # - mínimo 6 caracteres
        regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=(?:.*\d){2,}).{6,}$"
        if not re.match(regex, value):
            raise ValueError(
                "La contraseña debe contener al menos una mayúscula, "
                "letras minúsculas y dos dígitos."
            )
        return value

    model_config = {
        "from_attributes": True,
        "validate_by_name": True
    }

class UserResponse(UserBase):
    id: UUID4
    created: datetime
    modified: datetime
    last_login: datetime
    token: str
    is_active: bool = Field(..., alias="is_active")
    phones: List[PhoneSchema]

    model_config = {
        "from_attributes": True,
        "validate_by_name": True,
        "populate_by_name": True  # para permitir alias en salida JSON
    }
