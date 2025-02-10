from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductUpdate
from app.controllers.productController import update_product
from app.controllers.productController import sync_create_product


router = APIRouter()

# 📌 Endpoint para actualizar un producto
@router.put("/products/{product_id}")
def update_product_endpoint(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    return update_product(product_id, product_update, db)

# 📌 Endpoint para recibir la sincronización desde `CreateProduct`
@router.post("/sync-create", status_code=200)
def sync_product_create(product_data: dict, db: Session = Depends(get_db)):
    return sync_create_product(product_data, db)
