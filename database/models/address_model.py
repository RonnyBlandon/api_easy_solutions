from enum import Enum  # Importa Enum del módulo estándar de Python
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.session import Base
from sqlalchemy import Enum as SQLAlchemyEnum  # Importa el Enum de SQLAlchemy

# Tabla para departamentos
class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    # Relaciones con municipios
    municipalities = relationship("Municipality", back_populates="department")

# Tabla para municipios
class Municipality(Base):
    __tablename__ = 'municipalities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id', ondelete="CASCADE"))

    # Relaciones con departamentos
    department = relationship("Department", back_populates="municipalities")
    addresses = relationship("Address", back_populates="municipality")
    businesses = relationship("Business", back_populates="municipality")

# Enum para tipos de entidad
class EntityTypeEnum(str, Enum):
    USER = "USER"
    BUSINESS = "BUSINESS"

# Tabla de direcciones
class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(UUID(as_uuid=True), nullable=False)  # ID del usuario o negocio
    entity_type = Column(SQLAlchemyEnum(EntityTypeEnum, name="entity_type_enum", native_enum=False), nullable=False)  # "usuario" o "negocio"
    alias = Column(String, nullable=False)  # Alias (Ej: "Mi casa", "Trabajo")
    address = Column(String, nullable=False)
    reference = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)  # Latitud para Google Maps
    longitude = Column(Float, nullable=True)  # Longitud para Google Maps
    is_main_address = Column(Boolean, default=False, nullable=False)

    # Relación con municipios
    municipality_id = Column(Integer, ForeignKey('municipalities.id', ondelete="CASCADE"))
    municipality = relationship("Municipality", back_populates="addresses")