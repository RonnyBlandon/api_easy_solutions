from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey , Numeric, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.session import Base

# Modelo para las imágenes de los negocios
class BusinessImage(Base):
    __tablename__ = 'business_images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey('businesses.id', ondelete="CASCADE"), nullable=False)
    image_url = Column(String, nullable=False)  # URL de la imagen
    image_type = Column(String, nullable=True)  # Tipo de imagen (logo, portada, etc.)

    # Relación inversa
    business = relationship("Business", back_populates="images")

# Modelo para los tipos de negocio
class TypeBusiness(Base):
    __tablename__ = 'type_business'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    businesses = relationship("Business", back_populates="type_business")

# Modelo para los negocios
class Business(Base):
    __tablename__ = 'businesses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    type_business_id = Column(Integer, ForeignKey('type_business.id', ondelete="CASCADE"), nullable=False, index=True)
    address = Column(String, nullable=False)
    admin_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    business_name = Column(String, nullable=False)
    category_id = Column(Integer, nullable=False, index=True)
    department_id = Column(Integer, ForeignKey('departments.id', ondelete="SET NULL"), nullable=True, index=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id', ondelete="SET NULL"), nullable=True, index=True)
    country = Column(String, nullable=False)
    description = Column(String, nullable=True)
    email = Column(String, nullable=False)
    lat = Column(Float, nullable=True)  # Considera geography en lugar de Float si es necesario
    long = Column(Float, nullable=True)  # Igual que lat
    phone_number = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    is_popular_this_week = Column(Boolean, default=False)
    is_novelty = Column(Boolean, default=False)
    has_free_delivery = Column(Boolean, default=False)
    has_alcohol = Column(Boolean, default=False)
    is_open_now = Column(Boolean, default=False)
    average_price = Column(Numeric(precision=10, scale=2), nullable=True)
    average_delivery = Column(String, nullable=True)

    # Relaciones
    type_business = relationship("TypeBusiness", back_populates="businesses")
    favourites = relationship("Favourite", back_populates="business", cascade="all, delete-orphan")
    images = relationship("BusinessImage", back_populates="business", cascade="all, delete-orphan")  # Relación con BusinessImage
    categories = relationship("Category", back_populates="business", cascade="all, delete-orphan")
    department = relationship("Department", back_populates="businesses")
    municipality = relationship("Municipality", back_populates="businesses")
    invoices = relationship("BusinessInvoice", back_populates="business")
