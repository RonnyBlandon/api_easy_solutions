from pydantic import BaseModel, UUID4, model_validator
from typing import Optional

class FavouriteBase(BaseModel):
    user_id: UUID4
    business_id: Optional[UUID4] = None
    product_id: Optional[UUID4] = None

    @model_validator(mode="before")
    def check_business_or_product(cls, values):
        if isinstance(values, dict):
            business_id = values.get("business_id")
            product_id = values.get("product_id")
        else:
            business_id = getattr(values, "business_id", None)
            product_id = getattr(values, "product_id", None)

        if not business_id and not product_id:
            raise ValueError("Debe especificar al menos un negocio o un producto.")
        if business_id and product_id:
            raise ValueError("No puede especificar ambos: negocio y producto.")
        return values


class FavouriteCreate(FavouriteBase):
    pass

class FavouriteResponse(FavouriteBase):
    id: int

    class Config:
        from_attributes = True
