from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from core.security import get_current_active_user
from database.session import get_db
from database.models.payment_method_model import PaymentMethod
from schemas.auth_schemas import TokenData
from schemas.payment_method_schemas import PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodResponse, PaymentMethodListResponse

router = APIRouter(prefix="/payment_methods", tags=["Payment Methods"])

@router.post("/", response_model=PaymentMethodResponse)
def add_payment_method(payment_data: PaymentMethodCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    user_id = current_user.local_id
    new_payment = PaymentMethod(**payment_data.model_dump(), user_id=user_id)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/", response_model=PaymentMethodListResponse)
def list_payment_methods(
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_active_user)
):
    user_id = current_user.local_id
    payment_method_list = (
        db.query(PaymentMethod)
        .filter(PaymentMethod.user_id == user_id)
        .order_by(PaymentMethod.is_main_payment_method.desc())  # Ordena por principal primero
        .all()
    )
    return {"payment_method_list": payment_method_list}

@router.get("/{payment_id}", response_model=PaymentMethodResponse)
def get_payment_method(payment_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    user_id = current_user.local_id
    payment = db.query(PaymentMethod).filter(
        PaymentMethod.id == payment_id, PaymentMethod.user_id == user_id
    ).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    return payment

@router.put("/", response_model=PaymentMethodResponse)
def update_payment(update_data: PaymentMethodUpdate, db: Session = Depends(get_db),current_user: TokenData = Depends(get_current_active_user)):
    user_id = current_user.local_id

    # Buscar el método de pago a actualizar
    payment = db.query(PaymentMethod).filter(
        PaymentMethod.id == update_data.id, PaymentMethod.user_id == user_id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")

    # Si el nuevo método es marcado como principal, desactivar los demás
    if update_data.is_main_payment_method:
        db.query(PaymentMethod).filter(
            PaymentMethod.user_id == user_id, PaymentMethod.id != update_data.id
        ).update({"is_main_payment_method": False})

    # Actualizar los campos del método de pago
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment


@router.delete("/{payment_id}")
def remove_payment_method(payment_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    user_id = current_user.local_id
    payment = db.query(PaymentMethod).filter(
        PaymentMethod.id == payment_id, PaymentMethod.user_id == user_id
    ).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")

    db.delete(payment)
    db.commit()
    return {"message": "Método de pago eliminado"}
