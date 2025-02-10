from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombreProducto = Column(String(255), nullable=False)
    descripcion = Column(String(500))
    marca = Column(String(100), nullable=False)
    precio = Column(DECIMAL(10,2), nullable=False)
    proveedor_id = Column(Integer, nullable=False)
    proveedor_nombre = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")
