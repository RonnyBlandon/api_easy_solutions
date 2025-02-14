from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models.product_model import Product

def search_products(db: Session, business_id: int, query: str):
    stmt = select(Product).where(
        Product.business_id == business_id,
        Product.name.ilike(f"%{query}%")
    )
    return db.execute(stmt).scalars().all()


def get_products_by_ids(db: Session, product_ids: list[int]):
    stmt = select(Product).where(Product.id.in_(product_ids))
    return db.execute(stmt).scalars().all()