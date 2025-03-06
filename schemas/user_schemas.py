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

# Esquema de respuesta para usuarios
class UserSchemaResponse(UserSchemaBase):
    id: UUID4
    start_date: datetime
    roles: Optional[str] = None

    class Config:
        from_attributes = True

# Esquema base para roles
class RoleSchemaBase(BaseModel):
    name: str

# Esquema para la creación de roles
class RoleSchemaCreate(RoleSchemaBase):
    pass

# Esquema de respuesta para roles
class RoleSchemaResponse(RoleSchemaBase):
    id: int

    class Config:
        from_attributes = True

# Esquema base para la asociación de roles de usuario
class UserRoleAssociationSchemaBase(BaseModel):
    user_id: UUID4
    role_id: int
    assigned_at: Optional[datetime] = None

# Esquema para la creación de la asociación de roles de usuario
class UserRoleAssociationSchemaCreate(UserRoleAssociationSchemaBase):
    pass


# Esquema de respuesta para la asociación de roles de usuario
class UserRoleAssociationSchemaResponse(UserRoleAssociationSchemaBase):
    id: UUID4

    class Config:
        from_attributes = True

# Esquema base para direcciones
class AddressSchemaBase(BaseModel):
    address_type: str
    street_address: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    municipality_id: int

# Esquema para la creación de direcciones
class AddressSchemaCreate(AddressSchemaBase):
    pass

# Esquema para la actualización de direcciones
class AddressSchemaUpdate(BaseModel):
    address_type: Optional[str] = None
    street_address: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    municipality_id: Optional[int] = None

# Esquema de respuesta para direcciones
class AddressSchemaResponse(AddressSchemaBase):
    id: int

    class Config:
        from_attributes = True

# Esquema base para municipios
class MunicipalitySchemaBase(BaseModel):
    name: str
    department_id: int

# Esquema de respuesta para municipios
class MunicipalitySchemaResponse(MunicipalitySchemaBase):
    id: int

    class Config:
        from_attributes = True

# Esquema base para departamentos
class DepartmentSchemaBase(BaseModel):
    name: str

# Esquema de respuesta para departamentos
class DepartmentSchemaResponse(DepartmentSchemaBase):
    id: int

    class Config:
        from_attributes = True