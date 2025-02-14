from datetime import datetime, timezone
from decimal import Decimal
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from database.models.product_model import Product
from database.session import get_db
from database.models.cart_model import Cart, CartItem
from schemas.product_schemas import ProductResponse
from schemas.cart_schemas import (
    CartCreate,
    CartResponse,
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
)

router = APIRouter(prefix="/carts", tags=["Carts"])

# Endpoints para "Cart"

@router.get("/carts/{user_id}", response_model=List[CartResponse])
def get_carts_for_user(user_id: UUID, db: Session = Depends(get_db)):
    """Obtiene todos los carritos de un usuario con productos completos."""
    carts = db.query(Cart).filter(Cart.user_id == user_id).all()
    
    tax_rate = Decimal("0.15")
    delivery_fee = Decimal("50.00")
    
    cart_responses = []
    for cart in carts:
        # Recalcula totales dinámicamente
        subtotal = sum(
            item.quantity * (item.product.price or Decimal('0.00')) for item in cart.cart_items
        )
        discount_total = sum(
            item.quantity * (item.product.discount or Decimal('0.00')) for item in cart.cart_items
        )
        effective_subtotal = subtotal - discount_total
        taxes = effective_subtotal * tax_rate
        total = effective_subtotal + delivery_fee

        # Construye la respuesta del carrito
        cart_responses.append(CartResponse(
            id=cart.id,
            user_id=cart.user_id,
            business_id=cart.business_id,
            created_at=cart.created_at,
            updated_at=cart.updated_at,
            subtotal=subtotal,
            discount_total=discount_total,
            taxes=taxes,
            delivery_fee=delivery_fee,
            total=total,
            cart_items=[
                CartItemResponse(
                    id=item.id,
                    product_id=item.product.id,
                    product=ProductResponse(
                        id=item.product.id,
                        name=item.product.name,
                        price=item.product.price,
                        product_image_url=item.product.product_image_url,
                        discount=item.product.discount,
                        available=item.product.available,
                        business_id=item.product.business_id,
                        is_active=item.product.is_active
                    ),
                    quantity=item.quantity,
                    created_at=item.created_at,
                    updated_at=item.updated_at
                )
                for item in cart.cart_items
            ]
        ))
    
    return cart_responses


