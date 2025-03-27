from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional, List
from datetime import datetime


# Esquema base para usuario
class UserSchemaBase(BaseModel):
    email: EmailStr
    phone_number: str
    full_name: str
    municipality_id: Optional[int] = None
    is_active: Optional[bool] = True

# Esquema para la creación de usuarios
class UserSchemaCreate(UserSchemaBase):
    password: str

# Esquema para la actualización de usuarios
class UserSchemaUpdate(BaseModel):
    phone_number: Optional[str] = None
    full_name: Optional[str] = None
    hashed_password: Optional[str] = None
    municipality_id: Optional[int] = None
    providers: Optional[List[str]] = None

# Esquema de respuesta para usuarios
class UserSchemaResponse(UserSchemaBase):
    id: UUID4
    start_date: datetime
    providers: List[str]
    roles: List[str]

    class Config:
        from_attributes = True
