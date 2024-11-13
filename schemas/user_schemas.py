from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional, List
from datetime import datetime
import enum

# Definición del Enum para los roles
class UserRoleEnum(str, enum.Enum):
    USER = "USER"
    DRIVER = "DRIVER"
    BUSINESS_ADMIN = "BUSINESS_ADMIN"

# Esquema base de usuarios (común entre lectura y escritura)
class UserBaseSchema(BaseModel):
    email: EmailStr
    phone_number: str
    full_name: str
    department_id: int
    municipality_id: int
    role: UserRoleEnum
    is_active: Optional[bool] = True

# Esquema para crear usuarios
class UserCreateSchema(UserBaseSchema):
    password: str  # Contraseña sin hash para la creación

# Esquema para leer usuarios (incluye relaciones y datos adicionales)
class UserReadSchema(UserBaseSchema):
    id: UUID4
    department_id: Optional[int]
    municipality_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True  # Habilita la conversión desde objetos ORM

# Esquema base para Department
class DepartmentBaseSchema(BaseModel):
    name: str

# Esquema para crear un Department
class DepartmentCreateSchema(DepartmentBaseSchema):
    pass

# Esquema para leer un Department (incluye usuarios y municipios)
class DepartmentReadSchema(DepartmentBaseSchema):
    id: int
    users: List[UserReadSchema] = []
    municipalities: List['MunicipalityReadSchema'] = []

    class Config:
        from_attributes = True

# Esquema base para Municipality
class MunicipalityBaseSchema(BaseModel):
    name: str
    department_id: int

# Esquema para crear un Municipality
class MunicipalityCreateSchema(MunicipalityBaseSchema):
    pass

# Esquema para leer un Municipality (incluye relaciones con departamentos y usuarios)
class MunicipalityReadSchema(MunicipalityBaseSchema):
    id: int
    department: DepartmentReadSchema
    users: List[UserReadSchema] = []

    class Config:
        from_attributes = True

# Esquema base para Address
class AddressBaseSchema(BaseModel):
    address_type: str
    street_address: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None

# Esquema para crear una Address
class AddressCreateSchema(AddressBaseSchema):
    municipality_id: int

# Esquema para leer una Address (incluye relación con el municipio)
class AddressReadSchema(AddressBaseSchema):
    id: int
    municipality: MunicipalityReadSchema

    class Config:
        from_attributes = True

