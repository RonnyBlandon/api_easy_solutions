from pydantic import BaseModel, UUID4
from typing import Optional, List

class PaymentMethodBase(BaseModel):
    name_in_the_card: str
    card_number: str
    month_and_year: str
    cvc: str
    card_alias: str
    card_provider: Optional[str] = None
    is_main_payment_method: bool

class PaymentMethodCreate(PaymentMethodBase):
    pass  # Se utiliza al crear un nuevo método de pago

class PaymentMethodUpdate(BaseModel):
    id: UUID4
    name_in_the_card: Optional[str]
    card_number: Optional[str]
    month_and_year: Optional[str]
    cvc: Optional[str]
    card_alias: Optional[str]
    card_provider: Optional[str]
    is_main_payment_method: Optional[bool]

class PaymentMethodResponse(PaymentMethodBase):
    id: UUID4

    class Config:
        from_attributes = True

class PaymentMethodListResponse(BaseModel):
    payment_method_list: List[PaymentMethodResponse]
