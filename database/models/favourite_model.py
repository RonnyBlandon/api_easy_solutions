from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.session import Base

# Modelo para los favoritos
class Favourite(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="CASCADE"), nullable=False, index=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=True)

    # Restricción para evitar que ambos campos sean nulos o ambos tengan datos
    __table_args__ = (
        UniqueConstraint('user_id', 'business_id', name='unique_user_business'),
        UniqueConstraint('user_id', 'product_id', name='unique_user_product')
    )

    # Relaciones con otros modelos
    user = relationship("User", back_populates="favourites")
    business = relationship("Business", back_populates="favourites")
    product = relationship("Product", back_populates="favourites")
