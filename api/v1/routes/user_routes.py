from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from core.security import get_current_active_user
from schemas.user_schemas import (UserSchemaResponse, UserSchemaUpdate)
from database.models.users_model import User
from database.session import get_db
from schemas.auth_schemas import TokenData
from utils.validators import validate_phone_number

router = APIRouter(prefix="/users", tags=["Users"])

# Obtener un usuario por token
@router.get("/", response_model=UserSchemaResponse)
def get_user(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    user_id = current_user.local_id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    # Retornar el usuario con los roles transformados
    return {
        "id": user.id,
        "email": user.email,
        "phone_number": user.phone_number,
        "full_name": user.full_name,
        "municipality_id": user.municipality_id,
        "is_active": user.is_active,
        "start_date": user.start_date,
        "providers": user.providers,
        "roles": user.roles
    }

# Actualizar un usuario
@router.put("/", response_model=UserSchemaResponse)
def update_user(user: UserSchemaUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    user_id = current_user.local_id
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    # Validar el número de teléfono solo si se proporciona
    if user.phone_number:
        validate_phone_number(user.phone_number)

    # Actualizar los campos del usuario con los datos recibidos
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(existing_user, key, value)
    
    db.commit()
    db.refresh(existing_user)
    
    # Retornar el usuario actualizado con los roles transformados
    return {
        "id": existing_user.id,
        "email": existing_user.email,
        "phone_number": existing_user.phone_number,
        "full_name": existing_user.full_name,
        "municipality_id": existing_user.municipality_id,
        "is_active": existing_user.is_active,
        "start_date": existing_user.start_date,
        "providers": existing_user.providers,
        "roles": existing_user.roles
    }


# Eliminar un usuario
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    db.delete(user)
    db.commit()
    return