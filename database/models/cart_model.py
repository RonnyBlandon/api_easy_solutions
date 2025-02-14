from sqlalchemy.sql import func
from decimal import Decimal
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.session import Base

class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="CASCADE"), nullable=False, index=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True)  # Relación con el negocio
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    # Totales financieros
    subtotal = Column(Numeric(precision=10, scale=2), nullable=False)
    discount = Column(Numeric(precision=10, scale=2), nullable=False)
    taxes = Column(Numeric(precision=10, scale=2), nullable=False)
    delivery_fee = Column(Numeric(precision=10, scale=2), nullable=False)
    total = Column(Numeric(precision=10, scale=2), nullable=False)

    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete")
    user = relationship("User", back_populates="cart")
    business = relationship("Business")  # Relación con el negocio


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product")
