import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import Base, Supplier, Product

# Create tables
Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    try:
        # Check if we already have data
        if db.query(Supplier).first():
            print("Database already initialized!")
            return

        # Create sample suppliers
        suppliers = [
            Supplier(
                name="TechCorp Inc.",
                contact_email="contact@techcorp.com",
                contact_phone="1-800-TECH",
                address="123 Tech Street, Silicon Valley, CA",
                product_categories="Laptops, Smartphones, Tablets"
            ),
            Supplier(
                name="ElectroGoods Ltd.",
                contact_email="sales@electrogoods.com",
                contact_phone="1-888-ELECTRO",
                address="456 Electronics Ave, New York, NY",
                product_categories="TVs, Audio Equipment, Gaming"
            ),
            Supplier(
                name="SmartGear Solutions",
                contact_email="info@smartgear.com",
                contact_phone="1-877-SMART",
                address="789 Innovation Road, Seattle, WA",
                product_categories="Wearables, Smart Home, Accessories"
            )
        ]
        db.add_all(suppliers)
        db.commit()

        # Create sample products
        products = [
            # TechCorp Products
            Product(
                name="UltraBook Pro",
                brand="TechCorp",
                price=1299.99,
                category="Laptops",
                description="High-performance laptop with 16GB RAM and 512GB SSD",
                supplier_id=1
            ),
            Product(
                name="SmartPhone X",
                brand="TechCorp",
                price=799.99,
                category="Smartphones",
                description="Latest smartphone with 5G capability",
                supplier_id=1
            ),
            # ElectroGoods Products
            Product(
                name="4K Smart TV",
                brand="ElectroGoods",
                price=699.99,
                category="TVs",
                description="55-inch 4K Smart TV with HDR",
                supplier_id=2
            ),
            Product(
                name="Gaming Console Pro",
                brand="ElectroGoods",
                price=499.99,
                category="Gaming",
                description="Next-gen gaming console with 4K graphics",
                supplier_id=2
            ),
            # SmartGear Products
            Product(
                name="SmartWatch Elite",
                brand="SmartGear",
                price=299.99,
                category="Wearables",
                description="Advanced smartwatch with health monitoring",
                supplier_id=3
            ),
            Product(
                name="Smart Home Hub",
                brand="SmartGear",
                price=149.99,
                category="Smart Home",
                description="Central hub for smart home automation",
                supplier_id=3
            )
        ]
        db.add_all(products)
        db.commit()

        print("Database initialized successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 