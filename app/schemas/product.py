from pydantic import BaseModel
from typing import Optional

class ProductUpdate(BaseModel):
    nombreProducto: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    precio: Optional[float] = None
    proveedor_id: Optional[int] = None
