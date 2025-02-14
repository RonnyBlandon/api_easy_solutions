from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from database.models.order_model import Order, OrderItem  # Modelos de SQLAlchemy
from database.models.users_model import Driver, BusinessAdmin
from schemas.order_schemas import (
    OrderCreate,
    OrderUpdate,
    OrderResponse
)
from database.session import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

# Obtener todos los pedidos de un usuario
@router.get("/{user_id}", response_model=List[OrderResponse])
def get_orders(user_id: UUID, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders

# Obtener todos los pedidos asignados al repartidor
@router.get("/{driver_id}", response_model=List[OrderResponse])
def get_orders(driver_id: UUID, db: Session = Depends(get_db)):
      
    orders = db.query(Order).filter(Order.driver_id == driver_id).all()
    return orders

# Obtener todos los pedidos de un negocio
@router.get("/{business_id}", response_model=List[OrderResponse])
def get_orders(business_id: UUID, db: Session = Depends(get_db)):
    business = db.query(BusinessAdmin).filter(BusinessAdmin.id == business_id).first()
    if not business:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Este Usuario no tiene autorización o no existe.")
    orders = db.query(Order).filter(Order.business_id == business.id).all()
    return orders

# Obtener un pedido por su ID
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order

# Crear un nuevo pedido
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # Crear el pedido principal
    new_order = Order(
        user_id=order_data.user_id,
        driver_id=order_data.driver_id,
        business_id=order_data.business_id,
        delivery_time=order_data.delivery_time,
        status=order_data.status,
        payment_status=order_data.payment_status,
        subtotal=order_data.subtotal,
        discount=order_data.discount,
        taxes=order_data.taxes,
        delivery_fee=order_data.delivery_fee,
        total=order_data.total,
        delivery_address_type=order_data.delivery_address_type,
        delivery_street_address=order_data.delivery_street_address,
        delivery_latitude=order_data.delivery_latitude,
        delivery_longitude=order_data.delivery_longitude,
        delivery_municipality=order_data.delivery_municipality,
        notes=order_data.notes,
    )
    db.add(new_order)
    db.flush()  # Asegurarse de que el ID del pedido esté disponible

    # Crear los items del pedido
    for item in order_data.order_items:
        new_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            product_name=item.product_name,
            product_price=item.product_price,
            quantity=item.quantity,
            total_price=item.total_price,
        )
        db.add(new_item)

    db.commit()
    db.refresh(new_order)  # Refrescar para incluir los items creados
    return new_order

# Actualizar un pedido
@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: UUID, order_data: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Actualizar los campos permitidos
    for key, value in order_data.dict(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order

# Eliminar un pedido
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    db.delete(order)
    db.commit()
