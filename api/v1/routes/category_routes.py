from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from uuid import UUID
from database.session import get_db
from database.models.product_model import CategoryProductAssociation, Product, Category
from database.models.business_model import Business
from schemas.product_schemas import (BusinessWithCategoriesResponse, CategoryCreate, CategoryUpdate, CategoryResponse)

router = APIRouter(prefix="/categories", tags=["Categories"])

# Endpoints para categorías
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/category/{category_id}/", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Este negocio no tiene esta categoría.")
    return category


@router.get("/restaurant/{business_id}/", response_model=BusinessWithCategoriesResponse)
def get_restaurant_categories(business_id: UUID, db: Session = Depends(get_db)):
    categories = db.query(Category).filter(Category.business_id == business_id).all()
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="No existe este negocio.")
    if not categories:
        raise HTTPException(status_code=404, detail="Este negocio no tiene categorías.")
    return {"business": business, "business_categories": categories}


@router.get("/business/{business_id}/", response_model=BusinessWithCategoriesResponse)
def get_business_categories(business_id: UUID, db: Session = Depends(get_db)):

    limit = 10  # Limita la cantidad de productos por categoria

    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="No existe este negocio.")

    # Obtener las categorías del negocio
    categories = (
        db.query(Category)
        .filter(Category.business_id == business_id)
        .options(joinedload(Category.products))
        .all()
    )

    # Limitar los productos por categoría
    for category in categories:
        category.products = db.query(Product).join(CategoryProductAssociation).filter(
            CategoryProductAssociation.category_id == category.id
        ).limit(limit).all()

    return {"business": business, "business_categories": categories}


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
