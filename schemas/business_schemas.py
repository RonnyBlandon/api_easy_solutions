from pydantic import BaseModel, EmailStr, UUID4
from typing import List, Optional


# Esquema para BusinessImage
class BusinessImageBase(BaseModel):
    image_url: str
    image_type: Optional[str]


class BusinessImageCreate(BusinessImageBase):
    business_id: UUID4


class BusinessImageResponse(BusinessImageBase):
    id: int

    class Config:
        from_attributes = True


# Esquema para TypeBusiness
class TypeBusinessBase(BaseModel):
    name: str
    image_url: str


class TypeBusinessCreate(TypeBusinessBase):
    pass


class TypeBusinessResponse(TypeBusinessBase):
    id: int

    class Config:
        from_attributes = True


# Esquema para Business
class BusinessBase(BaseModel):
    address: str
    admin_id: UUID4
    business_name: str
    municipality_id: Optional[int]
    country: str
    description: Optional[str]
    email: EmailStr
    lat: Optional[float]
    long: Optional[float]
    phone_number: Optional[str]
    zip_code: Optional[str]
    is_active: bool
    is_popular_this_week: bool
    is_novelty: bool
    has_free_delivery: bool
    has_alcohol: bool
    is_open_now: bool
    average_price: Optional[float]
    average_delivery: Optional[str]


class BusinessCreate(BusinessBase):
    type_business_id: int


class BusinessResponse(BusinessBase):
    id: UUID4
    type_business: Optional[TypeBusinessResponse]
    business_images: List[BusinessImageResponse] = []

    class Config:
        from_attributes = True
