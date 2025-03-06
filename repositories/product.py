from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from database.models.favourite_model import Favourite
from database.models.product_model import Product

from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists

def search_products(db: Session, business_id: UUID, query: str, user_id: UUID):
    FavouriteAlias = aliased(Favourite)
    
    stmt = select(
        Product,
        exists().where(
            (FavouriteAlias.product_id == Product.id) &
            (FavouriteAlias.user_id == user_id)
        ).label("is_favorite")
    ).where(
        Product.business_id == business_id,
        Product.name.ilike(f"%{query}%")
    )

    result = db.execute(stmt).all()
    
    # Mapear resultados para incluir `is_favorite`
    products = [
        {**product[0].__dict__, "is_favorite": product[1]} 
        for product in result
    ]

    return products



def get_products_by_ids(db: Session, product_ids: list[UUID], user_id: UUID):
    FavouriteAlias = aliased(Favourite)
    
    stmt = select(
        Product,
        exists().where(
            (FavouriteAlias.product_id == Product.id) &
            (FavouriteAlias.user_id == user_id)
        ).label("is_favorite")
    ).where(Product.id.in_(product_ids))

    result = db.execute(stmt).all()
    
    # Mapear resultados para incluir `is_favorite`
    products = [
        {**product[0].__dict__, "is_favorite": product[1]} 
        for product in result
    ]

    # Crear un diccionario con los productos obtenidos
    product_dict = {product["id"]: product for product in products}
    
    # Reordenar según el orden original
    ordered_products = [product_dict[pid] for pid in product_ids if pid in product_dict]
    
    return ordered_products