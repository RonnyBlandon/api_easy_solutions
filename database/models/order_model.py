import datetime
from decimal import Decimal
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from database.session import Base

class OrderStatus(enum.Enum):
    PENDING = "Pendiente"
    IN_PROGRESS = "En Curso"
    DELIVERED = "Entregado"
    CANCELED = "Cancelado"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Relación con usuario
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=True)  # Relación con el driver
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)  # Relación con el negocio
    created_at = Column(DateTime, nullable=False)  # Fecha de creación del pedido
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)

    # Totales financieros
    subtotal = Column(Numeric(precision=10, scale=2), nullable=False)  # Suma de los precios de los productos
    taxes = Column(Numeric(precision=10, scale=2), nullable=False)  # Impuestos calculados
    delivery_fee = Column(Numeric(precision=10, scale=2), nullable=False)  # Costo de envío
    total = Column(Numeric(precision=10, scale=2), nullable=False)  # Total = Subtotal + Taxes + Delivery Fee

    # Relación con los productos del pedido
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def calculate_totals(self, tax_rate: Decimal, delivery_fee: Decimal):
        """Método para calcular subtotal, impuestos y total usando Decimal."""
        self.subtotal = sum(
            item.quantity * item.unit_price for item in self.order_items
        )
        self.taxes = self.subtotal * tax_rate
        self.delivery_fee = delivery_fee
        self.total = self.subtotal + self.taxes + self.delivery_fee


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=True)  # Puede ser nulo si el producto es eliminado
    product_name = Column(String, nullable=False)  # Copia del nombre del producto
    product_price = Column(Numeric(precision=10, scale=2), nullable=False)  # Copia del precio del producto
    quantity = Column(Integer, nullable=False)
    total_price = Column(Numeric(precision=10, scale=2), nullable=False)  # Precio total del ítem = product_price * quantity
    order = relationship("Order", back_populates="items")
