from pydantic import BaseModel, UUID4
from user_schemas import UserReadSchema

# Esquema base para BusinessAdmin (común entre lectura y escritura)
class BusinessAdminBaseSchema(BaseModel):
    business_name: str

# Esquema para crear un BusinessAdmin
class BusinessAdminCreateSchema(BusinessAdminBaseSchema):
    pass

# Esquema para leer un BusinessAdmin (incluye relación con el usuario)
class BusinessAdminReadSchema(BusinessAdminBaseSchema):
    id: UUID4
    user: UserReadSchema

    class Config:
        from_attributes = True