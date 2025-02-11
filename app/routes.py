from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductUpdate
from app.controllers.productController import update_product
from app.controllers.productController import sync_create_product
from app.models.product import Product


router = APIRouter()

# 📌 Endpoint para actualizar un producto
@router.put("/products/{product_id}")
def update_product_endpoint(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    return update_product(product_id, product_update, db)

# 📌 Endpoint para recibir la sincronización desde `CreateProduct`
@router.post("/sync-create", status_code=200)
def sync_product_create(product_data: dict, db: Session = Depends(get_db)):
    return sync_create_product(product_data, db)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.productController import update_product
from app.schemas.product import ProductUpdate

router = APIRouter()

# 📌 Endpoint para actualizar un producto
@router.put("/products/{product_id}")
def update_product_endpoint(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    return update_product(product_id, product_update, db)

# 📌 Endpoint para recibir la sincronización desde `CreateProduct`
@router.post("/sync-create", status_code=200)
def sync_product_create(product_data: dict, db: Session = Depends(get_db)):
    return sync_create_product(product_data, db)

# 📌 Endpoint para recibir actualizaciones desde `CreateProduct`
@router.post("/sync-update", status_code=200)
def sync_product_update(product_data: dict, db: Session = Depends(get_db)):
    return sync_update_product(product_data, db)


@router.post("/sync-delete")
def sync_delete_product(product_data: dict, db: Session = Depends(get_db)):
    """Elimina el producto en `CreateProduct` cuando `DeleteProduct` lo notifica."""
    
    print(f"🔍 Recibiendo solicitud de eliminación: {product_data}")  # Debugging

    product_id = product_data.get("id")  # ✅ Extraer ID del producto

    if not product_id:
        print("❌ Error: ID de producto no encontrado en la solicitud")
        return {"error": "ID de producto no encontrado en la solicitud"}

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        print(f"⚠️ Producto con ID {product_id} no encontrado en read.")
        return {"error": "Producto no encontrado en read"}

    db.delete(product)
    db.commit()

    print(f"✅ Producto eliminado en Read: {product_id}")

    return {"message": "Producto eliminado correctamente"}

