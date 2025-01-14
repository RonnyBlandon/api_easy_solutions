from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from database.session import get_db
from database.models.product_model import Product, Category
from schemas.product_schemas import (CategoryCreate, CategoryUpdate, CategoryResponse)

router = APIRouter(prefix="/categories", tags=["Categories"])

# Endpoints para categorías
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/{business_id}/", response_model=List[CategoryResponse])
def get_category(business_id: UUID, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.business_id == business_id).all()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}/", response_model=CategoryResponse)
def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category_update.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}/", response_model=dict)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted successfully"}


# Endpoint para agregar un producto a una categoría
@router.post("/{category_id}/products/{product_id}/", response_model=CategoryResponse)
def add_product_to_category(category_id: int, product_id: UUID, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    category.products.append(product)
    db.commit()
    db.refresh(category)
    return category


# Endpoint para eliminar un producto de una categoría
@router.delete("/{category_id}/products/{product_id}/", response_model=CategoryResponse)
def remove_product_from_category(category_id: int, product_id: UUID, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    category.products.remove(product)
    db.commit()
    db.refresh(category)
    return category
