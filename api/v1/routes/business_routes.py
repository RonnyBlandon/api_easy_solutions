from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from database.session import get_db
from database.models.business_model import Business, BusinessImage, TypeBusiness
from schemas.business_schemas import (
    BusinessCreate,
    BusinessResponse,
    BusinessImageCreate,
    BusinessImageResponse,
    TypeBusinessCreate,
    TypeBusinessResponse,
)

router = APIRouter(prefix="/businesses", tags=["Businesses"])

# Endpoint para crear un negocio
@router.post("/", response_model=BusinessResponse, status_code=201)
def create_business(business_data: BusinessCreate, db: Session = Depends(get_db)):
    new_business = Business(**business_data.model_dump())
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    return new_business

# Endpoint para obtener todos los negocios
@router.get("/", response_model=List[BusinessResponse])
def get_all_businesses(db: Session = Depends(get_db)):
    businesses = db.query(Business).all()
    return businesses

# Endpoint para obtener un negocio por ID
@router.get("/{business_id}", response_model=BusinessResponse)
def get_business_by_id(business_id: UUID, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

# Endpoint para actualizar un negocio
@router.put("/{business_id}", response_model=BusinessResponse)
def update_business(business_id: UUID, business_data: BusinessCreate, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    for key, value in business_data.dict().items():
        setattr(business, key, value)
    
    db.commit()
    db.refresh(business)
    return business

# Endpoint para eliminar un negocio
@router.delete("/{business_id}", status_code=204)
def delete_business(business_id: UUID, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    db.delete(business)
    db.commit()
    return {"detail": "Business deleted successfully"}

# Endpoint para agregar una imagen a un negocio
@router.post("/{business_id}/images", response_model=BusinessImageResponse, status_code=201)
def add_business_image(business_id: UUID, image_data: BusinessImageCreate, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    new_image = BusinessImage(**image_data.dict())
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

# Endpoint para obtener los tipos de negocio
@router.get("/types", response_model=List[TypeBusinessResponse])
def get_all_type_businesses(db: Session = Depends(get_db)):
    types = db.query(TypeBusiness).all()
    return types

# Endpoint para crear un tipo de negocio
@router.post("/types", response_model=TypeBusinessResponse, status_code=201)
def create_type_business(type_data: TypeBusinessCreate, db: Session = Depends(get_db)):
    new_type = TypeBusiness(**type_data.dict())
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type
