from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional


# Esquemas de Driver
class DriverBase(BaseModel):
    vehicle_type: str
    license_number: str
    is_available: Optional[bool] = True
    license_image: Optional[HttpUrl] = None  # Imagen de la licencia del conductor

class DriverResponse(DriverBase):
    id: UUID4
    user_id: UUID4

    class Config:
        from_attributes = True