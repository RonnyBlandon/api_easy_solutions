from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from database.session import get_db
from database.models.product_model import Product, ProductImage, Option, Extra
from schemas.product_schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    ProductImageCreate, ProductImageUpdate, ProductImageResponse,
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
    # Agregar imágenes si se proporcionan
    if product.images:
        db_images = [
            ProductImage(product_id=db_product.id, **image.model_dump())
            for image in product.images
        ]
        db.add_all(db_images)
        db.commit()
    # Refrescar el producto para incluir las imágenes asociadas
    db.refresh(db_product)
    return ProductResponse.model_validate(db_product)



@router.get("/{product_id}/", response_model=ProductResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.model_validate(product)


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


# Endpoints para imágenes de productos
@router.post("/{product_id}/images/", response_model=ProductImageResponse)
def add_product_image(product_id: UUID, image: ProductImageCreate, db: Session = Depends(get_db)):
    # Verificar si el producto existe
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Crear instancia del modelo ProductImage excluyendo el campo product_id para evitar conflicto
    db_image = ProductImage(**image.model_dump(exclude={"product_id"}), product_id=product_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return ProductImageResponse.model_validate(db_image)


@router.delete("/images/{image_id}/", response_model=dict)
def delete_product_image(image_id: UUID, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    db.delete(image)
    db.commit()
    return {"detail": "Product image deleted successfully"}


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
