from decimal import Decimal
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric, Enum, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from database.session import Base

class PaymentStatus(enum.Enum):
    PENDING = "Pendiente"
    IN_PROGRESS = "En Curso"
    DELIVERED = "Entregado"
    CANCELED = "Cancelado"

class OrderStatus(enum.Enum):
    PAID = "Pagado"
    PENDING = "Pendiente"
    FAILED = "Fallido"

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="CASCADE"), nullable=False)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("drivers.id", ondelete="CASCADE"), nullable=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    # Tiempos del pedido
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # Fecha de creación
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # Última actualización
    delivery_time = Column(DateTime, nullable=True)  # Hora estimada de entrega
    completed_at = Column(DateTime, nullable=True)  # Hora en que se completó
    canceled_at = Column(DateTime, nullable=True)  # Hora en que se canceló
    # Estado
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False)  # Estado del pago: "pending", "paid", "failed"
    # Totales financieros
    subtotal = Column(Numeric(precision=10, scale=2), nullable=False)
    discount = Column(Numeric(precision=10, scale=2), nullable=False)
    taxes = Column(Numeric(precision=10, scale=2), nullable=False)
    delivery_fee = Column(Numeric(precision=10, scale=2), nullable=False)
    total = Column(Numeric(precision=10, scale=2), nullable=False)
    # Dirección de entrega
    delivery_address_type = Column(String, nullable=False)  # Tipo de dirección (casa, trabajo, etc.)
    delivery_street_address = Column(String, nullable=False)  # Dirección completa
    delivery_latitude = Column(String, nullable=True)  # Latitud
    delivery_longitude = Column(String, nullable=True)  # Longitud
    delivery_municipality = Column(String, nullable=False)  # Municipio (nombre textual)
    # Notas del pedido
    notes = Column(String, nullable=True)  # Instrucciones o comentarios del cliente

    # Relación con los productos del pedido
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def calculate_totals(self, tax_rate: Decimal, delivery_fee: Decimal):
        """ Calcula los totales del pedido, incluyendo descuentos. """
        # Calcular el subtotal de los productos
        self.subtotal = sum(
            item.quantity * item.product_price for item in self.order_items
        )
        # Aplicar el descuento al subtotal
        discounted_subtotal = max(self.subtotal - self.discount, Decimal(0))  # Evitar subtotales negativos
        self.taxes = discounted_subtotal * tax_rate    # Calcular impuestos sobre el subtotal con descuento
        self.delivery_fee = delivery_fee    # Asignar el costo de envío
        self.total = discounted_subtotal + self.taxes + self.delivery_fee   # Calcular el total final


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    product_name = Column(String, nullable=False)
    product_price = Column(Numeric(precision=10, scale=2), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Numeric(precision=10, scale=2), nullable=False)
    
    order = relationship("Order", back_populates="order_items")
