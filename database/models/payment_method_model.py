from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database.session import Base

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="CASCADE"), nullable=False)
    name_in_the_card = Column(String, nullable=False)
    card_number = Column(String, nullable=False)
    month_and_year = Column(String, nullable=False)
    cvc = Column(String, nullable=False)
    card_alias = Column(String, nullable=True)
    is_main_payment_method = Column(Boolean, default=False, nullable=False)
    card_provider = Column(String, nullable=True)  # Ejemplo: 'Visa', 'MasterCard', 'Banco XYZ'

    user = relationship("User", back_populates="payment_methods")
