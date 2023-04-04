from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from .schemas import ProductBase,ProductUpdateSchema,ProductListView
from .crud import create_products, get_all_products, get_a_product, delete_a_product, update_a_product
from config.database import get_db


router = APIRouter(
    prefix="/api/v1/products",
    tags= ["products"]
)

@router.post("/create_product")
def create_product(request: ProductBase, db: Session = Depends(get_db)):
    return create_products(db, request)

@router.get("/all_products")
def list_products(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.get("/{id}/products", response_model = ProductListView)
def read_product(id: int, db: Session = Depends(get_db)):
    return get_a_product(id, db)

@router.delete("/delete/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    return delete_a_product(id, db)

@router.post("/update/{id}")
def update_product(id: int, request: ProductUpdateSchema, db: Session = Depends(get_db)):
    return update_a_product(id, request, db)