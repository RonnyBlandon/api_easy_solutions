from pydantic import BaseModel, UUID4
from typing import Optional
from user_schemas import UserReadSchema

# Esquema base para Driver (común entre lectura y escritura)
class DriverBaseSchema(BaseModel):
    vehicle_type: str
    license_number: str
    is_available: Optional[bool] = True

# Esquema para crear un Driver
class DriverCreateSchema(DriverBaseSchema):
    pass

# Esquema para leer un Driver (incluye relación con el usuario)
class DriverReadSchema(DriverBaseSchema):
    id: UUID4
    user: UserReadSchema

    class Config:
        from_attributes = True