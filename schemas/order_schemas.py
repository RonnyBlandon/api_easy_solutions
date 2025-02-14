from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import datetime
import enum

class PaymentStatusEnum(str, enum.Enum):
    PENDING = "Pendiente"
    IN_PROGRESS = "En Curso"
    DELIVERED = "Entregado"
    CANCELED = "Cancelado"

class OrderStatusEnum(str, enum.Enum):
    PAID = "Pagado"
    PENDING = "Pendiente"
    FAILED = "Fallido"

# Base para Order
class OrderBase(BaseModel):
    user_id: UUID
    driver_id: Optional[UUID]
    business_id: UUID
    delivery_time: Optional[datetime]
    status: OrderStatusEnum
    payment_status: PaymentStatusEnum
    subtotal: Decimal
    discount: Decimal
    taxes: Decimal
    delivery_fee: Decimal
    total: Decimal
    delivery_address_type: str
    delivery_street_address: str
    delivery_latitude: Optional[str]
    delivery_longitude: Optional[str]
    delivery_municipality: str
    notes: Optional[str]

# Esquema para creación
class OrderCreate(OrderBase):
    order_items: List['OrderItemCreate'] = Field(default_factory=list)

# Esquema para actualización
class OrderUpdate(BaseModel):
    status: Optional[OrderStatusEnum]
    payment_status: Optional[PaymentStatusEnum]
    delivery_time: Optional[datetime]
    notes: Optional[str]

# Esquema para respuesta
class OrderResponse(OrderBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    canceled_at: Optional[datetime]
    order_items: List['OrderItemResponse']

    class Config:
        from_attributes = True


# Base para OrderItem
class OrderItemBase(BaseModel):
    product_id: Optional[UUID]
    product_name: str
    product_price: Decimal
    quantity: int
    total_price: Decimal

# Esquema para creación
class OrderItemCreate(OrderItemBase):
    pass

# Esquema para respuesta
class OrderItemResponse(OrderItemBase):
    id: UUID

    class Config:
        from_attributes = True