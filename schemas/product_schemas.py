from pydantic import BaseModel, UUID4
from typing import Optional, List

# Esaquema para imagenes de productos
class ProductImageBase(BaseModel):
    product_id: UUID4
    image_url: str
    image_type: Optional[str] = None

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageUpdate(BaseModel):
    image_url: Optional[str] = None
    image_type: Optional[str] = None

class ProductImageResponse(ProductImageBase):
    id: UUID4

    class Config:
        from_attributes = True

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
    products: List[UUID4] = []

    class Config:
        from_attributes = True


# Esquema para Productos
class ProductBase(BaseModel):
    product_name: str
    product_price: float
    product_description: Optional[str] = None
    stock: int = 0
    available: bool
    business_id: UUID4
    status: bool

class ProductCreate(ProductBase):
    images: Optional[List[ProductImageCreate]]
    pass

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    product_price: Optional[float] = None
    product_description: Optional[str] = None
    stock: Optional[int] = None
    available: bool
    status: bool

class ProductResponse(ProductBase):
    id: UUID4
    options: List[UUID4] = []
    images: List[UUID4] = []
    categories: List[int] = []

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
    id: UUID4
    extras: List[UUID4] = []

    class Config:
        from_attributes = True


# Esquema para Extra
class ExtraBase(BaseModel):
    title: str
    price: float
    option_id: UUID4

class ExtraCreate(ExtraBase):
    pass

class ExtraUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None

class ExtraResponse(ExtraBase):
    id: UUID4

    class Config:
        from_attributes = True