import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from database.models.product_model import Product
from database.session import get_db
from database.models.cart_model import Cart, CartItem
from schemas.cart_schemas import CartResponse, CartItemCreate

router = APIRouter(prefix="/cart", tags=["cart"])

# Obtener carrito del usuario
@router.get("/", response_model=CartResponse)
def get_cart(user_id: UUID, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    return cart


# Agregar o actualizar un artículo en el carrito
@router.post("/items", response_model=CartResponse)
def add_or_update_cart_item(user_id: UUID, item: CartItemCreate, db: Session = Depends(get_db)):
    DELIVERY_FEE = 50.00  # tarifa fija de entrega

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        # Crear carrito si no existe
        cart = Cart(user_id=user_id, subtotal=0.0, total=0.0)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Obtener el producto relacionado
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="El producto no existe.")

    # Verificar si el producto tiene stock suficiente
    if product.stock is not None and item.quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente. Solo hay {product.stock} unidades disponibles."
        )

    # Buscar si el producto ya está en el carrito
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == item.product_id).first()
    if cart_item:
        # Actualizar la cantidad del artículo
        cart_item.quantity += item.quantity
        cart_item.updated_at = datetime.datetime.now()
    else:
        # Agregar un nuevo artículo al carrito
        cart_item = CartItem(cart_id=cart.id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)

    # Actualizar subtotal y total del carrito
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    cart.subtotal = sum(item.quantity * product.price for item in cart_items)
    cart.delivery_fee = DELIVERY_FEE
    cart.total = cart.subtotal + cart.delivery_fee # Aquí puedes aplicar descuentos o impuestos si es necesario

    # Guardar cambios en la base de datos
    db.commit()
    db.refresh(cart)
    return cart


# Eliminar un artículo del carrito
@router.delete("/items/{product_id}", response_model=CartResponse)
def remove_cart_item(user_id: UUID, product_id: UUID, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")

    db.delete(cart_item)
    db.commit()
    return cart


# Vaciar el carrito
@router.delete("/", response_model=CartResponse)
def clear_cart(user_id: UUID, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return cart
