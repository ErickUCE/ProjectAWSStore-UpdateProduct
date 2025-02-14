from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductUpdate
import os
import requests

# 🔥 URLs de los microservicios `CreateProduct` y `ReadProduct`
CREATE_PRODUCT_SERVICE_URL = os.getenv("CREATE_PRODUCT_SERVICE_URL", "http://13.216.61.88:8000")
READ_PRODUCT_SERVICE_URL = os.getenv("READ_PRODUCT_SERVICE_URL", "http://44.195.73.5:8007")
UPDATE_PRODUCT_SERVICE_URL= os.getenv("UPDATE_PRODUCT_SERVICE_URL", "http://54.165.250.5:8006")
DELETE_PRODUCT_SERVICE_URL= os.getenv("DELETE_PRODUCT_SERVICE_URL", "http://52.44.127.200:8005")

def update_product(product_id: int, product_update: ProductUpdate, db: Session):
    """Actualiza un producto en `UpdateProduct` y lo sincroniza con `CreateProduct` y `ReadProduct"""
    
    # Buscar el producto por ID
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return {"error": "Producto no encontrado en UpdateProduct"}

    # Actualiza los datos del producto, sin incluir `updated_at`
    update_data = product_update.model_dump(exclude_unset=True)  # Usando model_dump en lugar de dict

    # Eliminar 'updated_at' si está presente en los datos de actualización
    if 'updated_at' in update_data:
        del update_data['updated_at']

    # Aplicar los cambios a los campos del producto
    for key, value in update_data.items():
        setattr(db_product, key, value)

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(db_product)

    print(f"✅ Producto actualizado en UpdateProduct: {db_product.nombreProducto}")

    # Sincronizar con `CreateProduct` y `ReadProduct`
    sync_with_microservices(db_product)

    return db_product



def sync_with_microservices(product):
    """ 🔄 Sincronizar con `CreateProduct` y `ReadProduct` """

    sync_services = [
        f"{CREATE_PRODUCT_SERVICE_URL}/sync-update",
        f"{READ_PRODUCT_SERVICE_URL}/sync-update",
        f"{DELETE_PRODUCT_SERVICE_URL}/sync-update"
    ]

    product_data = {
        "id": product.id,
        "nombreProducto": product.nombreProducto,
        "descripcion": product.descripcion,
        "marca": product.marca,
        "precio": float(product.precio),  # ✅ Convertir Decimal a float
        "proveedor_id": product.proveedor_id,
        "proveedor_nombre": product.proveedor_nombre
    }

    for service in sync_services:
        try:
            response = requests.post(service, json=product_data)
            if response.status_code == 200:
                print(f"✅ Sincronización exitosa con {service}")
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
        print(f"⚠️ Producto con ID {db_product.id} ya existe en Updateeee.")
        return
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    print(f"✅ Producto sincronizado en UpdateProduct: {db_product.nombreProducto}")
    return db_product