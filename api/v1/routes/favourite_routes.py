from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from database.models.favourite_model import Favourite
from schemas.favourite_schemas import FavouriteCreate, FavouriteResponse

router = APIRouter(prefix="/favourites", tags=["Favourites"])

@router.post("/", response_model=FavouriteResponse)
def create_favourite(favourite: FavouriteCreate, db: Session = Depends(get_db)):
    if not (favourite.business_id or favourite.product_id):
        raise HTTPException(status_code=400, detail="Either business_id or product_id must be provided.")
    db_favourite = Favourite(**favourite.model_dump())
    db.add(db_favourite)
    db.commit()
    db.refresh(db_favourite)
    return db_favourite

@router.get("/", response_model=List[FavouriteResponse])
def get_all_favourites(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los favoritos del usuario, incluyendo negocios y productos.
    """
    return db.query(Favourite).filter(Favourite.user_id == user_id).all()

@router.get("/businesses", response_model=List[FavouriteResponse])
def get_business_favourites(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene solo los favoritos asociados a negocios.
    """
    return db.query(Favourite).filter(Favourite.user_id == user_id, Favourite.business_id != None).all()

@router.get("/products", response_model=List[FavouriteResponse])
def get_product_favourites(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene solo los favoritos asociados a productos.
    """
    return db.query(Favourite).filter(Favourite.user_id == user_id, Favourite.product_id != None).all()

@router.delete("/{favourite_id}", status_code=204)
def delete_favourite(favourite_id: int, db: Session = Depends(get_db)):
    favourite = db.query(Favourite).filter(Favourite.id == favourite_id).first()
    if not favourite:
        raise HTTPException(status_code=404, detail="Favourite not found")
    db.delete(favourite)
    db.commit()
