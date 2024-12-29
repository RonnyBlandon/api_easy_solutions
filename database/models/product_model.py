from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.session import Base

# Modelo para las imágenes de los productos
class ProductImage(Base):
    __tablename__ = 'product_images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    image_url = Column(String, nullable=False)  # URL de la imagen
    image_type = Column(String, nullable=True)  # Tipo de imagen (imagen principal, secundaria, etc.)

    # Relación inversa
    product = relationship("Product", back_populates="images")

# Modelo para las categorías de productos
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    business_id = Column(UUID(as_uuid=True), ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False)

    business = relationship("Business", back_populates="categories")
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

# Modelo para los productos
class Product(Base):
    __tablename__ = 'products'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    product_description = Column(String, nullable=True)
    amount = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)

    options = relationship("Option", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")  # Relación con ProductImage
    category = relationship("Category", back_populates="products")
    favourites = relationship("Favourite", back_populates="product")

# Modelo para las opciones de productos
class Option(Base):
    __tablename__ = 'options'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    max_extras = Column(Integer, nullable=False)
    is_required = Column(Boolean, default=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), nullable=False)

    extras = relationship("Extra", back_populates="option", cascade="all, delete-orphan")
    product = relationship("Product", back_populates="options")

# Modelo para los extras de opciones
class Extra(Base):
    __tablename__ = 'extras'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    option_id = Column(UUID(as_uuid=True), ForeignKey('options.id', ondelete="CASCADE"), nullable=False)

    option = relationship("Option", back_populates="extras")
