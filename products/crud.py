from .models import Products
from .schemas import ProductBase, ProductListView,ProductUpdateSchema
from sqlalchemy.orm.session import Session
from fastapi import HTTPException,status

def create_products(db: Session, request: ProductBase):

    new_product = Products(
        name = request.name,
        description = request.description,
        price  = request.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

def get_all_products(db: Session):

    return db.query(Products).all()

def get_a_product(id: str, db: Session):
    product = db.query(Products).filter(Products.id == id).first()
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {id} not found")
    return product


def update_a_product(id: str, request: ProductUpdateSchema, db: Session):

    product = db.query(Products).filter(Products.pkid == id)
    if not product.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {id} not found")

    product.update({
        Products.name : request.name,
        Products.description : request.description,
        Products.duration : request.duration,
        Products.price : request.price
    })

    db.commit()
    return "Updated Successfully"

def delete_a_product(id: int, db: Session):
    product = db.query(Products).filter(Products.pkid == id).first()
    db.delete(product)
    db.commit()
    return "Deleted Successfully"