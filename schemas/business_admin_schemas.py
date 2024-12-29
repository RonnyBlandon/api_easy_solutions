from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional

# Esquemas de BusinessAdmin
class BusinessAdminBase(BaseModel):
    business_name: str
    logo_image: Optional[HttpUrl] = None  # Logo del negocio administrado

class BusinessAdminResponse(BusinessAdminBase):
    id: UUID4
    user_id: UUID4

    class Config:
        from_attributes = True