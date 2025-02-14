from __future__ import annotations  # Importar para Forward References
from decimal import Decimal
from pydantic import BaseModel, UUID4
from typing import Optional, List

from schemas.business_schemas import BusinessResponse

# Esquema para Categorias
class CategoryBase(BaseModel):
    name: str
    business_id: UUID4

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    products: List["ProductResponse"] = []  # Forward Reference corregido

    class Config:
        from_attributes = True

class BusinessWithCategoriesResponse(BaseModel):
    business: BusinessResponse
    business_categories: List[CategoryResponse]


# Esquema para Extra
class ExtraBase(BaseModel):
    title: str
    price: Decimal
    option_id: int

class ExtraCreate(ExtraBase):
    pass

class ExtraUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[Decimal] = None

class ExtraResponse(ExtraBase):
    id: int

    class Config:
        from_attributes = True


# Esquema para Option
class OptionBase(BaseModel):
    title: str
    max_extras: int
    is_required: bool = False
    product_id: UUID4

class OptionCreate(OptionBase):
    pass

class OptionUpdate(BaseModel):
    title: Optional[str] = None
    max_extras: Optional[int] = None
    is_required: Optional[bool] = None

class OptionResponse(OptionBase):
    id: int
    extras: List[ExtraResponse] = []

    class Config:
        from_attributes = True


# Esquema para Productos
class ProductBase(BaseModel):
    name: str
    price: Decimal
    description: Optional[str] = None
    product_image_url: str
    stock: int = 0
    available: bool
    business_id: UUID4
    discount: Decimal
    is_active: bool

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    product_image_url: Optional[str] = None
    stock: Optional[int] = None
    available: bool
    discount: Decimal
    is_active: bool

class ProductResponse(ProductBase):
    id: UUID4
    options: List[OptionResponse] = []

    class Config:
        from_attributes = True
