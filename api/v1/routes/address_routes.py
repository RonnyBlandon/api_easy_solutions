from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from database.models.address_model import Address
from schemas.auth_schemas import TokenData
from schemas.address_schemas import AddressCreateSchema, AddressUpdateSchema, AddressResponseSchema, AddressListResponseSchema
from core.security import get_current_active_user

router = APIRouter(prefix="/addresses", tags=["Addresses"])

# Obtener todas las direcciones del usuario autenticado
@router.get("/", response_model=AddressListResponseSchema)
def get_user_addresses(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user)
):
    address_list = db.query(Address).filter(Address.entity_id == current_user.local_id).order_by(Address.is_main_address.desc()).all()
    return {"address_list": address_list}

# Obtener una dirección específica por ID
@router.get("/{address_id}", response_model=AddressResponseSchema)
def get_address_by_id(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user)
):
    address = db.query(Address).filter(
        Address.id == address_id, Address.entity_id == current_user.local_id
    ).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    
    return address

# Crear una nueva dirección
@router.post("/", response_model=AddressResponseSchema, status_code=status.HTTP_201_CREATED)
def create_address(
    address_data: AddressCreateSchema,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user)
):
    if address_data.municipality_id == 0:
        address_data.municipality_id = 1

    # Verificar si el usuario ya tiene direcciones registradas
    existing_addresses = db.query(Address).filter(
        Address.entity_id == str(current_user.local_id),
        Address.entity_type == "USER"
    ).count()

    address_dict = address_data.model_dump()

    # Asignar el ID del usuario autenticado
    address_dict["entity_id"] = str(current_user.local_id)
    address_dict["entity_type"] = "USER"  # Solo clientes pueden tener varias direcciones

    # Si no tiene direcciones previas, establecer is_main_address en True
    if existing_addresses == 0:
        address_dict["is_main_address"] = True

    # Crear la dirección
    new_address = Address(**address_dict)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return new_address

# Actualizar una dirección
@router.put("/", response_model=AddressResponseSchema)
def update_address(update_data: AddressUpdateSchema, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    user_id = current_user.local_id

    # Buscar el método de pago a actualizar
    address = db.query(Address).filter(
        Address.id == update_data.id, Address.entity_type == "USER", Address.entity_id == user_id
    ).first()

    if not address:
        raise HTTPException(status_code=404, detail="Direccón no encontrada")

    # Si la nueva dirección es marcado como principal, desactivar los demás
    if update_data.is_main_address:
        db.query(Address).filter(
            Address.entity_id == user_id, Address.entity_type == "USER", Address.id != update_data.id
        ).update({"is_main_address": False})

    # Actualizar los campos de la dirección
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)
    return address

# Eliminar una dirección
@router.delete("/{address_id}", status_code=status.HTTP_200_OK)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user)
):
    address = db.query(Address).filter(
        Address.id == address_id, Address.entity_id == current_user.local_id
    ).first()

    if not address:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")

    db.delete(address)
    db.commit()

    return {"message": "Dirección eliminada correctamente"}
