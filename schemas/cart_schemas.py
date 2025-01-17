from pydantic import BaseModel
from typing import List
from uuid import UUID
from decimal import Decimal
from datetime import datetime

# Esquema base para el carrito
class CartBase(BaseModel):
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    subtotal: Decimal
    taxes: Decimal
    delivery_fee: Decimal
    total: Decimal

    class Config:
        from_attributes = True  # Permite que Pydantic pueda leer datos directamente de SQLAlchemy

# Esquema para la creación de un carrito
class CartCreate(CartBase):
    pass

# Esquema para la actualización de un carrito
class CartUpdate(CartBase):
    subtotal: Decimal
    taxes: Decimal
    delivery_fee: Decimal
    total: Decimal

# Esquema de respuesta del carrito, con los items incluidos
class CartResponse(CartBase):
    cart_items: List['CartItemBase']  # Relación de items en el carrito

    class Config:
        from_attributes = True  # Permite la conversión de instancias de SQLAlchemy a dict y viceversa


# Esquema base para los elementos dentro del carrito
class CartItemBase(BaseModel):
    product_id: UUID
    quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Permite que Pydantic pueda leer datos directamente de SQLAlchemy

# Esquema para la creación de un elemento dentro del carrito
class CartItemCreate(CartItemBase):
    pass

# Esquema para la actualización de un elemento dentro del carrito
class CartItemUpdate(CartItemBase):
    quantity: int

# Esquema de respuesta de un elemento dentro del carrito, con información adicional
class CartItemResponse(CartItemBase):
    product_name: str  # Nombre del producto
    product_price: Decimal  # Precio del producto

    class Config:
        from_attributes = True  # Permite la conversión de instancias de SQLAlchemy a dict y viceversa
