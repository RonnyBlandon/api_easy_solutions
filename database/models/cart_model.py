from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.session import Base

class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Campos financieros
    subtotal = Column(Numeric(precision=10, scale=2), nullable=False, default=Decimal('0.00'))  # Suma de los precios de los productos
    taxes = Column(Numeric(precision=10, scale=2), nullable=False, default=Decimal('0.00'))  # Impuestos calculados
    delivery_fee = Column(Numeric(precision=10, scale=2), nullable=False, default=Decimal('0.00'))  # Costo de envío
    total = Column(Numeric(precision=10, scale=2), nullable=False, default=Decimal('0.00'))  # Total = Subtotal + Taxes + Delivery Fee

    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete")
    user = relationship("User", back_populates="cart")  # Relación inversa con User

    def calculate_totals(self, tax_rate: Decimal, delivery_fee: Decimal):
        """Método para calcular subtotal, impuestos y total usando Decimal."""
        if not self.cart_items:
            self.subtotal = Decimal('0.00')
        else:
            self.subtotal = sum(item.quantity * (item.product.price or Decimal('0.00')) for item in self.cart_items)
        self.taxes = self.subtotal * tax_rate
        self.delivery_fee = delivery_fee
        self.total = self.subtotal + self.taxes + self.delivery_fee


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product")
