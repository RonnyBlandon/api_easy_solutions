from datetime import datetime
from fastapi import Form
# user_schemas.py
from pydantic import UUID4, BaseModel, EmailStr
from typing import Optional, List

#Esquema para signIn de usuarios
class SignInRequest(BaseModel):
    email: EmailStr
    password: str

# Esquema para retornar los tokens de acceso y actualización
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    local_id: str
    roles: List[str]

# Esquema para los datos del token
class TokenData(BaseModel):
    local_id: str
    roles: List[str]

#Esquema para refrescar el access token
class RefreshToken(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class GoogleSignInRequest(BaseModel):
    id_token: str = None
    access_token: str = None

# Esquema de respuesta para inicio de sesion de Google
class GoogleSignInResponse(BaseModel):
    local_id: UUID4
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    start_date: datetime
    access_token: str
    token_type: str = "bearer"
    refresh_token: str
    providers: List[str]
    roles: List[str]