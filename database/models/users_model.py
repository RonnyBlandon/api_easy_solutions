import uuid 
import enum
from sqlalchemy import Column, String, Boolean, ForeignKey, Enum, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.session import Base

# Definición del Enum para los roles
class UserRole(enum.Enum):
    USER = "USER"
    DRIVER = "DRIVER"
    BUSINESS_ADMIN = "BUSINESS_ADMIN"

# Tabla base de usuarios que almacena credenciales comunes
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}  # Esquema auth

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    profile_image = Column(String, nullable=True)  # URL de la imagen de perfil
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)  # driver, business_admin
    google_user_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Fecha de creación

    # Relaciones con los perfiles según el rol del usuario
    driver_profile = relationship("Driver", back_populates="user", uselist=False)
    business_admin_profile = relationship("BusinessAdmin", back_populates="user", uselist=False)
    favourites = relationship("Favourite", back_populates="user")
    department = relationship("Department", back_populates="users")
    municipality = relationship("Municipality", back_populates="users")

# Tabla para drivers (conductores)
class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(UUID(as_uuid=True), ForeignKey('auth.users.id'), primary_key=True)
    vehicle_type = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    license_image = Column(String, nullable=True)  # URL de la imagen de la licencia
    is_available = Column(Boolean, default=True)

    # Relación inversa hacia la tabla de usuarios
    user = relationship("User", back_populates="driver_profile")

# Tabla para administradores de negocios
class BusinessAdmin(Base):
    __tablename__ = 'business_admins'

    id = Column(UUID(as_uuid=True), ForeignKey('auth.users.id'), primary_key=True)
    business_name = Column(String, nullable=False)
    logo_image = Column(String, nullable=True)  # URL del logo del negocio

    # Relación inversa hacia la tabla de usuarios
    user = relationship("User", back_populates="business_admin_profile")

# Tabla para departamentos
class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    # Relaciones con usuarios y municipios
    users = relationship("User", back_populates="department")
    businesses = relationship("Business", back_populates="department")  # Relación inversa
    municipalities = relationship("Municipality", back_populates="department")

# Tabla para municipios
class Municipality(Base):
    __tablename__ = 'municipalities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))

    # Relaciones con departamento y usuarios
    department = relationship("Department", back_populates="municipalities")
    addresses = relationship("Address", back_populates="municipality")
    users = relationship("User", back_populates="municipality")
    businesses = relationship("Business", back_populates="municipality")

# Tabla de direcciones
class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_type = Column(String, nullable=False)  # Tipo de dirección (casa, trabajo, etc.)
    street_address = Column(String, nullable=False)
    latitude = Column(String, nullable=True)  # Latitud para Google Maps
    longitude = Column(String, nullable=True)  # Longitud para Google Maps

    # Relaciones con municipios
    municipality_id = Column(Integer, ForeignKey('municipalities.id'))
    municipality = relationship("Municipality", back_populates="addresses")
