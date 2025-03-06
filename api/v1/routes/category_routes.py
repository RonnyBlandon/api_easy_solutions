from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import UUID
from core.security import get_current_active_user
from database.session import get_db
from database.models.product_model import CategoryProductAssociation, Product, Category
from database.models.business_model import Business
from database.models.favourite_model import Favourite
from schemas.auth_schemas import TokenData
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
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Este negocio no tiene esta categoría.")

    products_query = (
        db.query(
            Product,
            func.coalesce(Favourite.product_id.isnot(None), False).label("is_favorite")
        )
        .outerjoin(Favourite, 
                   (Favourite.product_id == Product.id) & 
                   (Favourite.user_id == current_user.local_id))
        .filter(Product.categories.any(id=category.id)).all()
    )

    category_response = {
        "id": category.id,
        "name": category.name,
        "business_id": category.business_id,
        "products": [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "product_image_url": product.product_image_url,
                "stock": product.stock,
                "available": product.available,
                "business_id": product.business_id,
                "discount": product.discount,
                "is_active": product.is_active,
                "options": product.options,
                "is_favorite": is_favorite
            }
            for product, is_favorite in products_query
        ]
    }
    
    return category_response


@router.get("/restaurant/{business_id}/", response_model=BusinessWithCategoriesResponse)
def get_restaurant_categories(business_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)):
    # Consultar negocio y si es favorito
    business_query = (
        db.query(
            Business,
            func.coalesce(Favourite.business_id.isnot(None), False).label("is_favorite")
        )
        .outerjoin(Favourite, 
                   (Favourite.business_id == Business.id) & 
                   (Favourite.user_id == current_user.local_id))
        .filter(Business.id == business_id)
    )

    result = business_query.first()
    if not result:
        raise HTTPException(status_code=404, detail="No existe este negocio.")

    business, is_favorite = result

    # Obtener las categorías del negocio
    categories = db.query(Category).filter(Category.business_id == business_id).all()

    if not categories:
        raise HTTPException(status_code=404, detail="Este negocio no tiene categorías.")

    categories_response = []
    for category in categories:
        products_query = (
            db.query(
                Product,
                func.coalesce(Favourite.product_id.isnot(None), False).label("is_favorite")
            )
            .join(CategoryProductAssociation)
            .outerjoin(Favourite, 
                       (Favourite.product_id == Product.id) & 
                       (Favourite.user_id == current_user.local_id))
            .filter(CategoryProductAssociation.category_id == category.id).all()
        )

        category_dict = {
            "id": category.id,
            "name": category.name,
            "business_id": category.business_id,
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "product_image_url": product.product_image_url,
                    "stock": product.stock,
                    "available": product.available,
                    "business_id": product.business_id,
                    "discount": product.discount,
                    "is_active": product.is_active,
                    "options": product.options,
                    "is_favorite": is_favorite
                }
                for product, is_favorite in products_query
            ]
        }
        
        categories_response.append(category_dict)

    return {
        "business": {
            "id": business.id,
            "address": business.address,
            "admin_id": business.admin_id,
            "business_name": business.business_name,
            "municipality_id": business.municipality_id,
            "country": business.country,
            "description": business.description,
            "email": business.email,
            "lat": business.lat,
            "long": business.long,
            "phone_number": business.phone_number,
            "zip_code": business.zip_code,
            "is_active": business.is_active,
            "is_popular_this_week": business.is_popular_this_week,
            "is_novelty": business.is_novelty,
            "has_free_delivery": business.has_free_delivery,
            "has_alcohol": business.has_alcohol,
            "is_open_now": business.is_open_now,
            "average_price": business.average_price,
            "average_delivery": business.average_delivery,
            "type_business": business.type_business,
            "business_images": business.business_images,
            "is_favorite": is_favorite
        },
        "business_categories": categories_response
    }


@router.get("/business/{business_id}/", response_model=BusinessWithCategoriesResponse)
def get_business_categories(business_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user)
):
    limit = 5  # Limitar la cantidad de productos por categoría

    # Consultar negocio y si es favorito
    business_query = (
        db.query(
            Business,
            func.coalesce(Favourite.business_id.isnot(None), False).label("is_favorite")
        )
        .outerjoin(Favourite, 
                   (Favourite.business_id == Business.id) & 
                   (Favourite.user_id == current_user.local_id))
        .filter(Business.id == business_id)
    )

    result = business_query.first()
    if not result:
        raise HTTPException(status_code=404, detail="No existe este negocio.")

    business, is_favorite = result

    # Obtener las categorías del negocio
    categories = db.query(Category).filter(Category.business_id == business_id).all()

    categories_response = []
    for category in categories:
        products_query = (
            db.query(
                Product,
                func.coalesce(Favourite.product_id.isnot(None), False).label("is_favorite")
            )
            .join(CategoryProductAssociation)
            .outerjoin(Favourite, 
                       (Favourite.product_id == Product.id) & 
                       (Favourite.user_id == current_user.local_id))
            .filter(CategoryProductAssociation.category_id == category.id)
            .limit(limit)
            .all()
        )

        # Crear una estructura serializable sin modificar la relación ORM
        category_dict = {
            "id": category.id,
            "name": category.name,
            "business_id": category.business_id,
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "product_image_url": product.product_image_url,
                    "stock": product.stock,
                    "available": product.available,
                    "business_id": product.business_id,
                    "discount": product.discount,
                    "is_active": product.is_active,
                    "options": product.options,
                    "is_favorite": is_favorite
                }
                for product, is_favorite in products_query
            ]
        }
        
        categories_response.append(category_dict)

    return {
        "business": {
            "id": business.id,
            "address": business.address,
            "admin_id": business.admin_id,
            "business_name": business.business_name,
            "municipality_id": business.municipality_id,
            "country": business.country,
            "description": business.description,
            "email": business.email,
            "lat": business.lat,
            "long": business.long,
            "phone_number": business.phone_number,
            "zip_code": business.zip_code,
            "is_active": business.is_active,
            "is_popular_this_week": business.is_popular_this_week,
            "is_novelty": business.is_novelty,
            "has_free_delivery": business.has_free_delivery,
            "has_alcohol": business.has_alcohol,
            "is_open_now": business.is_open_now,
            "average_price": business.average_price,
            "average_delivery": business.average_delivery,
            "type_business": business.type_business,
            "business_images": business.business_images,
            "is_favorite": is_favorite
        },
        "business_categories": categories_response
    }


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
