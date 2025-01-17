from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.session import Base

class BusinessInvoice(Base):
    __tablename__ = "business_invoices"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    invoice_date = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(Enum("PENDING", "PAID", "OVERDUE", name="invoice_status"), default="PENDING", nullable=False)
    total_amount = Column(Numeric(precision=10, scale=2), nullable=False)
    commission_amount = Column(Numeric(precision=10, scale=2), nullable=False)
    service_fee = Column(Numeric(precision=10, scale=2), nullable=True, default=0.00)  # Tarifa adicional si aplica
    notes = Column(Text, nullable=True)

    business = relationship("Business", back_populates="invoices")