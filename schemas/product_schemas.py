from pydantic import BaseModel, UUID4
from typing import List, Optional


# Esquema para ProductImage
class ProductImageBase(BaseModel):
    image_url: str
    image_type: Optional[str]


class ProductImageCreate(ProductImageBase):
    product_id: UUID4


class ProductImageResponse(ProductImageBase):
    id: UUID4

    class Config:
        from_attributes = True


# Esquema para Category
class CategoryBase(BaseModel):
    name: str
    business_id: UUID4


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# Esquema para Product
class ProductBase(BaseModel):
    product_name: str
    product_price: float
    product_description: Optional[str]
    amount: int


class ProductCreate(ProductBase):
    category_id: int


class ProductResponse(ProductBase):
    id: UUID4
    images: List[ProductImageResponse] = []
    category: Optional[CategoryResponse]
    options: List["OptionResponse"] = []

    class Config:
        from_attributes = True


# Esquema para Option
class OptionBase(BaseModel):
    title: str
    max_extras: int
    is_required: bool


class OptionCreate(OptionBase):
    product_id: UUID4


class OptionResponse(OptionBase):
    id: UUID4
    extras: List["ExtraResponse"] = []

    class Config:
        from_attributes = True


# Esquema para Extra
class ExtraBase(BaseModel):
    title: str
    price: float


class ExtraCreate(ExtraBase):
    option_id: UUID4


class ExtraResponse(ExtraBase):
    id: UUID4

    class Config:
        from_attributes = True
