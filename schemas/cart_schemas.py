from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from schemas.product_schemas import ProductResponse

# Esquema base para Cart
class CartBase(BaseModel):
    user_id: UUID
    business_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    subtotal: Decimal
    discount_total: Decimal
    taxes: Decimal
    delivery_fee: Decimal
    total: Decimal

    class Config:
        from_attributes = True  # Permite leer datos desde objetos SQLAlchemy

# Esquema para crear un Cart
class CartCreate(CartBase):
    pass

# Esquema para actualizar un Cart
class CartUpdate(CartBase):
    pass

# Esquema de respuesta para Cart, incluyendo sus items
class CartResponse(CartBase):
    id: int
    items: List['CartItemResponse'] = []  # Relación con los items

    class Config:
        from_attributes = True

# Esquema base para CartItem
class CartItemBase(BaseModel):
    product_id: UUID
    quantity: int = Field(..., ge=1)  # Asegura que la cantidad sea al menos 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquema para crear un CartItem
class CartItemCreate(CartItemBase):
    pass

# Esquema para actualizar un CartItem
class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)  # Asegura que la cantidad sea al menos 1

# Esquema de respuesta para CartItem, incluyendo información del producto
class CartItemResponse(CartItemBase):
    id: int
    product: ProductResponse

    class Config:
        from_attributes = True
