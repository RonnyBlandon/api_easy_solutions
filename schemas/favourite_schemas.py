from pydantic import BaseModel, UUID4, model_validator
from typing import Optional

class FavouriteBusinessCreate(BaseModel):
    business_id: str

class FavouriteProductCreate(BaseModel):
    product_id: str

class FavouriteResponse(BaseModel):
    message: str
