from sqlalchemy.orm import Session

import models, schemas

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, description=product.description, price=product.price, image_url=product.image_url)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(product_id=order.product_id, quantity=order.quantity, customer_name=order.customer_name, customer_email=order.customer_email, shipping_address=order.shipping_address)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()
