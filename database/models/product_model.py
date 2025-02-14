from decimal import Decimal
from sqlalchemy import Column, String, Integer, Boolean, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.session import Base

# Esta tabla almacenará las relaciones entre categorías y productos.
class CategoryProductAssociation(Base):
    __tablename__ = 'category_product_association'

    category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"), primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True)


# Modelo para las categorías de productos
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    business_id = Column(UUID(as_uuid=True), ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False)

    business = relationship("Business", back_populates="business_categories")
    products = relationship("Product", secondary="category_product_association", back_populates="categories")


# Modelo para los productos
class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price = Column(Numeric(precision=10, scale=2), default=Decimal("0.00"), nullable=False)
    description = Column(String, nullable=True)
    product_image_url = Column(String, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    available = Column(Boolean, default=True, nullable=False)
    business_id = Column(UUID(as_uuid=True), ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False)
    discount = Column(Numeric(precision=10, scale=2), nullable=True, default=0.00)
    is_active = Column(Boolean, default=False)

    # Relaciones con otros modelos
    options = relationship("Option", back_populates="product", cascade="all, delete-orphan")
    favourites = relationship("Favourite", back_populates="product")
    categories = relationship("Category", secondary="category_product_association", back_populates="products")

    # Restricciones
    __table_args__ = (
        CheckConstraint("price >= 0 AND discount >= 0 AND discount <= price", name="check_valid_discount"),
    )

    def get_discounted_price(self) -> Decimal:
        """
        Calcula el precio final después de aplicar el descuento.
        :return: Precio con descuento aplicado.
        """
        return max(self.price - (self.discount or 0), 0)  # Asegura que no haya precios negativos


# Modelo para las opciones de productos
class Option(Base):
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    max_extras = Column(Integer, default=0, nullable=False)
    is_required = Column(Boolean, default=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), nullable=False)

    extras = relationship("Extra", back_populates="option", cascade="all, delete-orphan")
    product = relationship("Product", back_populates="options")

# Modelo para los extras de opciones
class Extra(Base):
    __tablename__ = 'extras'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=True)
    option_id = Column(Integer, ForeignKey('options.id', ondelete="CASCADE"), nullable=False)

    option = relationship("Option", back_populates="extras")
