from fastapi import APIRouter, HTTPException, Depends, Query
from core.security import get_current_active_user
from repositories.product import get_products_by_ids, search_products
from sqlalchemy.orm import Session
from uuid import UUID
from database.session import get_db
from database.models.product_model import Product, Option, Extra
from schemas.auth_schemas import TokenData
from schemas.product_schemas import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse, ProductIdsRequest,
    OptionCreate, OptionUpdate, OptionResponse,
    ExtraCreate, ExtraUpdate, ExtraResponse
)

router = APIRouter(prefix="/products", tags=["Products"])

# Endpoints para productos
@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Crear el producto principal
    db_product = Product(**product.model_dump(exclude={"images"}))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Refrescar el producto para incluir las imágenes asociadas
    db.refresh(db_product)
    return ProductResponse.model_validate(db_product)


@router.get("/search", response_model=ProductListResponse)
def search_products_endpoint(
    business_id: UUID,
    query: str | None = Query(None, description="Texto a buscar en el nombre del producto"),
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),  # Obtener el usuario autenticado
):
    if not query:
        return {"product_list": []}

    return {"product_list": search_products(db, business_id, query, current_user.local_id)}


@router.post("/search_by_ids/", response_model=ProductListResponse)
def get_products_by_ids_endpoint(
    request: ProductIdsRequest,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user)  # Obtener el usuario autenticado
):
    return {"product_list": get_products_by_ids(db, request.product_ids, current_user.local_id)}



@router.get("/{product_id}/", response_model=ProductResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}/", response_model=ProductResponse)
def update_product(product_id: UUID, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return ProductResponse.model_validate(product)


@router.delete("/{product_id}/", response_model=dict)
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}


# Endpoints para opciones
@router.post("/options/", response_model=OptionResponse)
def create_option(option: OptionCreate, db: Session = Depends(get_db)):
    db_option = Option(**option.model_dump())
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return OptionResponse.model_validate(db_option)


@router.delete("/options/{option_id}/", response_model=dict)
def delete_option(option_id: UUID, db: Session = Depends(get_db)):
    option = db.query(Option).filter(Option.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")

    db.delete(option)
    db.commit()
    return {"detail": "Option deleted successfully"}


# Endpoints para extras
@router.post("/extras/", response_model=ExtraResponse)
def create_extra(extra: ExtraCreate, db: Session = Depends(get_db)):
    db_extra = Extra(**extra.model_dump())
    db.add(db_extra)
    db.commit()
    db.refresh(db_extra)
    return ExtraResponse.model_validate(db_extra)


@router.delete("/extras/{extra_id}/", response_model=dict)
def delete_extra(extra_id: UUID, db: Session = Depends(get_db)):
    extra = db.query(Extra).filter(Extra.id == extra_id).first()
    if not extra:
        raise HTTPException(status_code=404, detail="Extra not found")

    db.delete(extra)
    db.commit()
    return {"detail": "Extra deleted successfully"}