@router.delete("/carts/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    """Elimina un carrito por su ID."""
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    db.delete(cart)
    db.commit()
    return {"detail": "Cart deleted successfully"}

# Endpoints para "CartItem"

@router.post("/carts/{business_id}/items", response_model=CartResponse)
def add_item_to_cart(business_id: UUID, user_id: UUID, item: CartItemCreate, db: Session = Depends(get_db)):
    """Añade un producto al carrito o actualiza su cantidad, recalculando totales."""
    # Parámetros constantes para cálculos
    tax_rate = Decimal("0.15")  # Tasa de impuestos
    delivery_fee = Decimal("50.00")  # Tarifa fija de envío

    # Buscar el carrito del usuario para el negocio
    cart = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.business_id == business_id
    ).first()

    # Crear el carrito si no existe
    if not cart:
        cart = Cart(
            user_id=user_id,
            business_id=business_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            subtotal=Decimal("0.00"),
            discount_total=Decimal("0.00"),
            taxes=Decimal("0.00"),
            delivery_fee=delivery_fee,
            total=Decimal("0.00"),
        )
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Verificar si el producto existe
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")

    # Verificar si el producto ya está en el carrito
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id
    ).first()

    if cart_item:
        # Actualizar la cantidad del producto
        new_quantity = cart_item.quantity + item.quantity

        # Verificar disponibilidad y stock
        if product.stock < new_quantity or not product.available:
            raise HTTPException(
                status_code=400,
                detail=f"Actualmente solo quedan {product.stock} unidades."
            )

        cart_item.quantity = new_quantity
        cart_item.updated_at = datetime.now(timezone.utc)
    else:
        # Verificar disponibilidad y stock al agregar el producto
        if product.stock < item.quantity or not product.available:
            raise HTTPException(
                status_code=400,
                detail=f"Actualmente solo quedan {product.stock} unidades."
            )

        # Añadir un nuevo producto al carrito
        cart_item = CartItem(
            product_id=item.product_id,
            quantity=item.quantity,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            cart_id=cart.id
        )
        db.add(cart_item)

    # Calcular valores dinámicos para el carrito
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    subtotal = sum(
        ci.quantity * (product.price or Decimal('0.00')) for ci in cart_items
    )
    discount_total = sum(
        ci.quantity * (product.discount or Decimal('0.00')) for ci in cart_items
    )
    effective_subtotal = subtotal - discount_total
    taxes = effective_subtotal * tax_rate
    total = effective_subtotal + delivery_fee

    # Actualizar el carrito
    cart.updated_at = datetime.now(timezone.utc)
    cart.subtotal = subtotal
    cart.discount_total = discount_total
    cart.taxes = taxes
    cart.delivery_fee = delivery_fee
    cart.total = total

    db.commit()
    db.refresh(cart)

    # Preparar la respuesta del carrito
    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        business_id=cart.business_id,
        created_at=cart.created_at,
        updated_at=cart.updated_at,
        subtotal=subtotal,
        discount_total=discount_total,
        taxes=taxes,
        delivery_fee=delivery_fee,
        total=total,
        items=[
            CartItemResponse(
                id=ci.id,
                product_id=product.id,
                product=ProductResponse(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    discount=product.discount,
                    available=product.available,
                    business_id=product.business_id,
                    status=product.status,
                ),
                quantity=ci.quantity,
                created_at=ci.created_at,
                updated_at=ci.updated_at,
            )
            for ci in cart_items
        ]
    )


@router.put("/carts/{cart_id}/items/{item_id}", response_model=CartResponse)
def update_cart_item(cart_id: int, item_id: int, item: CartItemUpdate, db: Session = Depends(get_db)):
    """Actualiza la cantidad de un elemento del carrito, recalcula los totales y retorna el carrito completo."""
    # Buscar el item existente
    existing_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Obtener producto asociado
    product = db.query(Product).filter(Product.id == existing_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Verificar stock
    if item.quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente del producto '{product.name}'. Disponible: {product.stock}"
        )
    
    # Actualizar cantidad en el item del carrito
    existing_item.quantity = item.quantity
    db.commit()
    db.refresh(existing_item)

    # Recalcular totales del carrito
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    subtotal = sum(
        ci.quantity * (db.query(Product).filter(Product.id == ci.product_id).first().price or Decimal('0.00'))
        for ci in cart_items
    )
    discount_total = sum(
        ci.quantity * (db.query(Product).filter(Product.id == ci.product_id).first().discount or Decimal('0.00'))
        for ci in cart_items
    )
    effective_subtotal = subtotal - discount_total
    tax_rate = Decimal("0.15")  # Ejemplo de tasa de impuestos
    taxes = effective_subtotal * tax_rate
    delivery_fee = Decimal("5.00")  # Ejemplo de tarifa de entrega
    total = effective_subtotal + taxes + delivery_fee

    # Actualizar valores en el carrito
    cart.updated_at = datetime.now(timezone.utc)
    cart.subtotal = subtotal
    cart.discount_total = discount_total
    cart.taxes = taxes
    cart.delivery_fee = delivery_fee
    cart.total = total

    db.commit()
    db.refresh(cart)

    # Preparar y retornar la respuesta del carrito completo
    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        business_id=cart.business_id,
        created_at=cart.created_at,
        updated_at=cart.updated_at,
        subtotal=subtotal,
        discount_total=discount_total,
        taxes=taxes,
        delivery_fee=delivery_fee,
        total=total,
        items=[
            CartItemResponse(
                id=ci.id,
                product_id=ci.product_id,
                product=ProductResponse(
                    id=ci.product_id,
                    name=(product := db.query(Product).filter(Product.id == ci.product_id).first()).name,
                    price=product.price,
                    discount=product.discount,
                    available=product.available,
                    business_id=product.business_id,
                    status=product.status,
                ),
                quantity=ci.quantity,
                created_at=ci.created_at,
                updated_at=ci.updated_at,
            )
            for ci in cart_items
        ]
    )


@router.delete("/carts/{cart_id}/items/{item_id}")
def delete_cart_item(cart_id: int, item_id: int, db: Session = Depends(get_db)):
    """Elimina un elemento de un carrito."""
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(item)
    db.commit()
    return {"detail": f"Artículo del carrito eliminado exitosamente"}
