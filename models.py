from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_email = Column(String(100))
    contact_phone = Column(String(20))
    address = Column(Text)
    product_categories = Column(String(200))  # Comma-separated categories
    
    # Relationship
    products = relationship("Product", back_populates="supplier")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    brand = Column(String(50))
    price = Column(Float)
    category = Column(String(50))
    description = Column(Text)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    
    # Relationship
    supplier = relationship("Supplier", back_populates="products") 