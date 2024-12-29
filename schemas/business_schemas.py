from pydantic import BaseModel, EmailStr, UUID4
from typing import List, Optional


# Esquema para BusinessImage
class BusinessImageBase(BaseModel):
    image_url: str
    image_type: Optional[str]


class BusinessImageCreate(BusinessImageBase):
    business_id: UUID4


class BusinessImageResponse(BusinessImageBase):
    id: UUID4

    class Config:
        from_attributes = True


# Esquema para TypeBusiness
class TypeBusinessBase(BaseModel):
    name: str


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
    external_id: UUID4
    business_name: str
    category_id: int
    department_id: Optional[int]
    municipality_id: Optional[int]
    country: str
    description: Optional[str]
    email: EmailStr
    lat: Optional[float]
    long: Optional[float]
    phone_number: Optional[str]
    zip_code: Optional[str]
    status: Optional[str]
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
    images: List[BusinessImageResponse] = []

    class Config:
        from_attributes = True
