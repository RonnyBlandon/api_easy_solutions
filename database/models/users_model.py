import uuid
import enum
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.session import Base

# Enum para los roles
class RoleEnum(enum.Enum):
    USER = 'USER'
    DRIVER = 'DRIVER'
    BUSINESS_ADMIN = 'BUSINESS_ADMIN'

# Enum para los proveedores de autenticación
class AuthProviderEnum(enum.Enum):
    EMAIL = 'EMAIL'
    GOOGLE = 'GOOGLE'

# Tabla base de usuarios que almacena credenciales comunes
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}  # Esquema auth

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime(timezone=True), server_default=func.now())  # Fecha de creación
    providers = Column(ARRAY(Enum(AuthProviderEnum)), default=[AuthProviderEnum.EMAIL], nullable=False)
    roles = Column(ARRAY(Enum(RoleEnum)), default=[RoleEnum.USER], nullable=False)
    # Relaciones
    driver_profile = relationship("Driver", back_populates="user", uselist=False)
    business_admin_profile = relationship("BusinessAdmin", back_populates="user", uselist=False)
    favourites = relationship("Favourite", back_populates="user")
    cart = relationship("Cart", back_populates="user")

# Tabla para drivers (conductores)
class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(UUID(as_uuid=True), ForeignKey('auth.users.id', ondelete="CASCADE"), primary_key=True)
    profile_image = Column(String, nullable=True)  # URL de la imagen de perfil
    vehicle_type = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    license_image = Column(String, nullable=True)  # URL de la imagen de la licencia
    is_available = Column(Boolean, default=True)

    # Relación inversa hacia la tabla de usuarios
    user = relationship("User", back_populates="driver_profile")

# Tabla para administradores de negocios
class BusinessAdmin(Base):
    __tablename__ = 'business_admins'

    id = Column(UUID(as_uuid=True), ForeignKey('auth.users.id', ondelete="CASCADE"), primary_key=True)
    business_name = Column(String, nullable=False)
    logo_image = Column(String, nullable=True)  # URL del logo del negocio

    # Relación inversa hacia la tabla de usuarios
    user = relationship("User", back_populates="business_admin_profile")

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

# Tabla de direcciones
class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_type = Column(String, nullable=False)  # Tipo de dirección (casa, trabajo, etc.)
    street_address = Column(String, nullable=False)
    latitude = Column(String, nullable=True)  # Latitud para Google Maps
    longitude = Column(String, nullable=True)  # Longitud para Google Maps

    # Relación con municipios
    municipality_id = Column(Integer, ForeignKey('municipalities.id', ondelete="CASCADE"))
    municipality = relationship("Municipality", back_populates="addresses")
