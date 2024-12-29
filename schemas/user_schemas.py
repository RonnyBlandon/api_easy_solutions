from pydantic import BaseModel, EmailStr, UUID4, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum
from schemas.business_schemas import BusinessResponse

# Enum para los roles de usuario
class UserRole(str, Enum):
    USER = "USER"
    DRIVER = "DRIVER"
    BUSINESS_ADMIN = "BUSINESS_ADMIN"

# Esquemas de User
class UserBase(BaseModel):
    email: EmailStr
    phone_number: str
    full_name: str
    role: UserRole
    google_user_id: Optional[str] = None
    is_active: Optional[bool] = True
    profile_image: Optional[HttpUrl] = None  # Imagen de perfil del usuario

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID4
    created_at: datetime
    department_id: Optional[int] = None
    municipality_id: Optional[int] = None

    class Config:
        from_attributes = True

# Esquemas de Department
class DepartmentBase(BaseModel):
    name: str

class DepartmentResponse(DepartmentBase):
    id: int
    users: List[UserResponse] = []
    businesses: List["BusinessResponse"] = []
    municipalities: List["MunicipalityResponse"] = []

    class Config:
        from_attributes = True

# Esquemas de Municipality
class MunicipalityBase(BaseModel):
    name: str
    department_id: int

class MunicipalityResponse(MunicipalityBase):
    id: int
    department: DepartmentResponse
    users: List[UserResponse] = []
    addresses: List["AddressResponse"] = []
    businesses: List["BusinessResponse"] = []

    class Config:
        from_attributes = True

# Esquemas de Address
class AddressBase(BaseModel):
    address_type: str
    street_address: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None

class AddressResponse(AddressBase):
    id: int
    municipality_id: int
    municipality: MunicipalityResponse

    class Config:
        from_attributes = True