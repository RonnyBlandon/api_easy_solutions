from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID
from core.security import get_current_active_user
from database.models.business_model import Business
from database.models.product_model import Product
from database.session import get_db
from database.models.favourite_model import Favourite
from schemas.auth_schemas import TokenData
from schemas.business_schemas import BusinessListResponse
from schemas.favourite_schemas import FavouriteBusinessCreate, FavouriteProductCreate, FavouriteResponse
from schemas.product_schemas import ProductListResponse

router = APIRouter(prefix="/favourites", tags=["Favourites"])

@router.post("/business/", status_code=status.HTTP_201_CREATED, response_model=FavouriteResponse)
def add_favourite_business(favourite: FavouriteBusinessCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    user_id = current_user.local_id
    
    # Verificar si el negocio ya está en favoritos
    existing_favourite = db.query(Favourite).filter(
        Favourite.user_id == user_id,
        Favourite.business_id == favourite.business_id
    ).first()
    if existing_favourite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El negocio ya está en favoritos."
        )
    
    # Crear y guardar el favorito
    db_favourite = Favourite(user_id=user_id, business_id=favourite.business_id)
    db.add(db_favourite)
    db.commit()
    db.refresh(db_favourite)

    return {"message": "Negocio agregado a favoritos correctamente"}

@router.post("/product/", status_code=status.HTTP_201_CREATED, response_model=FavouriteResponse)
def add_favourite_product(favourite: FavouriteProductCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    user_id = current_user.local_id
    
    # Verificar si el producto ya está en favoritos
    existing_favourite = db.query(Favourite).filter(
        Favourite.user_id == user_id,
        Favourite.product_id == favourite.product_id
    ).first()
    if existing_favourite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El producto ya está en favoritos. {existing_favourite.product_id}"
        )
    
    # Crear y guardar el favorito
    db_favourite = Favourite(user_id=user_id, product_id=favourite.product_id)
    db.add(db_favourite)
    db.commit()
    db.refresh(db_favourite)

    return {"message": "Producto agregado a favoritos correctamente"}


@router.get("/businesses", response_model=BusinessListResponse)
def get_favourite_businesses(current_user: TokenData = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Obtiene la lista de negocios que el usuario ha marcado como favoritos.
    """
    businesses = (
        db.query(Business)
        .join(Favourite, Business.id == Favourite.business_id)
        .filter(Favourite.user_id == current_user.local_id)
        .all()
    )
    return {"business_list": businesses}

@router.get("/products", response_model=ProductListResponse)
def get_favourite_products(current_user: TokenData = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Obtiene la lista de productos que el usuario ha marcado como favoritos.
    """
    products = (
        db.query(Product)
        .join(Favourite, Product.id == Favourite.product_id)
        .filter(Favourite.user_id == current_user.local_id)
        .all()
    )
    return {"product_list": products}

@router.delete("/business/{business_id}", status_code=status.HTTP_200_OK, response_model=FavouriteResponse)
def delete_favourite_business(business_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    favourite = db.query(Favourite).filter(and_(Favourite.user_id == current_user.local_id, Favourite.business_id == business_id)).first()
    if not favourite:
        raise HTTPException(status_code=404, detail="Negocio favorito no encontrado")
    db.delete(favourite)
    db.commit()
    return {"message": "Negocio favorito eliminado correctamente"}

@router.delete("/product/{product_id}", status_code=status.HTTP_200_OK, response_model=FavouriteResponse)
def delete_favourite_product(product_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    favourite = db.query(Favourite).filter(and_(Favourite.user_id == current_user.local_id, Favourite.product_id == product_id)).first()
    if not favourite:
        raise HTTPException(status_code=404, detail="Producto favorito no encontrado")
    db.delete(favourite)
    db.commit()
    return {"message": "Producto favorito eliminado correctamente"}