from pydantic import BaseModel
from typing import List, Optional
from database.models.address_model import EntityTypeEnum

# Esquemas de departamento
class DepartmentCreateSchema(BaseModel):
    name: str

class DepartmentUpdateSchema(BaseModel):
    name: Optional[str] = None

class DepartmentResponseSchema(BaseModel):
    id: int
    name: str
    municipalities: List["MunicipalityResponseSchema"] = []

    class Config:
        from_attributes = True

# Esquemas de municipalidad
class MunicipalityCreateSchema(BaseModel):
    name: str
    department_id: int

class MunicipalityUpdateSchema(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None

class MunicipalityResponseSchema(BaseModel):
    id: int
    name: str
    department_id: int

    class Config:
        from_attributes = True

# Esquemas de address
class AddressBaseSchema(BaseModel):
    alias: str
    address: str
    reference: str
    sector: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_main_address: bool = False
    municipality_id: int

# Esquema para creación
class AddressCreateSchema(AddressBaseSchema):
    pass

# Esquema para actualización
class AddressUpdateSchema(BaseModel):
    id: int
    alias: Optional[str] = None
    address: Optional[str] = None
    reference: Optional[str] = None
    sector: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_main_address: Optional[bool] = False
    municipality_id: Optional[int] = None

# Esquema para respuesta
class AddressResponseSchema(AddressBaseSchema):
    id: int
    municipality: MunicipalityResponseSchema

    class Config:
        from_attributes = True

class AddressListResponseSchema(BaseModel):
    address_list: List[AddressResponseSchema]