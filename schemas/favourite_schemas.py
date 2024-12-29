from pydantic import BaseModel, UUID4
from typing import Optional
from schemas.user_schemas import UserResponse
from schemas.business_schemas import BusinessResponse
from schemas.product_schemas import ProductResponse

# Schemas for Favourite
class FavouriteBase(BaseModel):
    user_id: UUID4
    business_id: UUID4
    product_id: UUID4


class FavouriteCreate(FavouriteBase):
    pass


class FavouriteResponse(FavouriteBase):
    id: int
    user: Optional["UserResponse"] = None
    business: Optional["BusinessResponse"] = None
    product: Optional["ProductResponse"] = None

    class Config:
        from_attributes = True

