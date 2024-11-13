# user_schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

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
    role: Optional[str] = None

# Esquema para los datos del token
class TokenData(BaseModel):
    local_id: str
    role: Optional[str] = None

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