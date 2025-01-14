from sqlalchemy import Column, String, Float, Integer, Boolean, DECIMAL, ForeignKey, Table
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

# Esta tabla almacenará las relaciones entre categorías y productos.
category_product_association = Table(
    'category_product_association',
    Base.metadata,
    Column('category_id', Integer, ForeignKey('categories.id', ondelete="CASCADE"), primary_key=True),
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id', ondelete="CASCADE"), primary_key=True)
)


# Modelo para las categorías de productos
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    business_id = Column(UUID(as_uuid=True), ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False)

    business = relationship("Business", back_populates="categories")
    products = relationship(
        "Product",
        secondary=category_product_association,
        back_populates="categories"
    )


# Modelo para los productos
class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String, nullable=False)
    product_price = Column(DECIMAL(precision=10, scale=2), nullable=False)
    product_description = Column(String, nullable=True)
    stock = Column(Integer, default=0)
    available = Column(Boolean, default=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False)
    status = Column(Boolean, default=False)

    # Relaciones con otros modelos
    options = relationship("Option", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    favourites = relationship("Favourite", back_populates="product")
    categories = relationship(
        "Category",
        secondary="category_product_association",
        back_populates="products"
    )


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
    price = Column(DECIMAL(precision=10, scale=2), nullable=False)
    option_id = Column(UUID(as_uuid=True), ForeignKey('options.id', ondelete="CASCADE"), nullable=False)

    option = relationship("Option", back_populates="extras")
