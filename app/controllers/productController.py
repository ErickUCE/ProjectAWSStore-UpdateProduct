from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductUpdate
import os
import requests

# 🔥 URLs de los microservicios `CreateProduct` y `ReadProduct`
CREATE_PRODUCT_SERVICE_URL = os.getenv("CREATE_PRODUCT_SERVICE_URL", "http://localhost:8000")
READ_PRODUCT_SERVICE_URL = os.getenv("READ_PRODUCT_SERVICE_URL", "http://localhost:8002")
UPDATE_PRODUCT_SERVICE_URL= os.getenv("UPDATE_PRODUCT_SERVICE_URL", "http://localhost:8003")

def update_product(product_id: int, product_update: ProductUpdate, db: Session):
    """ 📌 Actualiza un producto en `UpdateProduct` y lo sincroniza con `CreateProduct` y `ReadProduct` """

    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return {"error": "Producto no encontrado en UpdateProduct"}

    # 🔄 Actualizar solo los campos proporcionados (sin el `updated_at`)
    update_data = product_update.dict(exclude_unset=True)

    # Eliminar 'updated_at' si está presente en la actualización (MySQL lo maneja automáticamente)
    if 'updated_at' in update_data:
        del update_data['updated_at']

    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    print(f"✅ Producto actualizado en UpdateProduct: {db_product.nombreProducto}")

    # 🔄 **Sincronizar con `CreateProduct` y `ReadProduct`**
    sync_with_microservices(db_product)

    return db_product


def sync_with_microservices(product):
    """ 🔄 Enviar producto a `ReadProduct` y `UpdateProduct` """
    
    sync_services = [
        f"{CREATE_PRODUCT_SERVICE_URL}/sync-create",  # URL de CreateProduct
        f"{READ_PRODUCT_SERVICE_URL}/sync-create",  # URL de ReadProduct
        f"{UPDATE_PRODUCT_SERVICE_URL}/sync-create"  # URL de UpdateProduct
    ]

    product_data = {
        "id": product.id,
        "nombreProducto": product.nombreProducto,
        "descripcion": product.descripcion,
        "marca": product.marca,
        "precio": float(product.precio),
        "proveedor_id": product.proveedor_id,
        "proveedor_nombre": product.proveedor_nombre
    }

    for service in sync_services:
        try:
            response = requests.post(service, json=product_data)
            if response.status_code == 200:
                print(f"✅ Producto sincronizado con {service}")
            else:
                print(f"⚠️ Error sincronizando con {service}. Código: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error enviando solicitud a {service}: {e}")



def sync_create_product(product_data: dict, db: Session):
    """ 📌 Sincronizar un producto creado en CreateProduct """
    db_product = Product(
        id=product_data["id"],  # 🔹 Asegura que el ID coincide con el de CreateProduct
        nombreProducto=product_data["nombreProducto"],
        descripcion=product_data["descripcion"],
        marca=product_data["marca"],
        precio=product_data["precio"],
        proveedor_id=product_data["proveedor_id"],
        proveedor_nombre=product_data["proveedor_nombre"],
    )
    
    # 🔥 Verifica si el producto ya existe antes de insertarlo
    existing_product = db.query(Product).filter(Product.id == db_product.id).first()
    if existing_product:
        print(f"⚠️ Producto con ID {db_product.id} ya existe en ReadProduct.")
        return
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    print(f"✅ Producto sincronizado en UpdateProduct: {db_product.nombreProducto}")
    return db_product